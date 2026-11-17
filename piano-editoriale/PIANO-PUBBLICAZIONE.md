# Piano di pubblicazione

Ultimo aggiornamento: 2026-11-17. Fuso: Europe/Rome. Pubblicazione manuale (profilo personale):
Daniele carica il video, sceglie la musica, incolla la descrizione dal `.txt`.

## Ritmo
3 video a settimana, circa 30 settimane (fino a giugno 2027), per i 90 episodi dei tre piani (3D 35, 4D 28, 5D 27).

## Slot fissi (dopo scuola e sera, dove si concentrano gli studenti)
| Giorno | Ora | Nota |
|--------|-----|------|
| Martedi' | 15:30 | pomeriggio infrasettimanale |
| Giovedi' | 15:30 | pomeriggio infrasettimanale |
| Domenica | 20:00 | sera prima della settimana di scuola |

## Test nelle prime 4 settimane
Gli studi (Sprout, Buffer, Hootsuite) non concordano, quindi si sposta uno slot per volta:
- Settimana 2: martedi' 15:30 -> lunedi' 13:00 (pausa pranzo)
- Settimana 3: giovedi' 15:30 -> mercoledi' 19:30 (sera)
- Settimana 4: domenica 20:00 -> domenica 09:00 (mattina)

A fine settimana 4 si confrontano visualizzazioni e completamento per fascia in TikTok Studio e si tengono
i 2-3 slot migliori (si modifica `pubblicazione.json` e si rigenera il calendario).

## Distribuzione dei contenuti
- Le classi ruotano slot dopo slot: 3D, 4D, 5D, 3D... Ogni classe ha 1 video a settimana.
- Dentro la classe si segue l'ordine del piano di classe (A, B, C...).
- Un episodio entra nel calendario solo se il renderer sa produrlo. Oggi e' attivo solo il C++
  (formati C, I, E): finche' non ci sono Java (4D) e SQL (5D) tutti gli slot vanno alla 3D, e dalla settimana 9
  restano slot liberi. Gli episodi che richiedono formato S, input `cin`, diagrammi, UML o E/R rientrano
  quando la funzione e' pronta (`funzioni_disponibili` in `pubblicazione.json`).
- I 5 episodi gia' pronti (01-05) occupano i primi 5 slot, poi si produce in anticipo di 1-2 settimane.

## Calendario e automazione
- `pubblicazione.json`: slot, test, classi, funzioni disponibili.
- `strumenti/pianifica.py`: genera `calendario.csv` (data, ora, classe, codice, titolo, episodio, stato).
  Rigenerare a ogni episodio prodotto o funzione aggiunta: `python3 strumenti/pianifica.py`.
- Passo successivo, automazione: dal calendario creare promemoria (Google Calendar) o bozze nella posta
  in arrivo di TikTok (API upload), con la descrizione dal `.txt`. Metodo ancora da scegliere.
