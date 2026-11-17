#!/usr/bin/env python3
"""Controllo fotogrammi (passo obbligatorio dopo ogni render).

Uso: python3 strumenti/controlla.py <ep>.json [-o foglio.png] [-n 12]
Genera un foglio di fotogrammi equidistanti lungo tutto il video (hook, scrittura, schede,
viz, terminale, chiusura) da guardare prima di consegnare. Stampa durata e avvisi di leggibilita'.
"""
import argparse, subprocess, sys, tempfile
from pathlib import Path
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("episodio")
ap.add_argument("-o", "--out", default=None)
ap.add_argument("-n", type=int, default=12)
a = ap.parse_args()
ep = Path(a.episodio)
mp4 = ep.with_suffix(".mp4")
if not mp4.exists():
    sys.exit("Manca l'mp4: renderizza prima l'episodio.")
dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                     "-of", "csv=p=0", str(mp4)], text=True))
ts = ",".join(f"{dur * i / a.n + 0.3:.1f}" for i in range(a.n))
tmp = Path(tempfile.mkdtemp())
r = subprocess.run([sys.executable, str(Path(__file__).parent / "render.py"), str(ep), "--preview", ts,
                    "-o", str(tmp)], capture_output=True, text=True)
for l in (r.stdout + r.stderr).splitlines():
    if "ATTENZIONE" in l or "Traceback" in l or "ERRORE" in l:
        print(l)
fs = sorted(tmp.glob("*.png"), key=lambda f: float(f.stem.split("_")[-1]))
cols = 6
W = Image.new("RGB", (270 * cols, 480 * ((len(fs) + cols - 1) // cols)))
for i, f in enumerate(fs):
    W.paste(Image.open(f).crop((0, 100, 1080, 1750)).resize((270, 413)), (270 * (i % cols), 480 * (i // cols)))
out = Path(a.out) if a.out else Path(tempfile.gettempdir()) / f"controllo-{ep.stem}.png"
W.save(out)
print(f"Durata {dur:.1f}s - foglio: {out}")
