# Piano editoriale: serie "AI Adoption" (uso consapevole dell'AI)

Obiettivo: contenuto didattico a sé, pubblico generico, stesso formato dei video di programmazione (senza voce, musica, tutto a schermo, descrizione bilingue IT/EN con richiamo teorico).

Regole comuni
- Prompt ed esempi sempre realistici e non banali (Daniele, 2026-11-24): prompt strutturati (ruolo, contesto, vincoli, formato), problemi veri, casi limite; esempi verificati prima del video.
- Ogni episodio mostra un prova reale: l'output va registrato al momento e verificato, non scritto a priori (i modelli cambiano, un esempio che oggi fallisce può non fallire domani).
- Nessun dato personale nei prompt; dati e nomi inventati.
- Durata 30-60 s. Hook nei primi 2 secondi (la domanda o l'errore già a schermo). Ultimo frame: la regola in una riga.
- Strumento: uno solo per episodio, nominato in descrizione; niente chiavi API visibili.

---

## Filone 1: AI Mythbusters (Fase 1 - Capire)
Formato: affermazione → prova → verdetto (VERO / FALSO / DIPENDE).

| # | Titolo | Cosa si vede | Regola finale |
|---|--------|--------------|---------------|
| 1 | L'AI cita fonti: esistono? | Si chiedono 3 riferimenti su un tema di nicchia; per ognuno si cerca titolo/link e si segna esiste / non esiste | Una fonte si apre, non si crede |
| 2 | "Sei sicuro?" | Risposta corretta, poi "no, ti sbagli": l'AI cede o no? | Insistere non rende l'AI più vera |
| 3 | Stessa domanda, due parole diverse | Due formulazioni quasi uguali, due risposte diverse affiancate | La domanda orienta la risposta |
| 4 | Perché sbaglia a contare le lettere | Conteggio in una parola + visualizzazione dei token | Vede pezzi di parola, non lettere |
| 5 | Che giorno è oggi? | Domanda sulla data/ultima notizia; confronto con orologio | Ha un limite di conoscenza |
| 6 | Calcolo lungo: AI vs calcolatrice | Moltiplicazione a molte cifre, verifica con calcolatrice | Per i numeri si verifica |
| 7 | "Scrivi la storia di un ingegnere e di un'infermiera" | Si guardano genere e ruoli attribuiti | I bias sono nei dati, controllali |

## Filone 2: Prompt vs Prompt (Fase 1-2)
Formato: schermo diviso, prompt pigro a sinistra, prompt ben fatto a destra, stesso compito.

| # | Titolo | Compito | Cosa cambia |
|---|--------|---------|-------------|
| 1 | Riassunto di un appunto | Riassumere 1 pagina | Aggiunge lunghezza, destinatario, formato |
| 2 | Spiegami la fotosintesi | Spiegazione di un concetto | Livello ("come a un 12enne") + esempio |
| 3 | Email al professore | Richiesta di spostare una verifica | Contesto e tono |
| 4 | Piano di studio | Studiare in 5 giorni | Vincoli reali (ore, argomenti) |
| 5 | Feedback su un tema | Valutare, non riscrivere | "Dimmi 3 punti deboli, non correggere" |
| 6 | Ruolo + Contesto + Formato | Qualsiasi richiesta | La formula in tre parti applicata |
| 7 | Prompt in due passi | Compito complesso | Prima il piano, poi l'esecuzione |

## Filone 3: Usa l'AI, non farti usare (Fase 2 - Usare)
Formato: modo giusto vs modo sbagliato, con il risultato a confronto.

| # | Titolo | Scena |
|---|--------|-------|
| 1 | Il tutor che fa domande | Prompt "guidami con domande, non darmi la soluzione" su un esercizio di matematica |
| 2 | Dai tuoi appunti a un quiz | Incolli appunti, ottieni 5 domande, rispondi |
| 3 | Flashcard in 20 secondi | Da appunti a carte domanda/risposta |
| 4 | Simula l'interrogazione | L'AI fa il docente, tu rispondi, poi ti dà un voto motivato |
| 5 | Copiato vs capito | Stesso esercizio: incolla la risposta vs spiegarla con parole proprie |
| 6 | Come dichiarare l'uso dell'AI | Riga di trasparenza da inserire in una relazione |
| 7 | Mappa concettuale dagli appunti | Struttura gerarchica generata, poi corretta a mano |
| 8 | Il riassunto è fedele? | Controllo di un riassunto AI contro il testo originale |

## Tipi di scena (formato "A", strumenti/render_chat.py)
Un video è una sequenza di scene; ogni episodio sceglie quelle che servono. Scene disponibili: `chat` (chat singola), `versus` (due chat impilate, sbagliato/giusto, con badge), `rule` (regola finale). Da implementare: `cards` (quiz e flashcard con rivelazione), `textdiff` (testo originale e riassunto con evidenziazioni), `tree` (mappa concettuale che si costruisce), `note` (riga di trasparenza da copiare).
Tutti gli episodi: hook di 3 righe, barra di avanzamento, caption numerata, badge a timbro, regola finale, CTA. Output dell'AI generati da Claude e registrati con modello e data nel .json.

### Filone 3: mappa episodi e scene
| # | Episodio | Scene | Stato |
|---|----------|-------|-------|
| 3.1 | Il tutor che fa domande | `chat` (tutor, 3 giri) + `rule` | prodotto: f3-01-tutor-che-fa-domande (40 s) |
| 3.2 | Dai tuoi appunti a un quiz | `chat` (incolla appunti, chiede 5 domande) + `cards` (domanda, risposta, esito) + `rule` | da fare (serve `cards`) |
| 3.3 | Flashcard in 20 secondi | `chat` (appunti → carte) + `cards` in modalità flashcard + `rule` | da fare (serve `cards`) |
| 3.4 | Simula l'interrogazione | `chat` con ruoli (AI docente, tu rispondi) + voto motivato + `rule` | da fare (solo `chat`) |
| 3.5 | Copiato vs capito | `versus` + `rule` | prodotto: f3-05-copiato-vs-capito (30 s) |
| 3.6 | Come dichiarare l'uso dell'AI | `chat` (chiedi la formula) + `note` (riga pronta) + `rule` | da fare (serve `note`) |
| 3.7 | Mappa concettuale dagli appunti | `chat` + `tree` (mappa che si costruisce) + correzione a mano + `rule` | da fare (serve `tree`) |
| 3.8 | Il riassunto è fedele? | `textdiff` (frasi evidenziate: fedele / aggiunta / omessa) + `rule` | da fare (serve `textdiff`) |
Ordine di produzione consigliato: 3.4 (solo chat) → 3.2 e 3.3 (stesse `cards`) → 3.8 → 3.7 → 3.6.

## Filone 4: Debug con l'AI, senza farsi scrivere il codice (Fase 2, linguaggi delle tue classi)
Formato: codice con errore → si chiede una spiegazione, non la correzione → si corregge a mano.

| # | Titolo | Linguaggio | Errore |
|---|--------|------------|--------|
| 1 | Leggere un errore con l'AI | C++ | Indice fuori dal vettore |
| 2 | NullPointerException | Java | Oggetto non inizializzato |
| 3 | Il ciclo che fa un giro di troppo | C++ | Off-by-one |
| 4 | Scrivi prima il test | Java | Test case per un metodo, poi il fix |
| 5 | Tre livelli di aiuto | C++ | Hint → indizio → soluzione, fermarsi al primo |
| 6 | L'AI propone un fix sbagliato | Java | Trovare cosa non va nel suggerimento |
| 7 | La query che duplica le righe | SQL | JOIN senza condizione corretta |

## Filone 5: Costruiamo un assistente (Fase 3 - Costruire)
Formato: timelapse di costruzione + prova finale. Dati inventati.

| # | Titolo | Cosa si costruisce |
|---|--------|--------------------|
| 1 | Un assistente FAQ in 60 secondi | No-code, con 10 FAQ inventate |
| 2 | Lo stesso assistente in 20 righe | Python con API (senza chiave a schermo) |
| 3 | Generatore di esercizi | Output in formato strutturato (JSON) |
| 4 | Un tutor di materia | Istruzione di sistema che vieta di dare la soluzione |
| 5 | Mettilo alla prova | Domande trabocchetto all'assistente |
| 6 | Migliorarlo con esempi | Prima/dopo aggiungendo esempi al prompt |
| 7 | Cosa può andare storto | Privacy, allucinazioni, uso improprio: checklist dei rischi |

## Filone 6: Studiare meglio con l'AI (Fase 2 - Usare)
Formato fisso in tre passi: il prompt, la risposta reale, "cosa fai tu". L'ultimo frame dice cosa resta allo studente. Complementare al filone 3 (nessun doppione con tutor, quiz, flashcard, simulazione interrogazione).

| # | Titolo | Scena | Regola finale |
|---|--------|-------|---------------|
| 1 | Metodo Feynman | Spieghi un concetto a parole tue, l'AI trova i buchi senza spiegarlo lei | Se non sai spiegarlo, non l'hai capito |
| 2 | Richiamo attivo | L'AI nasconde le parole chiave degli appunti, tu le recuperi | Ripassare non è rileggere |
| 3 | Ripasso a intervalli | Da un programma, piano di ripasso a 1-3-7-14 giorni | Poco e spesso batte tutto la sera prima |
| 4 | Dove sbaglio di solito | Compito inventato e corretto, l'AI individua gli errori ricorrenti | Gli errori sono la mappa dello studio |
| 5 | Le domande del prof | L'AI prevede 3 domande d'esame, tu rispondi, poi confronti | Prepara l'esame, non copiare le risposte |
| 6 | Esercizio con errore nascosto | Soluzione con un errore voluto, lo trovi tu | Non fidarti nemmeno dei passaggi |
| 7 | Spezzare il compito | Compito grosso diviso in blocchi da 25 minuti | Il primo blocco è il più difficile |
| 8 | L'avvocato del diavolo | L'AI attacca la tua tesi, tu rispondi | Una tesi regge se resiste alle obiezioni |

Idee da valutare (non ancora nel piano): conversazione in inglese con correzione degli errori; preparare un'esposizione orale (scaletta e tempi); il tema scritto dall'AI con un test di comprensione dopo (taglio positivo: cosa guadagni davvero se lo scrivi tu, non un'accusa agli studenti).

---

## Ordine di pubblicazione suggerito (1 al giorno)
Partire con la serie 1, ep. 1 (gancio più forte), poi alternare i filoni: 1 → 2 → 3 → 4 → 5 → 6 → 1 → 2 → ...
Gli episodi del filone 4 si possono mischiare ai video di programmazione già in calendario.

## Decisioni (2026-11-24)
- Output dell'AI: generati da Claude durante la sessione di produzione, salvati nel .json con data e modello; strumento citato in descrizione: Claude.
- Account: stesso profilo TikTok; serie riconoscibile con "AI Adoption" in descrizione e hashtag.
- Ritmo: 1 episodio AI ogni 3 giorni, programmazione prevalente (circa 2 a 1).
- Filone 6 "Studiare meglio con l'AI" aggiunto come filone separato (8 episodi): totale 44 episodi in 6 filoni.
- Ordine di produzione: 4.1 subito (renderer attuale), poi 2.1, 3.1 e 6.1/6.2 (serve il formato chat "A"), 1.1; il filone 5 per ultimo.

## Da fare
- Nuovo formato "A" nel renderer: scena chat singola o a schermo diviso, badge verdetto (VERO/FALSO/DIPENDE).
- Cartella episodi/ai-adoption/<filone>-<n>-<titolo>/ con .mp4, .txt, .json (trascrizione reale).
- Estendere strumenti/pianifica.py con la serie AI e il rapporto 1 a 3.
- Filone 4.7 (SQL) dipende dal supporto SQLite del renderer.
