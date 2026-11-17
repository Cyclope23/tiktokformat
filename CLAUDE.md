# Progetto TikTok didattico (Daniele Palma)

Video verticali (1080x1920) che spiegano concetti di programmazione con codice reale,
legati ai programmi di 3D, 4D e 5D INF (IIS Rosselli, Aprilia). Pubblicazione sul
profilo personale di Daniele. Lingua: italiano. Tono: conciso, diretto.

Sede principale: repository GitHub Cyclope23/tiktokformat (privata, branch main).
Copia di lavoro locale sincronizzata: OneDrive-Personale/001 - Lavoro/005-Personal/tiktokformat
(senza .git, per non far sincronizzare la cartella .git a OneDrive).
Allineamento: a fine sessione i file nuovi o modificati vanno committati e spinti su main nella
repo, e riportati nella cartella OneDrive (o viceversa se si e' lavorato li'). Non creare altre copie.

## REGOLA OBBLIGATORIA: aggiornare STATO.md
Dopo ogni lavoro svolto (nuovo episodio, decisione, modifica agli strumenti, passo completato)
e comunque prima di chiudere la sessione, aggiorna STATO.md: data, cosa e' stato fatto,
decisioni prese, passi aperti. Non aspettare che l'utente lo chieda e non concludere la
sessione senza averlo fatto. Se il lavoro e' avvenuto fuori da questa cartella (chat telefono/web),
annota in STATO.md i file da archiviare.
Aggiorna STATO.md e fai push nella stessa sessione, cosi' repo e OneDrive restano allineate.

## Come riprendere il lavoro
1. Leggi STATO.md: cosa e' fatto, decisioni prese, prossimi passi.
2. Leggi piano-editoriale/ per l'elenco degli episodi pianificati.
3. A fine sessione aggiorna STATO.md (episodi creati, decisioni, passi aperti).

## Struttura
- episodi/classe-N/NN-argomento-linguaggio/ -> NN-argomento-linguaggio.mp4 | .txt | .json
- piano-editoriale/ -> piano episodi per classe (da creare dalla programmazione didattica)
- musica/ -> brani scelti per la serie
- strumenti/render.py -> renderer; strumenti/episodio-modello.json -> modello da copiare

Nomi: tutto minuscolo, trattini, nessun underscore, numero progressivo per classe
(il prossimo episodio della 3ª e' 05-...). Le cartelle episodio contengono sempre i tre file.

## Creare un episodio
1. Copia strumenti/episodio-modello.json nella nuova cartella episodio e compilalo.
2. Renderizza: python3 strumenti/render.py <ep>.json -o <ep>.mp4 [--music brano.mp3] [--set cps=22]
   Anteprima fotogrammi: --preview 5,10,20 -o <cartella>
3. Il renderer compila ed esegue davvero il codice (g++ -std=c++17): l'output nel terminale
   del video e' quello reale. Se non compila, il rendering si ferma.
4. Controlla i fotogrammi (testo non tagliato, righe non fuori dal pannello) prima di consegnare.
5. Salva .mp4, .txt (generato dal renderer) e .json nella cartella episodio.

## Compatibilita' tra dispositivi
Prima di renderizzare su una macchina nuova: python3 strumenti/render.py --check
(controlla ffmpeg, compilatore C++, font, Pillow/Pygments). Installazione librerie:
pip install -r strumenti/requirements.txt
- I font DejaVu sono inclusi in strumenti/fonts/: il video e' identico su ogni sistema.
- Compilatore: g++, clang++ o c++ (rilevato in automatico). macOS: xcode-select --install.
  Windows: MinGW/MSYS2 (g++) nel PATH. ffmpeg nel PATH (macOS: brew install ffmpeg).
- Percorsi e file di testo gestiti in modo portabile (UTF-8, pathlib).
Dove lavorare:
- Computer con app desktop e cartella collegata: rendering in locale o nel container cloud;
  i file finiscono direttamente in questa cartella (OneDrive sincronizza).
- Chat da telefono o web (senza cartella collegata): Claude renderizza nel container cloud e
  invia i file in chat. Vanno poi messi a mano nella cartella episodio, oppure riportati nella
  prossima sessione desktop. In quel caso annotare in STATO.md gli episodi da archiviare.
- Repo: i video (~0,5 MB ciascuno) sono versionati insieme al resto; con molti episodi valutare Git LFS.

## Stile fisso della serie (non cambiare senza chiedere)
- Hook di 3 righe nei primi 3 secondi, poi simulazione IDE scuro: il codice si scrive da solo,
  pannello con visualizzazione (caselle del vettore o variabile), terminale con output reale.
- Caption numerate in alto ("1 · ..."), chiusura con CTA "Segui per la serie C++" e annuncio
  del prossimo episodio. Durata 20-30 s. Dimensione di codice e terminale automatica (la piu' grande che entra: codice max 44, terminale max 40). Margini: nessun testo a destra (120 px),
  in alto e in basso (zone coperte dall'interfaccia TikTok).
- Nessuna voce. Audio muto o musica; la musica si sceglie nell'editor di TikTok alla pubblicazione.
- Un concetto per episodio; esempi reali, brevi (10-14 righe).

## Operazioni "viz" disponibili nel JSON
init (values) | push (value) | set (index, value, label) | iterate (count, labels, var) |
label (text) | size. Ogni step: after_line, caption, viz, highlight_lines.
Opzioni episodio: theme (override parametri), viz_title, viz_index (true/false).

## Descrizione del post (file .txt)
Riga di apertura + "Richiamo teorico" (3-4 punti brevi, corretti) + hashtag.
Hashtag base: #cpp #programmazione #coding #imparareacodare #informatica #scuola #learnontiktok
(adattare per Java, SQL, Sistemi e Reti).

## Regole
- Account: profilo personale di Daniele. Non mostrare nomi, volti o dati di studenti.
- Il codice mostrato deve essere corretto e di livello adatto alla classe.
- Pubblicazione: Claude non pubblica da solo. Percorso scelto: bozza nella posta in arrivo di
  TikTok (API Content Posting, modalita' upload) o caricamento manuale; Daniele rivede, sceglie
  la musica e pubblica. La pubblicazione diretta pubblica richiede audit dell'app TikTok.
- Scrivere solo nella repo e nella cartella OneDrive indicata sopra.
