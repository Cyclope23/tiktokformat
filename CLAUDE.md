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
- piano-editoriale/PIANO-PUBBLICAZIONE.md + pubblicazione.json + calendario.csv -> slot di pubblicazione;
  strumenti/pianifica.py rigenera il calendario (da rilanciare a ogni episodio prodotto o funzione del renderer aggiunta)

Nomi: tutto minuscolo, trattini, nessun underscore, numero progressivo per classe
(numero = ordine di produzione nella classe; la 3ª riparte da 01 dopo l'azzeramento del 2026-11-17). Le cartelle episodio contengono sempre i tre file.

## Creare un episodio
1. Copia strumenti/episodio-modello.json nella nuova cartella episodio e compilalo.
2. Renderizza: python3 strumenti/render.py <ep>.json -o <ep>.mp4 [--music brano.mp3] [--set cps=22]
   Anteprima fotogrammi: --preview 5,10,20 -o <cartella>
3. Il renderer compila ed esegue davvero il codice (g++ -std=c++17): l'output nel terminale
   del video e' quello reale. Se non compila, il rendering si ferma.
4. CONTROLLO FOTOGRAMMI OBBLIGATORIO (ogni volta che si genera o rigenera un video, anche per una sola modifica
   al renderer: si ricontrollano TUTTI i video toccati): python3 strumenti/controlla.py <ep>.json
   produce un foglio con 12 fotogrammi lungo tutto il video; va guardato per intero. Verificare: ogni file/classe
   resta visibile abbastanza da essere letto (almeno ~3 s, scheda compresa), il codice completo si vede, testo non
   tagliato, righe dentro il pannello, caption coerenti con cio' che e' mostrato (numeri di righe, valori), pannello
   viz utile e non vuoto, output del terminale reale e colore giusto (errori in rosso), CTA e annuncio finali.
   Nessuna consegna e nessun commit di mp4 senza questo controllo; se emerge un difetto: correggere, rigenerare, ricontrollare.
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
  del prossimo episodio. Durata 20-30 s per i video semplici; fino a 90 s (1,5 min) ammessi per Java a piu' file e per la teoria animata (decisione di Daniele 2026-11-18). Dimensione di codice e terminale automatica (la piu' grande che entra: codice max 44, terminale max 40). Margini: 80 px a destra, 30 a sinistra; zona sicura fino a y=1650
  e in alto oltre y=150 (zone coperte dall'interfaccia TikTok).
- Nessuna voce. Audio muto o musica; la musica si sceglie nell'editor di TikTok alla pubblicazione.
- Un concetto per episodio; esempi reali, brevi (10-14 righe).

## REGOLA DIDATTICA 4D (Java): classe modello separata dal Main
Per ogni episodio della 4D, anche strutture dati e file: la classe modello sta in un file proprio (es. Pila.java,
Coda.java, Punto.java) e il Main (classe applicativa) serve solo a istanziarla e provarla. Mai tutta la logica dentro il Main.
Si usa "files" nel JSON (una scheda per classe, Main per ultimo), come negli esempi Televisore e Punto/Grafico/Avvio.
Vale anche per Vector, Pila, Coda, String e file (es. classe Rubrica che legge/scrive, il Main la prova).
(Indicazione di Daniele, 2026-11-18, da ricordare sempre.)

## Operazioni "viz" disponibili nel JSON
init (values) | push (value) | set (index, value, label) | iterate (count, labels, var) |
label (text) | size. Ogni step: after_line, caption, viz, highlight_lines.
Opzioni episodio: theme (override parametri), viz_title, viz_index (true/false).
Nomi sotto le caselle: viz init con "names": [...] o push con "name". Con i nomi l'indice [i] non compare.
Formato I (quiz): "quiz": {"question": "...", "seconds": 3} -> dopo il codice c'e' un conto alla rovescia, poi
la risposta con l'esecuzione reale (run_caption = didascalia della risposta).
Formato E (trova l'errore): "fix": {"line": N, "new": "riga corretta", "find_caption", "bug_caption",
"fix_caption", "run2_caption"} -> il codice dato e' quello con il bug (evidenziato in rosso), viene eseguito
(o mostrato l'errore reale del compilatore), poi la riga e' riscritta in verde e il programma rieseguito.

Teoria animata (strutture dati, blocco D 4D: Vector, Pila, Coda): "teoria": {"title", "kind": "stack|queue|vector",
"rule" (frase fissa in basso, es. "LIFO · Last In, First Out"), "step_seconds" (default 2.4),
"steps": [{"op": "push|pop|enqueue|dequeue|add|remove(index)|get(index)|size", "value", "caption"}]}
-> dopo l'hook una sezione animata (caselle che entrano/escono, etichette TOP / FRONT / BACK, indici) prima del codice;
il codice parte alla fine della teoria. Aggiunge ~10-13 s al video, durata massima 90 s (decisione di Daniele 2026-11-18: teoria dentro lo stesso video).
Teoria: 4-5 passi, stessi numeri del codice che segue.

## Descrizione del post (file .txt)
Sempre bilingue, italiano poi inglese: riga di apertura + "Richiamo teorico" (3-4 punti brevi, corretti),
poi "English:" con la stessa apertura e "Theory recap:" con gli stessi punti, poi gli hashtag.
Nel JSON: post.caption, post.theory (IT), post.caption_en, post.theory_en (EN).
Rigenera solo il testo senza rifare il video: python3 strumenti/render.py <ep>.json --solo-testo
Hashtag base: #cpp #programmazione #coding #imparareacodare #informatica #scuola #learnontiktok #learntocode
(adattare per Java, SQL, Sistemi e Reti).

## Regole
- Account: profilo personale di Daniele. Non mostrare nomi, volti o dati di studenti.
- Il codice mostrato deve essere corretto e di livello adatto alla classe.
- Pubblicazione: Claude non pubblica da solo. Percorso scelto: bozza nella posta in arrivo di
  TikTok (API Content Posting, modalita' upload) o caricamento manuale; Daniele rivede, sceglie
  la musica e pubblica. La pubblicazione diretta pubblica richiede audit dell'app TikTok.
- Scrivere solo nella repo e nella cartella OneDrive indicata sopra.
