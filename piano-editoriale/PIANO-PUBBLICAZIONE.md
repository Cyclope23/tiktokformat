# Piano di pubblicazione

Ultimo aggiornamento: 2026-11-17. Fuso: Europe/Rome. Pubblicazione manuale (profilo personale):
Daniele carica il video, sceglie la musica, incolla la descrizione dal `.txt`.

## Ritmo
1 video al giorno dal 19/11/2026, 30 settimane (207 slot). Le classi ruotano 3D, 4D, 5D (circa 2-3 video a settimana per classe).

## Slot fissi
| Giorno | Ora |
|--------|-----|
| Lunedi' | 15:30 |
| Martedi' | 15:30 |
| Mercoledi' | 15:30 |
| Giovedi' | 15:30 |
| Venerdi' | 15:30 |
| Sabato | 11:00 |
| Domenica | 20:00 |

## Test nelle prime 4 settimane
- Settimana 2: lunedi' 15:30 -> 13:00 (pausa pranzo)
- Settimana 3: mercoledi' 15:30 -> 19:30 (sera)
- Settimana 4: domenica 20:00 -> 09:00 (mattina)
A fine settimana 4 si confrontano visualizzazioni e completamento per fascia in TikTok Studio e si tengono gli slot migliori.

## Date bloccate
`pubblicazione.json` > `bloccati`: gli episodi gia' programmati su Buffer (01-05 della 3D) restano sulla loro data; pianifica.py assegna gli altri pronti agli slot liberi.

## Distribuzione dei contenuti
- Le classi ruotano slot dopo slot: 3D, 4D, 5D, 3D... Ogni classe ha 1 video a settimana.
- Dentro la classe si segue l'ordine del piano di classe (A, B, C...).
- Un episodio entra nel calendario solo se il renderer sa produrlo. Attivi C++ e Java (formati C, I, E); manca SQL (5D), quindi la 5D non entra ancora in calendario. Gli episodi che richiedono formato S, input `cin`, diagrammi, UML o E/R rientrano
  quando la funzione e' pronta (`funzioni_disponibili` in `pubblicazione.json`).
- I 5 episodi gia' pronti (01-05) occupano i primi 5 slot, poi si produce in anticipo di 1-2 settimane.

## Calendario e automazione
- `pubblicazione.json`: slot, test, classi, funzioni disponibili.
- `strumenti/pianifica.py`: genera `calendario.csv` (data, ora, classe, codice, titolo, episodio, stato).
  Rigenerare a ogni episodio prodotto o funzione aggiunta: `python3 strumenti/pianifica.py`.
- Passo successivo, automazione: dal calendario creare promemoria (Google Calendar) o bozze nella posta
  in arrivo di TikTok (API upload), con la descrizione dal `.txt`. Metodo ancora da scegliere.
