#!/usr/bin/env python3
"""Renderer di video didattici verticali (TikTok 1080x1920) da un file episodio JSON.

Uso:
  python3 render.py episodes/cpp-vector-01.json -o out/cpp-vector-01.mp4
  python3 render.py ep.json --music brano.mp3          # traccia audio opzionale
  python3 render.py ep.json --preview 1,6,12,20 -o out # salva solo PNG dei fotogrammi
  python3 render.py ep.json --set cps=22 --set hook_seconds=2.5   # override parametri

Tutti i parametri visivi e di ritmo sono in DEFAULTS e si possono sovrascrivere
dal blocco "theme" dell'episodio o da --set chiave=valore.
Il codice dell'episodio viene compilato ed eseguito davvero: l'output mostrato
nel terminale del video e' quello reale.
"""
import re
import argparse, json, math, os, shutil, subprocess, sys, tempfile
from bisect import bisect_right
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from pygments.lexers import CppLexer, JavaLexer
from pygments.token import Token

HERE = Path(__file__).resolve().parent
FONT_DIRS = [HERE / "fonts"]   # font inclusi nella cartella: stessi risultati su ogni dispositivo
FONT_DIRS += [Path(d) for d in (
    "/usr/share/fonts/truetype/dejavu", "/Library/Fonts", "/System/Library/Fonts/Supplemental",
    str(Path.home() / "Library/Fonts"), "C:/Windows/Fonts")]


def find_font(name):
    for d in FONT_DIRS:
        if (d / name).exists():
            return str(d / name)
    sys.exit(f"Font {name} non trovato. Controlla che strumenti/fonts/ sia presente.")

DEFAULTS = dict(
    width=1080, height=1920, fps=30,
    # ritmo
    cps=20.0, term_cps=30.0, step_pause=1.1, read_per_line=0.3, min_file_view=3.2, hook_seconds=3.0, iter_per_item=0.45,
    out_line_delay=0.4, outro_seconds=2.6, xfade=0.4,
    # tipografia
    code_font="auto", line_h=44, caption_font=54, term_font="auto",
    code_max=44, term_max=40, bottom_safe=1650,   # auto: dimensioni adattate a larghezza e altezza disponibili
    # layout (y)
    tag_y=150, caption_y=205, ide_y0=345, viz_gap=26, term_gap=22, viz_h=230, term_h=250,
    margin_l=30, margin_r=80,   # margine destro: i pulsanti di TikTok coprono la fascia in basso a destra
    # colori
    bg_top=(11, 16, 32), bg_bottom=(34, 18, 76),
    panel=(30, 30, 46), panel_bar=(24, 24, 37), term_bg=(17, 17, 27),
    text=(205, 214, 244), muted=(108, 112, 134), accent=(137, 180, 250),
    accent2=(245, 194, 231), good=(166, 227, 161), hl=(49, 50, 68),
    c_kw=(203, 166, 247), c_type=(249, 226, 175), c_str=(166, 227, 161),
    c_num=(250, 179, 135), c_com=(108, 112, 134), c_pre=(243, 139, 168),
    c_op=(137, 220, 235), c_fn=(137, 180, 250),
    hl_bad=(86, 38, 56), hl_ok=(34, 74, 52),
)
TYPE_NAMES = {"vector", "string", "map", "set", "size_t", "cout", "cin", "endl"}


def lerp(a, b, t):
    return tuple(int(round(x + (y - x) * t)) for x, y in zip(a, b))


def clamp(x, lo=0.0, hi=1.0):
    return max(lo, min(hi, x))


def ease_out_back(t):
    c1, c3 = 1.70158, 2.70158
    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2


def ease_out(t):
    return 1 - (1 - t) ** 3


_fonts = {}
def font(name, size):
    k = (name, size)
    if k not in _fonts:
        _fonts[k] = ImageFont.truetype(find_font(name), size)
    return _fonts[k]


def build_theme(ep, overrides):
    th = dict(DEFAULTS)
    th.update(ep.get("theme", {}))
    for kv in overrides or []:
        k, v = kv.split("=", 1)
        th[k] = json.loads(v) if v[:1] in "[0123456789-" else v
    for k, v in list(th.items()):
        if isinstance(v, list):
            th[k] = tuple(v)
    return th


def find_compiler():
    for c in ("g++", "clang++", "c++"):
        if shutil.which(c):
            return c
    sys.exit("Nessun compilatore C++ trovato (g++ / clang++). Esegui: python3 render.py --check")


