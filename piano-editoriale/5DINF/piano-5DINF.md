# Piano episodi 5D INF - Basi di dati e SQL

Base: piano di lavoro 5D INF 2025/26 (`contenuti-5DINF.md`). Richiede la modalita' SQL del renderer (SQLite per l'esecuzione reale).

Episodi pianificati: **27**.

Tipo: **C** concetto, **I** indovina l'output, **E** trova l'errore, **S** sfida guidata. Vedi `../PIANO.md`.

**Blocco A - Progettazione di basi di dati** (grafica nuova: schemi E/R)

| # | Tipo | Titolo | Esempio / idea | Stato |
|---|------|--------|----------------|-------|
| A1 | C | Archivi e basi di dati | Il problema della ridondanza nei file | da fare |
| A2 | C | Entità e associazioni | Schema E/R dello studente e del corso | da fare |
| A3 | C | Cardinalità | 1:1, 1:N, N:M | da fare |
| A4 | C | Dal modello E/R al relazionale | Associazione N:M che diventa tabella ponte | da fare |
| A5 | C | Chiave primaria e chiave esterna | Vincolo di integrità referenziale | da fare |

**Blocco B - SQL** (grafica nuova: tabelle e risultati)

| # | Tipo | Titolo | Esempio / idea | Stato |
|---|------|--------|----------------|-------|
| B1 | C | `CREATE TABLE` e tipi di dato | Tabella `studente` | da fare |
| B2 | C | `INSERT` | Righe che compaiono nella tabella | da fare |
| B3 | C | `SELECT` e `WHERE` | Selezione e proiezione | da fare |
| B4 | C | `ORDER BY` | Ordinamento crescente e decrescente | da fare |
| B5 | C | Funzioni aggregate | `COUNT`, `SUM`, `AVG`, `MIN`, `MAX` | da fare |
| B6 | C | `GROUP BY` | Righe che si raggruppano | da fare |
| B7 | C | `HAVING` contro `WHERE` | Filtro prima e dopo il raggruppamento | da fare |
| B8 | E | Trova l'errore: `DELETE` senza `WHERE` | Cancella tutta la tabella | da fare |
| B9 | C | `UPDATE` e `DELETE` | Modifiche mirate | da fare |
| B10 | C | `INNER JOIN` | Righe che si accoppiano sulla chiave | da fare |
| B11 | C | `LEFT JOIN` | Le righe senza corrispondenza con `NULL` | da fare |
| B12 | C | Self join | Dipendenti e capi nella stessa tabella | da fare |
| B13 | C | Interrogazioni annidate | Sottoquery nel `WHERE` | da fare |
| B14 | I | Indovina il risultato della query | Una `JOIN` e quante righe produce | da fare |
| B15 | S | Sfida: scrivi la query | Consegna in linguaggio naturale, poi la soluzione | da fare |
| B16 | C | Viste | `CREATE VIEW` | da fare |
| B17 | C | `GRANT` e `REVOKE` | Permessi sugli utenti (mostrato, non eseguito) | da fare |

**Blocco C - MySQL**

| # | Tipo | Titolo | Esempio / idea | Stato |
|---|------|--------|----------------|-------|
| C1 | C | Transazioni: `COMMIT` e `ROLLBACK` | Trasferimento tra due conti | da fare |
| C2 | C | `SELECT ... FOR UPDATE` | Il blocco di una riga (mostrato, non eseguito) | da fare |
| C3 | C | Procedure e function | Una function che calcola l'IVA | da fare |

**Blocco D - Dati in rete con PHP**

| # | Tipo | Titolo | Esempio / idea | Stato |
|---|------|--------|----------------|-------|
| D1 | C | PHP e database | Connessione e query, risultato in tabella HTML | da fare |
| D2 | C | Form e prepared statement | Il pericolo dell'SQL injection | da fare |
