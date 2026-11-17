# Stato del progetto (aggiornare a fine sessione)

Ultimo aggiornamento: 2026-11-17 (primo blocco 3D prodotto: episodi 01-05)

## Fatto
- Pipeline di rendering funzionante (strumenti/render.py), stile della serie approvato dall'utente.
- I 4 episodi di prova della 3D sono stati azzerati il 2026-11-17 (recuperabili dallo storico git, commit 9a4c1d9).
- README di progetto scritto.
- Struttura cartelle creata su OneDrive e pubblicata nella repo GitHub Cyclope23/tiktokformat (sede principale).
- Compatibilita' multi-dispositivo: render.py portabile (font inclusi, compilatore e ffmpeg rilevati, --check).

- Ricevuti i programmi di 3D, 4D e 5D (piano-editoriale/).
- Piani dettagliati per classe scritti: 3D 35 episodi (4 fatti), 4D 28, 5D 27, con formati C/I/E/S (piano-editoriale/PIANO.md). Da validare con l'utente: scelta e ordine degli episodi.

- Layout: codice e terminale adattati automaticamente (piu' grandi); i 4 episodi 3D rigenerati.

- OneDrive sincronizzata il 2026-11-17 (PC fisso-daniele): renderer, CLAUDE.md, STATO.md, piani, episodi 01-05.

- Renderer esteso (2026-11-17): nomi sotto le caselle viz, formato I (quiz con conto alla rovescia), formato E (bug evidenziato, doppia esecuzione, errori reali del compilatore).
- Prodotto il primo blocco 3D (episodi/classe-3/): 01 variabili e costanti (B2), 02 tipi di dato (B3), 03 divisione intera e resto (B5), 04 quiz divisione (B7), 05 errore = / == (B8). Ognuno con .json, .mp4, .txt; fotogrammi controllati. Da pubblicare a mano (musica da scegliere in TikTok).

- Qualita' video alzata (2026-11-17): x264 preset slow, CRF 14, colori bt709 con conversione corretta, audio 192k; i 5 episodi 3D rigenerati (~0,7 MB ciascuno). Opzione futura: 60 fps.

- Ricerca orari di pubblicazione (2026-11-17): gli studi (Sprout, Buffer, Hootsuite) non concordano; proposta di piano a slot di test (mar/gio 15:30, dom 20:00 + 2 slot di prova) da verificare con TikTok Studio dopo 4 settimane. Piano scritto: piano-editoriale/PIANO-PUBBLICAZIONE.md, pubblicazione.json, calendario.csv (89 slot dal 2026-11-19, generato da strumenti/pianifica.py). Da validare con l'utente; automazione (promemoria/bozze TikTok) da fare.

- Descrizioni dei post bilingui IT + EN (2026-11-17): campi post.caption_en/theory_en, hashtag + #learntocode, render.py --solo-testo rigenera solo il .txt; aggiornati i 5 episodi 3D e il modello.
- Test pubblicazione (2026-11-17): TikTok Studio funziona sul profilo di Daniele; l'upload del file non e' automatizzabile da Claude (lo fa Daniele), descrizione e impostazioni si compilano da Chrome; Pubblica/Programma solo con ok esplicito. Episodio 01 caricato in Studio per prova e poi cancellato da Daniele (2026-11-17): non pubblicato, resta 'pronto' in calendario per giovedi' 19/11 15:30 (descrizione ora bilingue).

## Decisioni
- Argomenti dei primi episodi scelti da Claude (programmazione di classe non ancora disponibile).
- Nessuna voce, musica da decidere; account personale TikTok.
- Pubblicazione: via bozza (inbox TikTok) con rifinitura manuale; scelta tra app TikTok propria
  (API gratuita, registrazione sviluppatore) e scheduler esterno ancora aperta.
  L'account e' personale: la programmazione nativa di TikTok Studio non e' disponibile.

## Da fare
0. Validare il piano di pubblicazione; produrre in anticipo gli episodi dei prossimi slot (3D B1, B6, C1...).
1. Validare i piani con l'utente e scegliere il primo blocco di episodi da produrre per classe.
2. Estendere il renderer: formato S, input simulato (cin), Java (4D), SQL con SQLite (5D), grafiche nuove (diagrammi a blocchi, UML, E/R). Vedi PIANO.md.
3. Scegliere la musica (cartella musica/).
4. Decidere il metodo di pubblicazione e, se serve, preparare lo script di invio alla bozza TikTok.
5. Eventuale copia dei materiali nella repo del dipartimento (decisione aperta).
