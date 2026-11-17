#!/usr/bin/env python3
"""Programma su Buffer (API GraphQL) gli episodi pronti del calendario.

Uso (dalla cartella del progetto, sul PC):
  python strumenti/buffer_pubblica.py --canali              # elenca i canali e il loro id
  python strumenti/buffer_pubblica.py --prossimi 3          # anteprima (nessun invio)
  python strumenti/buffer_pubblica.py --prossimi 3 --invia  # programma davvero

Parametri (nessun valore fisso nel codice):
  --chiave FILE    file con la chiave API (default: env.txt nella radice del progetto)
  --canale ID      id del canale TikTok (oppure variabile d'ambiente BUFFER_CANALE)
  --episodio ID    un episodio preciso (es. 01-variabili-costanti-cpp)
  --prossimi N     i prossimi N episodi "pronto" con data futura
  --invia          senza questo flag e' sempre un'anteprima

La chiave non viene mai stampata. Solo libreria standard di Python 3.9+.
"""
import argparse, csv, json, os, re, ssl, sys, urllib.request, urllib.error
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
API = "https://api.buffer.com"
TZ = ZoneInfo("Europe/Rome")
LIMITE_TESTO = 2200        # caratteri massimi della descrizione TikTok


def leggi_chiave(p):
    t = Path(p).read_text(encoding="utf-8").strip()
    if not t:
        sys.exit(f"File chiave vuoto o mancante: {p}")
    return re.sub(r"^[A-Za-z_]+\s*=\s*", "", t.splitlines()[0]).strip().strip("'\"")


def contesto_ssl():
    """Verifica TLS sempre attiva. Se c'e' certifi usa il suo archivio (evita le catene
    Let's Encrypt scadute nell'archivio di Windows), altrimenti quello di sistema."""
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


def gql(chiave, query, variabili=None):
    body = json.dumps({"query": query, "variables": variabili or {}}).encode()
    rq = urllib.request.Request(API, data=body, method="POST", headers={
        "Content-Type": "application/json", "Authorization": f"Bearer {chiave}"})
    try:
        with urllib.request.urlopen(rq, timeout=60, context=contesto_ssl()) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {"errors": [{"message": f"HTTP {e.code}: {e.read()[:300].decode(errors='replace')}"}]}
    except Exception as e:                                       # rete, proxy, DNS
        return {"errors": [{"message": f"{type(e).__name__}: {e}"}]}


def elenca_canali(chiave):
    r = gql(chiave, "{ account { organizations { id name } } }")
    if r.get("errors") or not r.get("data"):
        print("Errore:", r.get("errors")); return 1
    for org in r["data"]["account"]["organizations"]:
        c = gql(chiave, "query($o: OrganizationId!){ channels(input:{organizationId:$o}){ id name service } }",
                {"o": org["id"]})
        if c.get("errors"):
            print("Errore canali:", c["errors"]); continue
        for ch in c["data"]["channels"]:
            print(f'{ch["service"]:10} {ch["name"]:30} id={ch["id"]}')
    return 0


def episodi_pronti(args):
    righe = list(csv.DictReader((ROOT / "piano-editoriale/calendario.csv").open(encoding="utf-8")))
    ora = datetime.now(TZ)
    out = []
    for r in righe:
        if r["stato"] != "pronto" or not r["episodio"]:
            continue
        quando = datetime.fromisoformat(f'{r["data"]}T{r["ora"]}').replace(tzinfo=TZ)
        if args.episodio:
            if r["episodio"] == args.episodio:
                out.append((r, quando))
        elif quando > ora:
            out.append((r, quando))
    return out[: args.prossimi] if not args.episodio else out


def testo_post(r):
    cl = r["classe"][0]
    p = ROOT / f'episodi/classe-{cl}/{r["episodio"]}/{r["episodio"]}.txt'
    return p.read_text(encoding="utf-8").strip()


MUT = """mutation($i: CreatePostInput!){ createPost(input:$i){
  ... on PostActionSuccess { post { id status dueAt } }
  ... on MutationError { message } } }"""


def main():
    a = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument("--chiave", default=str(ROOT / "env.txt"))
    a.add_argument("--canale", default=os.environ.get("BUFFER_CANALE"))
    a.add_argument("--episodio")
    a.add_argument("--prossimi", type=int, default=1)
    a.add_argument("--canali", action="store_true")
    a.add_argument("--invia", action="store_true")
    args = a.parse_args()
    chiave = leggi_chiave(args.chiave)

    if args.canali:
        return elenca_canali(chiave)
    if not args.canale:
        print("Manca il canale: usa --canale ID (vedi --canali) o BUFFER_CANALE."); return 2

    lista = episodi_pronti(args)
    if not lista:
        print("Nessun episodio pronto da programmare."); return 0
    for r, quando in lista:
        testo = testo_post(r)
        url = r["video_url"]
        avvisi = []
        if len(testo) > LIMITE_TESTO:
            avvisi.append(f"descrizione di {len(testo)} caratteri (limite {LIMITE_TESTO})")
        print(f'\n{r["episodio"]}  ->  {quando:%a %d/%m/%Y %H:%M} ({quando.astimezone(timezone.utc):%H:%MZ})')
        print(f"   video: {url}\n   testo: {len(testo)} caratteri", *(f"\n   ATTENZIONE: {x}" for x in avvisi))
        if not args.invia:
            continue
        if avvisi:
            print("   saltato (correggi la descrizione)"); continue
        inp = {"text": testo, "channelId": args.canale, "schedulingType": "automatic",
               "mode": "customScheduled",
               "dueAt": quando.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
               "assets": {"videos": [{"url": url}]}}
        res = gql(chiave, MUT, {"i": inp})
        esito = (res.get("data") or {}).get("createPost")
        if res.get("errors") or not esito or "message" in esito:
            print("   ERRORE:", res.get("errors") or esito)
        else:
            print("   programmato:", esito["post"])
    if not args.invia:
        print("\nAnteprima: aggiungi --invia per programmare davvero.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
