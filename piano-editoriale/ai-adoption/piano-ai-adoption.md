# Piano editoriale: serie "AI Adoption" (uso consapevole dell'AI)

Obiettivo: contenuto didattico a sé, pubblico generico, stesso formato dei video di programmazione (senza voce, musica, tutto a schermo, descrizione bilingue IT/EN con richiamo teorico).

Regole comuni
- Prompt ed esempi sempre realistici e non banali (Daniele, 2026-11-24): prompt strutturati (ruolo, contesto, vincoli, formato), casi limite; esempi verificati prima del video.
- Esempi SEMPRE di risoluzione di algoritmi o programmazione (C++, Java, SQL), complessi e di livello scuola superiore (Daniele insegna informatica, 2026-11-24). Niente fisica, storia, email o altre materie.
- Ogni episodio mostra un prova reale: l'output va registrato al momento e verificato, non scritto a priori (i modelli cambiano, un esempio che oggi fallisce può non fallire domani).
- Nessun dato personale nei prompt; dati e nomi inventati.
- Durata 30-60 s. Hook nei primi 2 secondi (la domanda o l'errore già a schermo). Ultimo frame: la regola in una riga.
- Strumento: uno solo per episodio, nominato in descrizione; niente chiavi API visibili.

---

## Filone 1: AI Mythbusters (Fase 1 - Capire)
Formato: affermazione → prova → verdetto (VERO / FALSO / DIPENDE). Tutti gli esempi sono di programmazione e algoritmi.

| # | Titolo | Cosa si vede | Regola finale |
|---|--------|--------------|---------------|
| 1 | L'AI cita funzioni che esistono? | Si chiedono 3 funzioni di una libreria di nicchia; per ognuna si cerca nella documentazione ufficiale: esiste / non esiste | Una funzione si cerca nella documentazione, non si crede |
| 2 | "Sei sicuro?" | Codice C++ corretto, poi "c'è un bug alla riga 4": l'AI cede o difende il codice? | Insistere non rende l'AI più vera |
| 3 | Stessa domanda, due parole diverse | "Come ordino un array?" contro "Qual è l'algoritmo di ordinamento più veloce?": due risposte diverse affiancate | La domanda orienta la risposta |
| 4 | Perché sbaglia a contare le lettere | Conteggio in una parola + visualizzazione dei token | Vede pezzi di parola, non caratteri |
| 5 | Qual è l'ultima versione? | Si chiede l'ultima versione stabile di Java o dello standard C++; confronto con il sito ufficiale | Ha un limite di conoscenza |
| 6 | Eseguire a mente: AI contro compilatore | Programma con cicli annidati e overflow di int: la traccia dell'AI contro l'output reale | Il codice si esegue, non si crede |
| 7 | La complessità è giusta? | Big-O di un doppio ciclo con uscita anticipata; verifica contando le operazioni | La complessità si misura, non si dà per buona |
## Filone 2: Prompt vs Prompt (Fase 1-2)
Formato: schermo diviso, prompt pigro a sinistra, prompt ben fatto a destra, stesso compito. Tutti i compiti sono di programmazione e algoritmi.

| # | Titolo | Compito | Cosa cambia |
|---|--------|---------|-------------|
| 1 | Spiegami questo errore | Errore del compilatore su un programma C++ | Codice, messaggio, versione e cosa hai già provato |
| 2 | Spiegami la ricorsione | Spiegazione di un concetto con la traccia dello stack sul fattoriale | Livello (terza, C++) e un esempio da tracciare |
| 3 | Code review | Rivedere una funzione di ordinamento | Obiettivo, vincoli e cosa guardare (leggibilità, complessità) |
| 4 | Piano di studio | Verifica su array e matrici in 5 giorni | Vincoli reali: ore al giorno, argomenti, esercizi |
| 5 | Feedback su un algoritmo | Valutare, non riscrivere | "Dimmi 3 punti deboli, non correggere" |
| 6 | Ruolo + Contesto + Formato | Generare casi di test per una funzione | La formula in tre parti applicata |
| 7 | Prompt in due passi | Da pseudocodice a C++ | Prima il piano (top-down), poi il codice |
## Filone 3: Usa l'AI, non farti usare (Fase 2 - Usare)
Formato: modo giusto contro modo sbagliato, con il risultato a confronto. Esempi di algoritmi e programmazione (C++, Java, SQL), mai banali.

| # | Titolo | Scena |
|---|--------|-------|
| 1 | Il tutor che fa domande | Ricerca binaria in C++: prompt con ruolo e regole, domande una alla volta, casi limite finali |
| 2 | Dai tuoi appunti a un quiz | Appunti su puntatori e array: 5 domande con output da prevedere |
| 3 | Flashcard in 20 secondi | Da appunti sui JOIN SQL a carte query ↔ risultato |
| 4 | Simula l'interrogazione | L'AI fa il docente su ereditarietà e polimorfismo in Java, tu rispondi, poi voto motivato |
| 5 | Copiato vs capito | Rimuovere i duplicati da un array ordinato: codice copiato contro codice tuo rivisto dall'AI |
| 6 | Come dichiarare l'uso dell'AI | Riga di trasparenza per la relazione di un progetto (codice generato contro scritto) |
| 7 | Mappa concettuale dagli appunti | Classi Java: gerarchia e polimorfismo, poi correzione a mano |
| 8 | Il riassunto è fedele? | Riassunto di un testo sugli algoritmi di ordinamento: verifica delle complessità citate |

## Tipi di scena (formato "A", strumenti/render_chat.py)
Un video è una sequenza di scene; ogni episodio sceglie quelle che servono. Scene disponibili: `chat` (chat singola), `versus` (due chat impilate, sbagliato/giusto, con badge), `rule` (regola finale). Da implementare: `cards` (quiz e flashcard con rivelazione), `textdiff` (testo originale e riassunto con evidenziazioni), `tree` (mappa concettuale che si costruisce), `note` (riga di trasparenza da copiare).
Tutti gli episodi: hook di 3 righe, barra di avanzamento, caption numerata, badge a timbro, regola finale, CTA. Output dell'AI generati da Claude e registrati con modello e data nel .json.

### Filone 3: mappa episodi e scene
| # | Episodio | Scene | Stato |
|---|----------|-------|-------|
| 3.1 | Il tutor che fa domande (ricerca binaria) | `chat` (tutor, 3 giri) + `rule` | prodotto: f3-01-tutor-che-fa-domande (40 s) |
| 3.2 | Dai tuoi appunti a un quiz (puntatori e array) | `chat` (incolla appunti, chiede 5 domande) + `cards` (domanda, risposta, esito) + `rule` | da fare (serve `cards`) |
| 3.3 | Flashcard in 20 secondi (JOIN SQL) | `chat` (appunti → carte) + `cards` in modalità flashcard + `rule` | da fare (serve `cards`) |
| 3.4 | Simula l'interrogazione (Java: ereditarietà) | `chat` con ruoli (AI docente, tu rispondi) + voto motivato + `rule` | prodotto: f3-04-simula-interrogazione (57 s) |
| 3.5 | Copiato vs capito (rimuovi duplicati) | `versus` + `rule` | prodotto: f3-05-copiato-vs-capito (30 s) |
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
Formato fisso in tre passi: il prompt, la risposta reale, "cosa fai tu". L'ultimo frame dice cosa resta allo studente. Complementare al filone 3 (nessun doppione). Esempi di algoritmi e programmazione.

| # | Titolo | Scena | Regola finale |
|---|--------|-------|---------------|
| 1 | Metodo Feynman | Spieghi la ricorsione a parole tue, l'AI trova i buchi senza spiegarla lei | Se non sai spiegarlo, non l'hai capito |
| 2 | Richiamo attivo | Appunti su ArrayList e Vector con le parole chiave nascoste, tu le recuperi | Ripassare non è rileggere |
| 3 | Ripasso a intervalli | Programma di C++ (array, funzioni, puntatori): piano a 1-3-7-14 giorni | Poco e spesso batte tutto la sera prima |
| 4 | Dove sbaglio di solito | Verifica di C++ inventata e corretta: errori ricorrenti (off-by-one, = al posto di ==) | Gli errori sono la mappa dello studio |
| 5 | Le domande del prof | 3 domande su un programma da tracciare, tu rispondi, poi confronti | Prepara l'esame, non copiare le risposte |
| 6 | Algoritmo con errore nascosto | Bubble sort con lo scambio sbagliato, lo trovi tu | Non fidarti nemmeno dei passaggi |
| 7 | Spezzare il progetto | Gestione biblioteca in Java divisa in blocchi da 25 minuti | Il primo blocco è il più difficile |
| 8 | L'avvocato del diavolo | L'AI attacca la tua scelta (array o ArrayList, complessità della soluzione), tu rispondi | Una scelta regge se resiste alle obiezioni |

Idee da valutare (non ancora nel piano): conversazione tecnica in inglese con correzione dei termini; preparare un'esposizione orale del progetto (scaletta e tempi); il codice scritto dall'AI con un test di comprensione dopo (taglio positivo: cosa guadagni davvero se lo scrivi tu).
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
