#!/usr/bin/env python3
"""Formato "A" (AI Adoption): video a scene di tipo diverso, stesso stile e stesse zone sicure della serie.

Si usa tramite render.py (che delega qui quando l'episodio ha "format": "A"):
  python3 strumenti/render.py episodi/ai-adoption/<ep>/<ep>.json -o <ep>.mp4
  python3 strumenti/render.py <ep>.json --preview 5,12,20 -o cartella

Tipi di scena ("kind"):
  chat    una chat singola a tutto schermo (messaggi user/ai, badge finale opzionale)
  versus  due chat impilate: la prima (di solito "sbagliato") poi la seconda ("giusto")
  rule    la regola finale, parola per parola
Nei testi, **parola** evidenzia la parola (grassetto + colore).
Le risposte dell'AI sono output reali registrati al momento della produzione:
l'episodio riporta "tool", "model" e "registrato" (data), e il post cita lo strumento.
"""
import math
import re
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
import render as R   # noqa: E402
from render import clamp, ease_out, ease_out_back, font, lerp   # noqa: E402

CHAT_DEFAULTS = dict(
    bubble_font=34, user_cps=26.0, ai_cps=46.0, dots_seconds=0.9, read_wps=3.4,
    msg_gap=0.45, scene_pad=0.5, scene_xfade=0.35, badge_hold=1.6, rule_hold=2.4,
    bad=(243, 139, 168), good=(166, 227, 161), bubble_ai=(49, 50, 68),
    panel_y0=330, panel_y1=1630, versus_h=630, versus_y0=300, versus_gap=30,
)
MONO, MONO_B, SANS_B = "DejaVuSansMono.ttf", "DejaVuSansMono-Bold.ttf", "DejaVuSans-Bold.ttf"


def words_of(text):
    """'ciao **mondo**' -> [('ciao', False), ('mondo', True)]; '\\n' diventa ('\\n', False)."""
    out = []
    for i, seg in enumerate(re.split(r"\*\*", text)):
        for part in re.split(r"(\n)", seg):
            if part == "\n":
                out.append(("\n", False))
            else:
                lead = len(part) - len(part.lstrip(" "))
                if lead >= 2 and (not out or out[-1][0] == "\n"):   # indentazione del codice
                    out.append(("\u00a0" * (lead - 1), False))
                out += [(w, i % 2 == 1) for w in part.split(" ") if w]
    return out


def wrap(words, maxw, size):
    """Greedy: ritorna righe [[(word, bold, x, start_char)]] e il numero totale di caratteri."""
    fm = font(MONO, size)
    cw = fm.getlength("M")
    lines, cur, x, chars = [], [], 0.0, 0
    for w, b in words:
        if w == "\n":
            lines.append(cur)
            cur, x = [], 0.0
            chars += 1
            continue
        wl = len(w) * cw
        if cur and x + wl > maxw:
            lines.append(cur)
            cur, x = [], 0.0
        cur.append((w, b, x, chars))
        x += wl + cw
        chars += len(w) + 1
    if cur:
        lines.append(cur)
    return lines, chars