def compile_and_run_java(code, filename, files=None, main_class="Main"):
    """Java: javac + java. Gli errori di compilazione e le eccezioni sono quelli reali.
    files = [{"name": "Conto.java", "code": ...}, ...] per piu' classi in file separati."""
    stem = main_class if files else Path(filename).stem
    with tempfile.TemporaryDirectory() as d:
        srcs = []
        for fl in (files or [{"name": filename, "code": code}]):
            src = Path(d) / fl["name"]
            src.write_text(fl["code"], encoding="utf-8")
            srcs.append(str(src))
        src = Path(d) / (files[0]["name"] if files else filename)
        c = subprocess.run(["javac", "-encoding", "UTF-8", "-Xlint:none"] + srcs,
                           capture_output=True, text=True, encoding="utf-8")
        if c.returncode != 0:
            errs = []
            for ln in c.stderr.splitlines():
                if "error:" in ln:
                    ln = ln.replace(d + os.sep, "").replace(d + "/", "")
                    errs.append(ln if len(ln) <= 54 else ln[:53] + "…")
            return None, errs[:2] or ["errore di compilazione"]
        r = subprocess.run(["java", "-cp", d, stem], capture_output=True, text=True,
                           encoding="utf-8", timeout=20)
        out = r.stdout
        if r.returncode != 0:
            ex = [l.replace('Exception in thread "main" ', "").replace("java.lang.", "")
                  for l in r.stderr.splitlines() if l.startswith("Exception") or l.startswith("Error")]
            out += "\n".join(ex[:2]) + "\n"
        return out, None


def compile_and_run(code, filename, files=None, main_class="Main"):
    """Compila ed esegue davvero il codice.
    Ritorna (stdout, None) se gira, oppure (None, [righe di errore]) se non compila."""
    if filename.endswith(".java"):
        return compile_and_run_java(code, filename, files, main_class)
    with tempfile.TemporaryDirectory() as d:
        src = Path(d) / filename
        src.write_text(code, encoding="utf-8")
        exe = Path(d) / ("prog.exe" if os.name == "nt" else "prog")
        c = subprocess.run([find_compiler(), "-std=c++17", "-Wall", str(src), "-o", str(exe)],
                           capture_output=True, text=True, encoding="utf-8")
        if c.returncode != 0:
            errs = []
            for ln in c.stderr.splitlines():
                if "error:" in ln:
                    ln = ln.replace(str(src), filename)
                    errs.append(ln if len(ln) <= 54 else ln[:53] + "…")
            return None, errs[:2] or ["errore di compilazione"]
        r = subprocess.run([str(exe)], capture_output=True, text=True, encoding="utf-8", timeout=10)
        return r.stdout, None


def run_cpp(code, filename):
    out, err = compile_and_run(code, filename)
    if out is None:
        sys.exit("ERRORE di compilazione:\n" + "\n".join(err))
    return out


def apply_fix(code, fix):
    lines = code.rstrip("\n").split("\n")
    lines[fix["line"] - 1] = fix["new"]
    return "\n".join(lines) + "\n"


def check_env():
    ok = True
    for tool, hint in (("ffmpeg", "installa ffmpeg (macOS: brew install ffmpeg)"),):
        path = shutil.which(tool)
        print(f"{'OK ' if path else 'MANCA'} {tool}", path or "-> " + hint)
        ok &= bool(path)
    comp = next((c for c in ("g++", "clang++", "c++") if shutil.which(c)), None)
    print(f"{'OK ' if comp else 'MANCA'} compilatore C++", comp or "-> macOS: xcode-select --install; Windows: MinGW/MSYS2")
    ok &= bool(comp)
    jv = shutil.which("javac") and shutil.which("java")
    print(f"{'OK ' if jv else 'MANCA'} JDK (javac/java, solo per gli episodi Java)", jv or "-> installa un JDK 17+")
    for f in ("DejaVuSans-Bold.ttf", "DejaVuSansMono.ttf", "DejaVuSansMono-Bold.ttf"):
        found = next((d / f for d in FONT_DIRS if (d / f).exists()), None)
        print(f"{'OK ' if found else 'MANCA'} font {f}", found or "")
        ok &= bool(found)
    print("Python", sys.version.split()[0], "| Pillow e Pygments importati correttamente")
    print("Ambiente PRONTO" if ok else "Ambiente INCOMPLETO")
    return ok


def char_colors(code, th, java=False):
    cols = []
    toks = list((JavaLexer() if java else CppLexer()).get_tokens(code))
    flat = "".join(t for _, t in toks)
    for i, (tt, text) in enumerate(toks):
        pos = len(cols) + len(text)
        nxt = flat[pos] if pos < len(flat) else ""
        if tt in Token.Comment.Preproc or tt in Token.Comment.PreprocFile:
            c = th["c_pre"]
        elif tt in Token.Comment:
            c = th["c_com"]
        elif tt in Token.Keyword.Type:
            c = th["c_type"]
        elif tt in Token.Keyword:
            c = th["c_kw"]
        elif tt in Token.Literal.String:
            c = th["c_str"]
        elif tt in Token.Literal.Number:
            c = th["c_num"]
        elif tt in Token.Operator:
            c = th["c_op"]
        elif tt in Token.Name:
            if text in TYPE_NAMES:
                c = th["c_type"]
            elif nxt == "(":
                c = th["c_fn"]
            else:
                c = th["text"]
        else:
            c = th["text"]
        cols.extend([c] * len(text))
    return cols[: len(code)]


