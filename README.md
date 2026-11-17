# TikTok Format

Video didattici verticali (1080x1920, 20-30 secondi) che spiegano un concetto di programmazione
con codice reale: un IDE scuro in cui il codice si scrive da solo, una visualizzazione animata
(per esempio le caselle di un vettore) e il terminale con l'output vero del programma.
Pensati per i corsi di informatica della 3ª, 4ª e 5ª (IIS Rosselli, Aprilia) e per la
pubblicazione su TikTok.

## Come funziona

Ogni episodio è un file JSON (codice, passi, caption, richiamo teorico). Il renderer:

1. compila ed esegue davvero il codice, così l'output mostrato nel video è quello reale;
2. disegna i fotogrammi (Pillow) con evidenziazione della sintassi (Pygments);
3. li codifica con ffmpeg in H.264/AAC, pronti per TikTok, e genera la descrizione del post
   (riga di apertura, richiamo teorico, hashtag).

Nessuna voce: audio muto, la musica si sceglie nell'editor di TikTok alla pubblicazione
(oppure `--music brano.mp3`).

## Struttura

```
episodi/classe-N/NN-argomento-linguaggio/   .mp4 + .txt (descrizione) + .json (sorgente)
piano-editoriale/                           piano degli episodi per classe
musica/                                     brani della serie
strumenti/                                  render.py, modello episodio, font, requirements
CLAUDE.md                                   regole e stile del progetto (per Claude)
STATO.md                                    stato del lavoro, decisioni, passi aperti
```

Nomi in minuscolo con trattini e numero progressivo per classe, per esempio
`episodi/classe-3/05-argomento-cpp/`.

## Uso

```bash
pip install -r strumenti/requirements.txt
python3 strumenti/render.py --check            # verifica ffmpeg, compilatore, font
python3 strumenti/render.py episodi/classe-3/02-for-cpp/02-for-cpp.json -o out.mp4
```

Opzioni utili: `--music brano.mp3`, `--set cps=22` (velocità di battitura, e altri parametri di
tema), `--preview 5,10,20 -o cartella` (salva solo alcuni fotogrammi per controllare il layout).

Requisiti: Python 3, Pillow, Pygments, ffmpeg e un compilatore C++ (g++ o clang++).
I font DejaVu sono inclusi, quindi il risultato è identico su macOS, Windows e Linux.

## Nuovo episodio

1. Copia `strumenti/episodio-modello.json` in una nuova cartella episodio e compilalo.
2. Renderizza e controlla i fotogrammi con `--preview`.
3. Salva `.mp4`, `.txt` e `.json` nella cartella, poi aggiorna `STATO.md`.

Le operazioni di visualizzazione disponibili (`init`, `push`, `set`, `iterate`, `label`, `size`)
sono descritte in `CLAUDE.md`.

## Episodi

| Classe | # | Argomento |
|--------|---|-----------|
| 3D INF | 01 | `vector` in C++ |
| 3D INF | 02 | ciclo `for` |
| 3D INF | 03 | passaggio per valore e per riferimento |
| 3D INF | 04 | `while` e ricerca lineare nel vettore |

## Pubblicazione

Dal profilo personale, con controllo manuale: la bozza arriva nella posta in arrivo di TikTok
(API Content Posting, modalità upload) oppure si carica a mano. La pubblicazione diretta
pubblica via API richiede l'audit dell'app TikTok.

## Linguaggi

Il renderer oggi compila solo C++. Il supporto a Java e SQL (per 4ª e 5ª) è un passo aperto,
vedi `STATO.md`.