class Chat:
    """Una chat in un pannello: calcola layout e tempi dei messaggi."""

    def __init__(self, th, spec, x0, y0, x1, y1):
        self.th, self.spec = th, spec
        self.x0, self.y0, self.x1, self.y1 = x0, y0, x1, y1
        self.bar = 64
        self.view_h = (y1 - y0) - self.bar - 16
        size = th["bubble_font"]
        self.size, self.lh = size, round(size * 1.42)
        self.maxw = int((x1 - x0) * 0.80) - 52
        self.cw = font(MONO, size).getlength("M")
        self.msgs = []
        y = 22
        for m in spec["messages"]:
            lines, nch = wrap(words_of(m["text"]), self.maxw, size)
            w = max((l[-1][2] + len(l[-1][0]) * self.cw for l in lines if l), default=60)
            h = len(lines) * self.lh + 34
            self.msgs.append(dict(role=m["role"], lines=lines, nch=nch, w=int(w) + 52, h=h, y=y,
                                  nwords=sum(len(l) for l in lines)))
            y += h + 22
        self.content_h = y

    def schedule(self, t0):
        """Assegna i tempi (locali alla scena); ritorna il tempo di fine."""
        th = self.th
        t = t0
        for m in self.msgs:
            m["t"] = t
            if m["role"] == "user":
                m["dots"], m["typ"] = 0.0, m["nch"] / th["user_cps"] + 0.25
                t += m["typ"] + max(th["msg_gap"], m["nwords"] / th["read_wps"] - m["typ"])   # tempo per leggere
            else:
                m["dots"], m["typ"] = th["dots_seconds"], m["nch"] / th["ai_cps"]
                t += m["dots"] + m["typ"] + max(1.0, m["nwords"] / th["read_wps"])
        self.t_end_msgs = t
        b = self.spec.get("badge")
        self.badge_t = t if b else None
        if b:
            t += th["badge_hold"]
        self.t_end = t
        # scroll: ogni messaggio porta la sua base in vista
        need, prev = [], 0.0
        for m in self.msgs:
            prev = max(prev, m["y"] + m["h"] + 22 - self.view_h)
            need.append(prev)
        self.need = need
        return t

    def scroll(self, t):
        s, prev = 0.0, 0.0
        for m, n in zip(self.msgs, self.need):
            if m["t"] <= t:
                s = lerp((prev,), (n,), ease_out(clamp((t - m["t"]) / 0.45)))[0]
            prev = n
        return s

    def draw(self, im, t, rend):
        th = self.th
        d = ImageDraw.Draw(im)
        tone = self.spec.get("tone")
        d.rounded_rectangle((self.x0, self.y0, self.x1, self.y1), 22, fill=th["panel"])
        d.rounded_rectangle((self.x0, self.y0, self.x1, self.y0 + self.bar), 22, fill=th["panel_bar"])
        d.rectangle((self.x0, self.y0 + 40, self.x1, self.y0 + self.bar), fill=th["panel_bar"])
        col = th.get(tone, th["accent"]) if tone else th["muted"]
        d.text((self.x0 + 28, self.y0 + self.bar // 2), self.spec.get("title", ""),
               font=font(SANS_B, 30), fill=col, anchor="lm")
        d.text((self.x1 - 28, self.y0 + self.bar // 2), "✦ AI", font=font(SANS_B, 26),
               fill=th["muted"], anchor="rm")
        vw, vh = self.x1 - self.x0, self.view_h
        view = Image.new("RGB", (vw, vh), th["panel"])
        vd = ImageDraw.Draw(view)
        sc = self.scroll(t)
        f, fb = font(MONO, self.size), font(MONO_B, self.size)
        for m in self.msgs:
            if m["t"] > t:
                break
            top = m["y"] - sc
            user = m["role"] == "user"
            lt = t - m["t"]
            if not user and lt < m["dots"]:   # tre puntini che pulsano
                bx0 = 24
                vd.rounded_rectangle((bx0, top, bx0 + 150, top + 66), 30, fill=th["bubble_ai"])
                for i in range(3):
                    k = 0.5 + 0.5 * math.sin(lt * 9 - i * 0.9)
                    r = 7 + 3 * k
                    vd.ellipse((bx0 + 44 + i * 31 - r, top + 33 - r, bx0 + 44 + i * 31 + r, top + 33 + r),
                               fill=lerp(th["muted"], th["text"], k))
                continue
            shown = int(max(0.0, lt - m["dots"]) * (th["user_cps"] if user else th["ai_cps"]))
            bx0 = vw - 24 - m["w"] if user else 24
            pop = clamp(lt - m["dots"] + 0.15) / 0.15 if not user else clamp(lt / 0.15)
            dy = (1 - ease_out(clamp(pop))) * 16
            fill = th["accent"] if user else th["bubble_ai"]
            vd.rounded_rectangle((bx0, top + dy, bx0 + m["w"], top + dy + m["h"]), 30, fill=fill)
            ink = (24, 24, 37) if user else th["text"]
            for li, ln in enumerate(m["lines"]):
                for w, b, x, c0 in ln:
                    n = min(len(w), shown - c0)
                    if n <= 0:
                        continue
                    colr = (24, 24, 37) if user else (th["accent2"] if b else ink)
                    vd.text((bx0 + 26 + x, top + dy + 17 + li * self.lh), w[:n],
                            font=fb if b else f, fill=colr)
        im.paste(view, (self.x0, self.y0 + self.bar))
        b = self.spec.get("badge")
        if b and self.badge_t is not None and t >= self.badge_t:
            rend.draw_badge(im, b, t - self.badge_t, self.x1 - 14, self.y0 + self.bar // 2)


class ChatRenderer:
    def __init__(self, ep, th):
        self.ep, self.th = ep, th
        self.W, self.H = th["width"], th["height"]
        self.L, self.R = th["margin_l"], self.W - th["margin_r"]
        self.bg = R.Renderer._gradient(self)
        self.scenes = []
        t = th["hook_seconds"]
        for sc in ep["scenes"]:
            s = dict(sc)
            s["t0"] = t
            kind = sc["kind"]
            if kind == "rule":
                words = words_of(sc["text"])
                s["words"] = words
                s["dur"] = 0.6 + len(words) * 0.2 + th["rule_hold"]
            else:
                panels = sc["panels"] if kind == "versus" else [sc]
                s["chats"], tl = [], 0.4
                hs = sc.get("heights") or [th["versus_h"]] * len(panels)   # altezze dei pannelli (px)
                y0 = th["versus_y0"]
                for i, p in enumerate(panels):
                    if kind == "versus":
                        c = Chat(th, p, self.L, y0, self.R, y0 + hs[i])
                        y0 += hs[i] + th["versus_gap"]
                    else:
                        c = Chat(th, sc, self.L, th["panel_y0"], self.R, th["panel_y1"])
                    c.appear = tl
                    tl = c.schedule(tl + 0.3) + 0.3
                    s["chats"].append(c)
                s["dur"] = tl + th["scene_pad"]
            t += s["dur"]
            self.scenes.append(s)
        self.outro_t0 = t
        self.total = t + th["outro_seconds"]

    text_fade = R.Renderer.text_fade

    # ----- elementi comuni -----
    def top_overlay(self, d, t, caption):
        th = self.th
        d.text((self.W // 2, th["tag_y"]), f'{self.ep["series"]}  ·  {self.ep["class"]}',
               font=font(SANS_B, 28), fill=th["muted"], anchor="mm")
        d.rounded_rectangle((self.L, 186, self.R, 192), 3, fill=th["panel_bar"])
        d.rounded_rectangle((self.L, 186, self.L + (self.R - self.L) * clamp(t / self.total), 192), 3, fill=th["accent"])
        if caption:
            size = th["caption_font"]
            while font(SANS_B, size).getlength(caption) > self.R - self.L and size > 30:
                size -= 2
            d.text((self.W // 2, th["caption_y"] + 40), caption, font=font(SANS_B, size), fill=th["text"], anchor="mm")

    def draw_badge(self, im, b, lt, right, cy):   # right = bordo destro del badge
        th = self.th
        col = th.get(b.get("tone", "good"), th["good"])
        txt = b["text"]
        f = font(SANS_B, 40)
        w, h = int(f.getlength(txt)) + 56, 74
        lay = Image.new("RGBA", (w + 8, h + 8), (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        ld.rounded_rectangle((4, 4, w + 4, h + 4), 18, fill=(*lerp(th["panel_bar"], (0, 0, 0), 0.3), 255), outline=col, width=5)
        ld.text(((w + 8) // 2, (h + 8) // 2), txt, font=f, fill=col, anchor="mm")
        k = clamp(lt / 0.45)
        s = 0.3 + 0.7 * ease_out_back(k)
        lay = lay.rotate(-5, expand=True, resample=Image.BICUBIC)
        lay = lay.resize((max(1, int(lay.width * s)), max(1, int(lay.height * s))), Image.BICUBIC)
        lay.putalpha(lay.getchannel("A").point(lambda v: int(v * clamp(k * 2))))
        im.paste(lay, (int(right - lay.width), int(cy - lay.height / 2)), lay)

    # ----- scene -----
    def hook(self, t):
        return R.Renderer.render_hook(self, t)

    def scene_frame(self, s, lt):
        th = self.th
        im = self.bg.copy()
        d = ImageDraw.Draw(im)
        if s["kind"] == "rule":
            self.top_overlay(d, s["t0"] + lt, "")
            d.text((self.W // 2, 640), "LA REGOLA", font=font(SANS_B, 40), fill=th["muted"], anchor="mm")
            size, y = 84, 780
            lines, cur, wd = [], [], 0
            f = font(SANS_B, size)
            sp = f.getlength(" ")
            for i, (w, b) in enumerate(s["words"]):
                wl = f.getlength(w)
                if cur and wd + wl > self.R - self.L - 40:
                    lines.append(cur)
                    cur, wd = [], 0
                cur.append((i, w, b, wd))
                wd += wl + sp
            lines.append(cur)
            for ln in lines:
                total = ln[-1][3] + f.getlength(ln[-1][1])
                for i, w, b, x in ln:
                    a = clamp((lt - 0.4 - i * 0.2) / 0.3)
                    if a <= 0:
                        continue
                    pos = (self.W // 2 - total / 2 + x, y + (1 - ease_out(a)) * 22)
                    col = lerp(self.bg_at(y), th["accent2"] if b else th["text"], a)
                    d.text(pos, w, font=f, fill=col, anchor="lm")
                y += 118
            return im
        self.top_overlay(d, s["t0"] + lt, s.get("caption", ""))
        for c in s["chats"]:
            if lt >= c.appear:
                a = clamp((lt - c.appear) / 0.3)
                if a < 1:   # ingresso: scivola dal basso
                    sub = Image.new("RGB", im.size, (0, 0, 0))
                    sub.paste(self.bg, (0, 0))
                    c.draw(sub, lt, self)
                    box = (c.x0 - 2, c.y0 - 2, c.x1 + 2, c.y1 + 2)
                    part = sub.crop(box)
                    im.paste(Image.blend(im.crop(box), part, ease_out(a)), box[:2])
                else:
                    c.draw(im, lt, self)
        return im

    def bg_at(self, y):
        return lerp(self.th["bg_top"], self.th["bg_bottom"], y / self.H)

    def outro(self, lt):
        th = self.th
        im = self.bg.copy()
        d = ImageDraw.Draw(im)
        self.top_overlay(d, self.outro_t0 + lt, "")
        o = self.ep["outro"]
        a = clamp(lt / 0.4)
        f = font(SANS_B, 72)
        txt = o["cta"]
        while f.getlength(txt) > self.R - self.L and f.size > 30:
            f = font(SANS_B, f.size - 4)
        d.text((self.W // 2, 860 + (1 - ease_out(a)) * 30), txt, font=f,
               fill=lerp(self.bg_at(860), th["accent"], a), anchor="mm")
        a2 = clamp((lt - 0.5) / 0.4)
        size = 44
        while font(SANS_B, size).getlength(o["caption"]) > self.R - self.L and size > 26:
            size -= 2
        d.text((self.W // 2, 1000), o["caption"], font=font(SANS_B, size),
               fill=lerp(self.bg_at(1000), th["text"], a2), anchor="mm")
        return im

    def frame(self, t):
        th = self.th
        if t < th["hook_seconds"]:
            return self.hook(t)
        if t >= self.outro_t0:
            return self.outro(t - self.outro_t0)
        for i, s in enumerate(self.scenes):
            if s["t0"] <= t < s["t0"] + s["dur"]:
                lt = t - s["t0"]
                im = self.scene_frame(s, lt)
                left = s["dur"] - lt
                xf = th["scene_xfade"]
                if left < xf:
                    nxt = self.scenes[i + 1] if i + 1 < len(self.scenes) else None
                    other = self.scene_frame(nxt, 0.0) if nxt else self.outro(0.0)
                    im = Image.blend(im, other, ease_out(1 - left / xf))
                return im
        return self.outro(t - self.outro_t0)


def run(ep, args):
    th = R.build_theme(ep, args.set)
    for k, v in CHAT_DEFAULTS.items():
        th.setdefault(k, v)
        if k not in ep.get("theme", {}) and not any(s.startswith(k + "=") for s in args.set):
            th[k] = v
    rend = ChatRenderer(ep, th)
    print(f"Durata video: {rend.total:.1f}s ({len(rend.scenes)} scene)")
    out = args.out or f"out/{ep['id']}.mp4"
    if args.preview:
        Path(out).mkdir(parents=True, exist_ok=True)
        for s in args.preview.split(","):
            rend.frame(float(s)).save(Path(out) / f"preview_{float(s):05.1f}.png")
        return
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    nframes = math.ceil(rend.total * th["fps"])
    p = subprocess.Popen(R.encode_cmd(th, rend.total, args.music, out), stdin=subprocess.PIPE)
    for i in range(nframes):
        p.stdin.write(rend.frame(i / th["fps"]).tobytes())
        if i % 150 == 0:
            print(f"  frame {i}/{nframes}", flush=True)
    p.stdin.close()
    if p.wait() != 0:
        sys.exit("ffmpeg ha fallito")
    R.write_post(ep, out)
    print("OK ->", out)