class Timeline:
    def __init__(self, ep, th, runs):
        self.code = ep["code"].rstrip("\n")
        self.lines = self.code.split("\n")
        self.file_of, self.local_no, self.tabs, self.nrows = [], [], [], len(self.lines)
        if ep.get("files"):
            self.tabs = [f["name"] for f in ep["files"]]
            for fi, f in enumerate(ep["files"]):
                m = len(f["code"].rstrip("\n").split("\n"))
                self.file_of += [fi] * m
                self.local_no += list(range(m))
            self.nrows = max(self.local_no) + 1
        else:
            self.file_of = [0] * len(self.lines)
            self.local_no = list(range(len(self.lines)))
        self.line_start = []
        p = 0
        for ln in self.lines:
            self.line_start.append(p)
            p += len(ln) + 1
        by_line = {s["after_line"]: s for s in ep["steps"]}
        t = th["hook_seconds"] + 0.2
        self.type_t0 = t
        self.char_times = []
        self.events = []
        vals = 0
        for k, ln in enumerate(self.lines, start=1):
            indent = len(ln) - len(ln.lstrip(" "))
            for ci in range(len(ln)):
                if ci >= indent:
                    t += 1.0 / th["cps"]
                self.char_times.append(t)
            last_of_file = bool(self.tabs) and (k == len(self.lines) or self.file_of[k] != self.file_of[k - 1])
            if k < len(self.lines) and not last_of_file:
                t += 0.12
                self.char_times.append(t)
            if k in by_line:
                ev = dict(by_line[k])
                ev["t"] = t + 0.1
                v = ev.get("viz") or {}
                op = v.get("op")
                pause = th["step_pause"]
                if op == "init":
                    vals = len(v["values"])
                elif op == "push":
                    vals += 1
                elif op == "iterate":
                    pause = v.get("count", vals) * th["iter_per_item"] + 0.7
                if op != "iterate":   # tempo per leggere le righe appena scritte
                    pause = max(pause, th["read_per_line"] * len(ev.get("highlight_lines", [])) + 0.7)
                ev["n_items"] = vals
                self.events.append(ev)
                t += pause
            if last_of_file:   # il file e' finito: resta visibile il tempo di leggerlo, poi si cambia scheda
                nf = sum(1 for x in self.file_of if x == self.file_of[k - 1])
                t += max(th["min_file_view"], th["read_per_line"] * nf + 1.0)
                if k < len(self.lines):
                    t += 0.12
                    self.char_times.append(t)
        self.code_end = t
        t += 0.6
        self.views = []   # (t0, t1, file): rilettura di ogni file prima dell'esecuzione
        if self.tabs:
            for fi in range(len(self.tabs)):
                nf = sum(1 for x in self.file_of if x == fi)
                d_ = max(th["min_file_view"], th["read_per_line"] * nf + 1.0)
                self.views.append((t, t + d_, fi))
                t += d_
        else:
            t += th["read_per_line"] * len(self.lines) * 0.5   # il codice completo resta fermo prima dell'esecuzione
        quiz, fix = ep.get("quiz"), ep.get("fix")
        self.chal = quiz or fix
        self.chal_t0 = self.chal_dur = None
        if self.chal:
            self.chal_t0, self.chal_dur = t, float(self.chal.get("seconds", 3.0))
            t += self.chal_dur
        self.cmd = th.get("cmd_display") or (f"javac {ep['filename']} && java {Path(ep['filename']).stem}" if ep["filename"].endswith(".java") else f"g++ {ep['filename']} -o main && ./main")
        self.fix_t0 = self.fix_idx = self.fix_new = None
        self.fix_times = []
        self.runs = []
        for ri, run in enumerate(runs):
            if ri == 1:   # correzione del codice prima della seconda esecuzione
                t += 1.6
                self.fix_t0, self.fix_idx, self.fix_new = t, fix["line"] - 1, fix["new"]
                self.fix_times = [t + 0.3 + (i + 1) / th["cps"] for i in range(len(self.fix_new))]
                t = self.fix_times[-1] + 1.0
            run_t0 = t
            cmd_times = [t + (i + 1) / th["term_cps"] for i in range(len(self.cmd))]
            t = cmd_times[-1] + 0.6
            out_times = [t + i * th["out_line_delay"] for i in range(len(run["lines"]))]
            if out_times:
                t = out_times[-1]
            self.runs.append(dict(t0=run_t0, cmd_times=cmd_times, lines=run["lines"],
                                  out_times=out_times, bad=run.get("bad", False)))
        self.run_t0 = self.runs[0]["t0"]
        self.run2_t0 = self.runs[1]["t0"] if len(self.runs) > 1 else None
        self.outro_t0 = t + 1.4
        self.total = self.outro_t0 + th["outro_seconds"]
        self.max_items = max([e["n_items"] for e in self.events] + [1])

    def active_file(self, t):
        n = sum(1 for ct in self.char_times if ct <= t)
        for t0, t1, fi in self.views:
            if t0 <= t < t1:
                return fi, True
        cur = bisect_right(self.line_start, n) - 1 if n < len(self.code) else len(self.lines) - 1
        return self.file_of[cur], False

    def check_readable(self, th):
        """Ogni file deve restare completo e fermo in vista abbastanza a lungo per essere letto."""
        nfiles = max(1, len(self.tabs))
        problems = []
        for fi in range(nfiles):
            rows = sum(1 for x in self.file_of if x == fi)
            idx = [i for i, x in enumerate(self.file_of) if x == fi]
            last = self.char_times[min(idx[-1], len(self.char_times) - 1)]
            seen, t = 0.0, last
            while t < self.run_t0 + 1.0:
                if self.active_file(t)[0] == fi:
                    seen += 0.1
                t += 0.1
            need = max(th["min_file_view"] - 0.5, th["read_per_line"] * rows + 0.5)
            if seen < need:
                problems.append((fi, rows, round(seen, 1), round(need, 1)))
        return problems


