# Piano editoriale

Piani dettagliati per classe: `3DINF/piano-3DINF.md`, `4DINF/piano-4DINF.md`, `5DINF/piano-5DINF.md`.

## Formati di episodio

| Sigla | Formato | Struttura (20-30 s) | Renderer |
|-------|---------|---------------------|----------|
| C | Concetto | Hook, codice che si scrive, visualizzazione, terminale | disponibile (C++) |
| I | Indovina l'output | Codice, domanda, pausa con conto alla rovescia, risposta reale eseguita | da aggiungere |
| E | Trova l'errore | Codice con un bug, errore o risultato sbagliato, correzione | da aggiungere (errore atteso) |
| S | Sfida guidata | Consegna a schermo, pausa, soluzione scritta | da aggiungere |

I formati I, E e S servono da richiamo e da esercitazione, e fanno interagire (commenti con la risposta).

## Estensioni del renderer, in ordine di priorita'
1. Formati I, E, S (valgono per tutti i linguaggi).
2. Input simulato per `cin` (3D, blocco B).
3. Java (4D): compilazione con `javac`, output reale.
4. SQL (5D): esecuzione con SQLite e visualizzazione delle tabelle. `GRANT`, procedure e `FOR UPDATE`
   non sono supportati da SQLite: si mostrano senza eseguirli, oppure con un MySQL/MariaDB installato.
5. Grafiche nuove: diagramma a blocchi (3D A), UML (4D A), schema E/R (5D A).

## Come scegliere i prossimi episodi
Indica nel piano di classe gli episodi da produrre per primi (o cambia titolo, esempio, ordine).
Ogni episodio prodotto passa a "fatto" con il nome della cartella.
