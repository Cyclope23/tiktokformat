#!/usr/bin/env python3
"""Genera piano-editoriale/calendario.csv dagli slot di pubblicazione e dai piani di classe.

Uso: python3 strumenti/pianifica.py
Legge piano-editoriale/pubblicazione.json e piano-editoriale/<classe>/piano-<classe>INF.md.
Le classi ruotano slot dopo slot (3D, 4D, 5D, ...). Di ogni classe si prende il prossimo episodio
del piano NON ancora fatto e con tutte le funzioni del renderer disponibili (config
"funzioni_disponibili"); gli altri restano in coda e rientrano quando la funzione viene aggiunta.
Gli episodi gia' fatti compaiono con stato "fatto" e non occupano slot.
"""
import csv, json, re
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PE = ROOT / "piano-editoriale"
GIORNI = ["lun", "mar", "mer", "gio", "ven", "sab", "dom"]


def requisiti(classe, codice, tipo):
    r = []
    if classe == "3D":
        r.append("cpp")
        if codice.startswith("A"):
            r.append("grafica-diagramma")
        if codice == "B4":
            r.append("cin")
    elif classe == "4D":
        r.append("java")
        if codice.startswith("A"):
            r.append("uml")
    else:
        r.append("sql")
        if codice.startswith("A"):
            r.append("er")
    r.append(tipo)
    return r


def leggi_piano(classe):
    p = PE / f"{classe}INF" / f"piano-{classe}INF.md"
    righe = []
    for ln in p.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\|\s*([A-Z]\d+)\s*\|\s*([CIES])\s*\|\s*(.+?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*$", ln)
        if m:
            cod, tipo, titolo, _, stato = m.groups()
            ep = ""
            fm = re.match(r"fatto \((\d+)\)", stato)
            if fm:
                d = sorted((ROOT / "episodi" / f"classe-{classe[0]}").glob(f"{fm.group(1)}-*"))
                ep = d[0].name if d else fm.group(1)
            righe.append(dict(classe=classe, codice=cod, tipo=tipo, titolo=titolo.replace("`", ""),
                              fatto=stato.startswith("fatto"), episodio=ep,
                              req=requisiti(classe, cod, tipo)))
    return righe


def slot_con_varianti(cfg, settimana, giorno, ora):
    for v in cfg.get("slot_di_prova", []):
        if v["settimana"] == settimana and v["da"] == f"{giorno} {ora}":
            g, o = v["a"].split()
            return g, o, "prova"
    return giorno, ora, "fisso"


def main():
    cfg = json.loads((PE / "pubblicazione.json").read_text(encoding="utf-8"))
    inizio = date.fromisoformat(cfg["inizio"])
    lunedi0 = inizio - timedelta(days=inizio.weekday())
    disp = set(cfg["funzioni_disponibili"])
    code = {c: [r for r in leggi_piano(c) if not r["fatto"]] for c in cfg["classi"]}
    done = [r for c in cfg["classi"] for r in leggi_piano(c) if r["fatto"]]
    attive = [c for c in cfg["classi"]
              if any(set(r["req"]) <= disp for r in code[c])]
    pronti = sorted(done, key=lambda r: (r["classe"], r["episodio"]))   # gia' prodotti: vanno per primi
    rows, rot = [], 0
    for w in range(1, cfg["settimane"] + 1):
        for s in cfg["slot_settimanali"]:
            g, o, kind = slot_con_varianti(cfg, w, s["giorno"], s["ora"])
            d = lunedi0 + timedelta(weeks=w - 1, days=GIORNI.index(g))
            if d < inizio:
                continue
            ep = None
            if pronti:
                ep = pronti.pop(0)
                rows.append([d.isoformat(), o, g, kind, w, ep["classe"], ep["codice"], ep["tipo"],
                             ep["titolo"], ep["episodio"], "pronto"])
                continue
            for _ in range(len(cfg["classi"])):
                c = cfg["classi"][rot % len(cfg["classi"])]
                rot += 1
                for i, r in enumerate(code[c]):
                    if set(r["req"]) <= disp:
                        ep = code[c].pop(i)
                        break
                if ep:
                    break
            rows.append([d.isoformat(), o, g, kind, w,
                         ep["classe"] if ep else "", ep["codice"] if ep else "",
                         ep["tipo"] if ep else "", ep["titolo"] if ep else "(slot libero: serve il renderer Java/SQL o nuovi episodi)",
                         "", "da produrre" if ep else "libero"])
    out = PE / "calendario.csv"
    with out.open("w", newline="", encoding="utf-8") as f:
        w_ = csv.writer(f)
        w_.writerow(["data", "ora", "giorno", "slot", "settimana", "classe", "codice", "formato",
                     "titolo", "episodio", "stato"])
        w_.writerows(rows)
    print(f"{len(rows)} slot -> {out}")
    print("Episodi gia' prodotti:", len(done), "| classi attive:", attive)


if __name__ == "__main__":
    main()