class Renderer:
    def __init__(self, ep, th, tl):
        self.ep, self.th, self.tl = ep, th, tl
        self.W, self.H = th["width"], th["height"]
        self.L, self.R = th["margin_l"], self.W - th["margin_r"]
        self.colors = char_colors(tl.code, th, ep["filename"].endswith(".java"))
        self.fix_colors = []
        if tl.fix_new is not None:
            fixed = apply_fix(tl.code, ep["fix"]).rstrip("\n")
            st = tl.line_start[tl.fix_idx]
            self.fix_colors = char_colors(fixed, th, ep["filename"].endswith(".java"))[st:st + len(tl.fix_new)]
        n = tl.nrows
        self._autofit(th, tl, n)
        self.cw = font("DejaVuSansMono.ttf", th["code_font"]).getlength("M")
        self.ide_y1 = th["ide_y0"] + 56 + 24 + n * th["line_h"] + 18
        self.viz_y0 = self.ide_y1 + th["viz_gap"]
        self.viz_y1 = self.viz_y0 + th["viz_h"]
        self.term_y0 = self.viz_y1 + th["term_gap"]
        self.term_y1 = self.term_y0 + th["term_h"]
        if self.term_y1 > th["bottom_safe"] + 10:
            print(f"ATTENZIONE: il layout arriva a y={self.term_y1} (zona coperta dall'interfaccia di TikTok).")
        self.bg = self._gradient()
        self.base_main = self._static_main()

    def _autofit(self, th, tl, n):
        """Sceglie la dimensione massima di codice e terminale che entra nello schermo."""
        ratio = font("DejaVuSansMono.ttf", 100).getlength("M") / 100
        width = self.R - self.L
        all_out = [l for r_ in tl.runs for l in r_["lines"]]
        n_out = max(1, max(len([l for l in r_["lines"] if l != ""]) for r_ in tl.runs))
        if th["term_font"] == "auto":
            longest = max([len(tl.cmd) + 2] + [len(l) for l in all_out])
            th["term_font"] = max(24, min(th["term_max"], int((width - 56) / (ratio * longest))))
        th["term_h"] = max(th["term_h"], 56 + 22 + (th["term_font"] + 12) * (1 + n_out) + 26)
        if th["code_font"] == "auto":
            maxlen = max([len(l) for l in tl.lines] + ([len(tl.fix_new)] if tl.fix_new else []))
            f_w = (width - 100 - 24) / (ratio * maxlen)
            below = th["viz_gap"] + th["viz_h"] + th["term_gap"] + th["term_h"]
            code_h = th["bottom_safe"] - th["ide_y0"] - 56 - 24 - 18 - below
            f_h = code_h / (n * 1.375)
            th["code_font"] = max(24, min(th["code_max"], int(f_w), int(f_h)))
            th["line_h"] = round(th["code_font"] * 1.375)

    # ---------- statico ----------
    def _gradient(self):
        th = self.th
        im = Image.new("RGB", (self.W, self.H))
        d = ImageDraw.Draw(im)
        for y in range(self.H):
            d.line([(0, y), (self.W, y)], fill=lerp(th["bg_top"], th["bg_bottom"], y / self.H))
        return im

    def bg_at(self, y):
        return lerp(self.th["bg_top"], self.th["bg_bottom"], y / self.H)

    def _panel(self, d, y0, y1, title, body, bar):
        L, R = self.L, self.R
        d.rounded_rectangle((L, y0, R, y1), 22, fill=body)
        d.rounded_rectangle((L, y0, R, y0 + 56), 22, fill=bar)
        d.rectangle((L, y0 + 34, R, y0 + 56), fill=bar)
        for i, c in enumerate([(243, 139, 168), (249, 226, 175), (166, 227, 161)]):
            d.ellipse((L + 24 + i * 30, y0 + 20, L + 40 + i * 30, y0 + 36), fill=c)
        d.text((L + 130, y0 + 28), title, font=font("DejaVuSansMono.ttf", 26),
               fill=self.th["muted"], anchor="lm")

    def _static_main(self):
        th = self.th
        im = self.bg.copy()
        d = ImageDraw.Draw(im)
        self._panel(d, th["ide_y0"], self.ide_y1, self.ep["filename"], th["panel"], th["panel_bar"])
        d.rounded_rectangle((self.L, self.viz_y0, self.R, self.viz_y1), 22, fill=th["panel_bar"])
        self._panel(d, self.term_y0, self.term_y1, "Terminale", th["term_bg"], th["panel_bar"])
        return im

    # ---------- testo con dissolvenza ----------
    def text_fade(self, d, xy, s, f, fill, a, anchor="la"):
        if a <= 0:
            return
        col = lerp(self.bg_at(xy[1]), fill, clamp(a))
        d.text(xy, s, font=f, fill=col, anchor=anchor)

    # ---------- hook ----------
    def render_hook(self, t):
        th = self.th
        im = self.bg.copy()
        d = ImageDraw.Draw(im)
        self.text_fade(d, (self.W // 2, th["tag_y"]), self.ep["series"], font("DejaVuSans-Bold.ttf", 30),
                       th["muted"], 1, "mm")
        hook = self.ep["hook"]
        ys = [700, 830, 1010]
        for i, line in enumerate(hook):
            a = clamp((t - (0.2 + 0.7 * i)) / 0.3)
            last = i == len(hook) - 1
            size = 92 if last else 56
            while font("DejaVuSans-Bold.ttf", size).getlength(line) > self.R - self.L and size > 30:
                size -= 4   # adatta il testo alla larghezza utile
            f = font("DejaVuSans-Bold.ttf", size)
            col = th["accent"] if last else th["text"]
            off = (1 - ease_out(a)) * 24
            self.text_fade(d, (self.W // 2, ys[min(i, 2)] + off), line, f, col, a, "mm")
        return im

    # ---------- principale ----------
    def render_main(self, t):
        th, tl = self.th, self.tl
        im = self.base_main.copy()
        d = ImageDraw.Draw(im)
        # tag
        d.text((self.W // 2, th["tag_y"]), f'{self.ep["series"]}  ·  {self.ep["class"]}',
               font=font("DejaVuSans-Bold.ttf", 28), fill=th["muted"], anchor="mm")
        self.draw_caption(d, t)
        self.draw_code(d, t)
        if t >= tl.outro_t0:
            self.draw_cta(d, t)
        elif tl.chal_t0 is not None and tl.chal_t0 <= t < tl.run_t0:
            self.draw_countdown(d, t)
        else:
            self.draw_viz(d, t)
        self.draw_term(d, t)
        return im

    def current_event(self, t):
        cur = None
        for ev in self.tl.events:
            if ev["t"] <= t:
                cur = ev
        return cur

    def draw_caption(self, d, t):
        th, tl = self.th, self.tl
        fix, quiz = self.ep.get("fix"), self.ep.get("quiz")
        if t >= tl.outro_t0:
            text, t0 = self.ep["outro"]["caption"], tl.outro_t0
        elif tl.run2_t0 is not None and t >= tl.run2_t0:
            text, t0 = fix["run2_caption"], tl.run2_t0
        elif tl.fix_t0 is not None and t >= tl.fix_t0:
            text, t0 = fix["fix_caption"], tl.fix_t0
        elif t >= tl.run_t0:
            text, t0 = (fix["bug_caption"] if fix else self.ep["run_caption"]), tl.run_t0
        elif tl.chal_t0 is not None and t >= tl.chal_t0:
            text, t0 = (quiz["question"] if quiz else fix["find_caption"]), tl.chal_t0
        else:
            ev = self.current_event(t)
            if not ev:
                return
            text, t0 = ev["caption"], ev["t"]
        a = clamp((t - t0) / 0.25)
        f = font("DejaVuSans-Bold.ttf", th["caption_font"])
        maxw = self.R - self.L
        words, lines, cur = text.split(" "), [], ""
        for w in words:
            trial = (cur + " " + w).strip()
            if f.getlength(trial) <= maxw:
                cur = trial
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
        off = (1 - ease_out(a)) * 18
        for i, ln in enumerate(lines):
            self.text_fade(d, (self.W // 2 - 20, th["caption_y"] + i * 66 + off), ln, f, (255, 255, 255), a, "ma")

    def draw_code(self, d, t):
        th, tl = self.th, self.tl
        n = sum(1 for ct in tl.char_times if ct <= t)
        total = len(tl.code)
        if n < total:
            cur_line = bisect_right(tl.line_start, n) - 1
        else:
            cur_line = len(tl.lines) - 1
        ev = self.current_event(t)
        hl = set(ev.get("highlight_lines", [])) if (ev and t < tl.run_t0) else set()
        typing = t < tl.code_end and n < total
        x_code = self.L + 100
        y_top = th["ide_y0"] + 56 + 24
        f = font("DejaVuSansMono.ttf", th["code_font"])
        fn = font("DejaVuSansMono.ttf", th["code_font"] - 6)
        cf = tl.file_of[cur_line]
        review = False
        if tl.tabs:
            cf, review = tl.active_file(t)
            if review:
                cur_line = len(tl.lines) - 1
        if tl.tabs:
            self.draw_tabs(d, cf)
        for i, ln in enumerate(tl.lines):
            if i > cur_line:
                break
            if tl.file_of[i] != cf:
                continue
            ly = y_top + tl.local_no[i] * th["line_h"]
            tint = None
            if (i + 1) in hl or (typing and i == cur_line):
                tint = th["hl"]
            start = tl.line_start[i]
            fixing = tl.fix_t0 is not None and i == tl.fix_idx and t >= tl.fix_t0
            if fixing:
                ln, cols = tl.fix_new, self.fix_colors
                typed = sum(1 for ft in tl.fix_times if ft <= t)
                tint = th["hl_ok"]
            else:
                cols = self.colors[start:start + len(ln)]
                typed = max(0, min(len(ln), n - start))
                if tl.fix_t0 is not None and i == tl.fix_idx and tl.chal_t0 is not None and t >= tl.chal_t0:
                    tint = th["hl_bad"]
            if tint:
                d.rounded_rectangle((self.L + 12, ly - 3, self.R - 12, ly + th["line_h"] - 5), 8, fill=tint)
            d.text((self.L + 80, ly + 3), str(tl.local_no[i] + 1), font=fn, fill=th["muted"], anchor="ra")
            j = 0
            while j < typed:
                k = j
                col = cols[j]
                while k < typed and cols[k] == col:
                    k += 1
                seg = ln[j:k]
                if seg.strip():
                    d.text((x_code + j * self.cw, ly), seg, font=f, fill=col, anchor="la")
                j = k
        # cursore
        if not review and (t < tl.run_t0 and int(t * 2) % 2 == 0 or typing):
            col_i = (n - tl.line_start[cur_line]) if n < total else len(tl.lines[-1])
            cx = x_code + col_i * self.cw
            cy = y_top + tl.local_no[cur_line] * th["line_h"]
            d.rectangle((cx + 1, cy + 2, cx + 4, cy + th["line_h"] - 10), fill=th["accent2"])

    def draw_tabs(self, d, active):
        """Schede dei file: la scheda attiva e' evidenziata."""
        th = self.th
        y0 = th["ide_y0"]
        d.rectangle((self.L + 110, y0 + 4, self.R - 20, y0 + 56), fill=th["panel_bar"])
        f = font("DejaVuSansMono.ttf", 26)
        x = self.L + 130
        for i, name in enumerate(self.tl.tabs):
            w = f.getlength(name)
            if i == active:
                d.rounded_rectangle((x - 14, y0 + 8, x + w + 14, y0 + 52), 10, fill=th["panel"])
                d.text((x, y0 + 30), name, font=f, fill=th["accent2"], anchor="lm")
            else:
                d.text((x, y0 + 30), name, font=f, fill=th["muted"], anchor="lm")
            x += w + 44

    def draw_viz(self, d, t):
        th, tl = self.th, self.tl
        L, R = self.L, self.R
        d.text((L + 28, self.viz_y0 + 30), self.ep.get("viz_title", "voti  ·  vector<int>"),
               font=font("DejaVuSansMono.ttf", 28), fill=th["muted"], anchor="lm")
        vals, iter_info, label = [], None, None   # vals: [valore, t_comparsa, t_flash]
        for ev in tl.events:
            if ev["t"] > t:
                break
            v = ev.get("viz")
            if not v:
                continue
            op = v["op"]
            if op == "init":
                names = v.get("names") or [None] * len(v["values"])
                vals = [[x, ev["t"] + i * 0.12, ev["t"] + i * 0.12, names[i]] for i, x in enumerate(v["values"])]
            elif op == "push":
                vals.append([v["value"], ev["t"], ev["t"], v.get("name")])
            elif op == "set":
                vals[v.get("index", 0)][0] = v["value"]
                vals[v.get("index", 0)][2] = ev["t"]
                if "label" in v:
                    label = (v["label"], ev["t"])
            elif op == "iterate":
                iter_info = (ev["t"] + 0.3, v.get("count", len(vals)), v.get("labels"), v.get("var", "v"))
            elif op == "label":
                label = (v["text"], ev["t"])
            elif op == "size":
                label = (f"size() = {len(vals)}", ev["t"])
        if not vals:
            return
        m = tl.max_items
        slot = min(128, (R - L - 60) // m)
        bs = slot - 16
        x0 = (L + R) / 2 - (m * slot - 16) / 2
        cy = self.viz_y0 + 135
        cur = -1
        if iter_info:
            ts, cnt = iter_info[0], iter_info[1]
            k = int((t - ts) / th["iter_per_item"])
            if 0 <= k < cnt:
                cur = k
        for i, (val, ta, tf, nm) in enumerate(vals):
            p = clamp((t - ta) / 0.4)
            if p <= 0:
                continue
            sc = 0.5 + 0.5 * ease_out_back(p)
            cx = x0 + i * slot + bs / 2
            half = bs / 2 * sc
            flash = clamp(1 - (t - tf) / 0.8)
            fill = lerp(th["accent"], th["accent2"], flash)
            if i == cur:
                fill = th["good"]
            d.rounded_rectangle((cx - half, cy - half, cx + half, cy + half), 16, fill=fill)
            vfs = min(50, int(bs * 0.84 / (0.602 * max(1, len(str(val))))))
            d.text((cx, cy), str(val), font=font("DejaVuSansMono-Bold.ttf", max(12, int(vfs * sc))),
                   fill=(24, 24, 37), anchor="mm")
            if nm:
                d.text((cx, cy + bs / 2 + 26), nm, font=font("DejaVuSansMono.ttf", 26),
                       fill=th["text"], anchor="mm")
            elif self.ep.get("viz_index", True):
                d.text((cx, cy + bs / 2 + 26), f"[{i}]", font=font("DejaVuSansMono.ttf", 24),
                       fill=th["muted"], anchor="mm")
            if i == cur:
                d.polygon([(cx - 14, cy - bs / 2 - 26), (cx + 14, cy - bs / 2 - 26), (cx, cy - bs / 2 - 8)],
                          fill=th["good"])
        rf = font("DejaVuSansMono-Bold.ttf", 28)
        if cur >= 0:
            labels, var = iter_info[2], iter_info[3]
            txt = labels[cur] if labels else f"{var} = {vals[cur][0]}"
            d.text((R - 28, self.viz_y0 + 30), txt, font=rf, fill=th["good"], anchor="rm")
        elif label is not None:
            a = clamp((t - label[1]) / 0.3)
            self.text_fade_panel(d, (R - 28, self.viz_y0 + 30), label[0], rf, th["accent2"], a)

    def draw_countdown(self, d, t):
        th, tl = self.th, self.tl
        left = tl.chal_t0 + tl.chal_dur - t
        if left <= 0:
            return
        num = max(1, math.ceil(left))
        frac = 1 - (left - math.floor(left)) if left != math.floor(left) else 0
        size = int(150 - 30 * clamp(frac))
        cx, cy = (self.L + self.R) / 2, (self.viz_y0 + self.viz_y1) / 2
        d.text((cx, cy), str(num), font=font("DejaVuSansMono-Bold.ttf", size), fill=th["accent2"], anchor="mm")

    def text_fade_panel(self, d, xy, s, f, fill, a):
        d.text(xy, s, font=f, fill=lerp(self.th["panel_bar"], fill, clamp(a)), anchor="rm")

    def draw_cta(self, d, t):
        th, tl = self.th, self.tl
        a = clamp((t - tl.outro_t0) / 0.35)
        d.rounded_rectangle((self.L, self.viz_y0, self.R, self.viz_y1), 22,
                            fill=lerp(th["panel_bar"], th["accent"], a))
        col = lerp(th["accent"], (24, 24, 37), a)
        d.text(((self.L + self.R) / 2, (self.viz_y0 + self.viz_y1) / 2), self.ep["outro"]["cta"],
               font=font("DejaVuSans-Bold.ttf", 52), fill=col, anchor="mm")

    def draw_term(self, d, t):
        th, tl = self.th, self.tl
        run = None
        for r_ in tl.runs:
            if r_["t0"] <= t:
                run = r_
        if run is None:
            return
        f = font("DejaVuSansMono.ttf", th["term_font"])
        x = self.L + 28
        y = self.term_y0 + 56 + 22
        lh = th["term_font"] + 12
        n = sum(1 for ct in run["cmd_times"] if ct <= t)
        d.text((x, y), "$", font=f, fill=th["good"], anchor="la")
        d.text((x + 2 * f.getlength("M"), y), tl.cmd[:n], font=f, fill=th["text"], anchor="la")
        first_out = run["out_times"][0] if run["out_times"] else float("inf")
        if n < len(tl.cmd) or (t < first_out and int(t * 2) % 2 == 0):
            cx = x + (2 + n) * f.getlength("M")
            d.rectangle((cx, y + 3, cx + 14, y + th["term_font"] + 2), fill=th["text"])
        col = th["c_pre"] if run["bad"] else th["good"]
        for i, ot in enumerate(run["out_times"]):
            if ot <= t:
                d.text((x, y + lh * (i + 1)), run["lines"][i], font=f, fill=col, anchor="la")

    # ---------- frame ----------
    def frame(self, t):
        th = self.th
        if t < th["hook_seconds"]:
            return self.render_hook(t)
        a = (t - th["hook_seconds"]) / th["xfade"]
        main = self.render_main(t)
        if a < 1:
            return Image.blend(self.render_hook(th["hook_seconds"] - 0.001), main, clamp(a))
        return main


def encode_cmd(th, total, music, out):
    W, H, fps = th["width"], th["height"], th["fps"]
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{W}x{H}", "-r", str(fps), "-i", "-"]
    if music:
        cmd += ["-stream_loop", "-1", "-i", music]
    else:
        cmd += ["-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo"]
    cmd += ["-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "slow", "-crf", "14",
            "-vf", "scale=out_color_matrix=bt709:out_range=tv:flags=lanczos+accurate_rnd+full_chroma_int,format=yuv420p",
            "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv",
            "-profile:v", "high", "-r", str(fps), "-c:a", "aac", "-b:a", "192k"]
    if music:
        cmd += ["-af", f"afade=t=out:st={max(0, total - 1.5):.2f}:d=1.5"]
    cmd += ["-t", f"{total:.3f}", "-movflags", "+faststart", out]
    return cmd


def write_post(ep, out):
    """Scrive il .txt del post: italiano, poi inglese (se presente), poi hashtag."""
    post = ep.get("post")
    if not post:
        return
    parts = [post["caption"]]
    if post.get("theory"):
        parts.append("Richiamo teorico:\n" + "\n".join("- " + x for x in post["theory"]))
    if post.get("caption_en"):
        parts.append("English:\n" + post["caption_en"])
        if post.get("theory_en"):
            parts.append("Theory recap:\n" + "\n".join("- " + x for x in post["theory_en"]))
    parts.append(" ".join(post["hashtags"]))
    Path(out).with_suffix(".txt").write_text("\n\n".join(parts) + "\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode", nargs="?")
    ap.add_argument("--solo-testo", action="store_true", help="rigenera solo il .txt del post (senza video)")
    ap.add_argument("--check", action="store_true", help="verifica ambiente (ffmpeg, compilatore, font)")
    ap.add_argument("-o", "--out", default=None)
    ap.add_argument("--music", default=None, help="file audio opzionale (mp3/wav/m4a)")
    ap.add_argument("--set", action="append", default=[], help="override parametro, es. cps=22")
    ap.add_argument("--preview", default=None, help="tempi in secondi separati da virgola: salva PNG e basta")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if args.check:
        sys.exit(0 if check_env() else 1)
    if not args.episode:
        ap.error("indica il file episodio (oppure --check)")
    if not shutil.which("ffmpeg") and not args.preview:
        sys.exit("ffmpeg non trovato. Esegui: python3 render.py --check")

    ep = json.loads(Path(args.episode).read_text(encoding="utf-8"))
    if ep.get("files"):    # Java: una classe per file (schede nell'IDE)
        ep["code"] = "\n".join(f["code"].rstrip("\n") for f in ep["files"]) + "\n"
        ep["filename"] = ep["files"][0]["name"]
        ep.setdefault("theme", {})["cmd_display"] = "javac *.java && java " + ep.get("main_class", "Main")
    if args.solo_testo:
        write_post(ep, args.out or str(Path(args.episode).with_suffix(".mp4")))
        print("Testo del post rigenerato.")
        return
    th = build_theme(ep, args.set)
    fix = ep.get("fix")
    runs = []
    stdout, err = compile_and_run(ep["code"], ep["filename"], ep.get("files"), ep.get("main_class", "Main"))
    if stdout is None:
        if not fix and not ep.get("expect_error"):
            sys.exit("ERRORE di compilazione:\n" + "\n".join(err))
        runs.append({"lines": err, "bad": True})
        print("Il codice con il bug NON compila (errore reale):", err)
    else:
        runs.append({"lines": stdout.split("\n"), "bad": any(re.match(r"^[\w.]*(Exception|Error)\b", l) for l in stdout.split("\n"))})
        print("Codice compilato ed eseguito. Output reale:", repr(stdout))
    if fix:
        stdout, err = compile_and_run(apply_fix(ep["code"], fix), ep["filename"])
        if stdout is None:
            sys.exit("ERRORE: il codice corretto non compila:\n" + "\n".join(err))
        runs.append({"lines": stdout.split("\n")})
        print("Codice corretto, output reale:", repr(stdout))
    if "expected_output" in ep and stdout != ep["expected_output"]:
        sys.exit(f"Output diverso dall'atteso: {stdout!r}")

    tl = Timeline(ep, th, runs)
    for fi, rows, seen, need in tl.check_readable(th):
        print(f"ATTENZIONE: file {fi + 1} ({rows} righe) in vista {seen}s, ne servono almeno {need}s per leggerlo.")
    r = Renderer(ep, th, tl)
    print(f"Durata video: {tl.total:.1f}s")

    out = args.out or f"out/{ep['id']}.mp4"
    if args.preview:
        Path(out).mkdir(parents=True, exist_ok=True)
        for s in args.preview.split(","):
            r.frame(float(s)).save(Path(out) / f"preview_{float(s):05.1f}.png")
        return

    Path(out).parent.mkdir(parents=True, exist_ok=True)
    nframes = math.ceil(tl.total * th["fps"])
    p = subprocess.Popen(encode_cmd(th, tl.total, args.music, out), stdin=subprocess.PIPE)
    for i in range(nframes):
        p.stdin.write(r.frame(i / th["fps"]).tobytes())
        if i % 150 == 0:
            print(f"  frame {i}/{nframes}", flush=True)
    p.stdin.close()
    if p.wait() != 0:
        sys.exit("ffmpeg ha fallito")
    write_post(ep, out)
    print("OK ->", out)


if __name__ == "__main__":
    main()
