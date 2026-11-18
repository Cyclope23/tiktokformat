# Piano episodi 4D INF - Java

Base: programma svolto 4D INF 2025/26. Richiede l'estensione del renderer a Java.

Episodi pianificati: **46** (aggiornato 2026-11-18: Vector, Pila e Coda anche con Vector, gestione dei file, approfondimento String).

Tipo: **C** concetto, **I** indovina l'output, **E** trova l'errore, **S** sfida guidata. Vedi `../PIANO.md`.

**Blocco A - Modellazione UML** (grafica nuova: schemi UML)

| # | Tipo | Titolo | Esempio / idea | Stato |
|---|------|--------|----------------|-------|
| A1 | C | Use case diagram | Attori e casi d'uso di un sistema di prestiti | da fare |
| A2 | C | Class diagram | Classe con attributi e metodi, poi relazioni | da fare |
| A3 | C | Dal class diagram al codice Java | Lo stesso schema che diventa `class` | da fare |

**Blocco B - Basi di Java**

| # | Tipo | Titolo | Esempio / idea | Stato |
|---|------|--------|----------------|-------|
| B1 | C | Struttura di un programma Java | `class`, `main`, `System.out.println` | fatto (01) |
| B2 | C | Variabili e costanti | `final` e inferenza `var` | fatto (02) |
| B3 | C | Tipi primitivi e `String` | `int`, `double`, `boolean`, `char` | fatto (09) |
| B4 | C | Il casting | `(int) 3.9`, ampliamento e restringimento | fatto (10) |
| B5 | I | Indovina l'output: divisione tra interi | `5 / 2` e `5 / 2.0` | fatto (03) |
| B6 | C | Gli operatori | `++`, `+=`, precedenza | fatto (11) |
| B7 | C | Array in Java | Dichiarazione, `length`, scorrimento | fatto (12) |
| B8 | C | Le eccezioni: try e catch | `ArrayIndexOutOfBoundsException` gestita | fatto (13) |
| B9 | E | Trova l'errore: eccezione non gestita | `NumberFormatException` sulla conversione | fatto (14) |

**Blocco C - Classi e oggetti** (convenzione della serie: ogni classe in un file separato; il `Main` serve solo a lanciare e a usare le istanze)

| # | Tipo | Titolo | Esempio / idea | Stato |
|---|------|--------|----------------|-------|
| C1 | C | Classe e oggetto | `Cane.java` e `Main` con due `new` | fatto (04) |
| C2 | C | Attributi private | `c.saldo` dal main: errore reale di `private` | fatto (05) |
| C3 | C | Getter e setter | `getSaldo`, `setSaldo`, `this` | fatto (06) |
| C4 | C | Il costruttore | `new Conto(200)` | fatto (07) |
| C5 | C | toString | `println(c)` e `@Override` | fatto (08) |
| C6 | C | Metodi di una classe | `versa()` e `preleva()` con controllo | fatto (15) |
| C7 | C | La classe completa | `Persona`: private, costruttore, setter con controllo, toString | fatto (16) |
| C8 | C | Riferimenti: due variabili, un oggetto | `b = a` e modifica visibile da entrambe | da fare |
| C9 | I | Indovina l'output: riferimenti | Modifica tramite un alias | da fare |
| C10 | C | Ereditarietà | `extends` e `super` | da fare |
| C11 | C | Sottoclassi | `Studente` e `Docente` da `Persona` | da fare |
| C12 | C | Polimorfismo | Array di `Animale`, `override` di `parla()` | da fare |
| C13 | C | Le Stringhe | Immutabilità e oggetto `String` | da fare |
| C14 | E | Trova l'errore: `==` contro `equals` | Confronto tra stringhe | da fare |
| C15 | S | Sfida: classe `Rettangolo` | Consegna e soluzione (classe completa) | da fare |
| C16 | C | String: length, charAt, substring | Leggere e ritagliare un testo | da fare |
| C17 | C | String: indexOf, contains, replace | Cercare e sostituire | da fare |
| C18 | C | String: trim, toUpperCase, split | Pulire e dividere (es. riga `nome;età`) | da fare |
| C19 | I | Indovina l'output: substring e indici | Estremo finale escluso | da fare |
| C20 | S | Sfida: parola palindroma | Consegna e soluzione con i metodi di String | da fare |

**Blocco D - Strutture dati** (Pila e Coda realizzate sia con `ArrayList` sia con `Vector`)

| # | Tipo | Titolo | Esempio / idea | Stato |
|---|------|--------|----------------|-------|
| D1 | C | Array dinamico (`ArrayList`) | `add`, `get`, `size` | da fare |
| D2 | C | La classe `Vector` | `add`, `get`, `size`, `remove`, `elementAt` | fatto (17) |
| D3 | C | `ArrayList` e `Vector` a confronto | Stessa interfaccia, `Vector` sincronizzato | da fare |
| D4 | C | `Vector<Punto>` | Vettore di oggetti: ricerca e rimozione | da fare |
| D5 | C | La pila (LIFO) con `ArrayList` | `push` e `pop` animati | fatto (18) |
| D6 | C | La pila (LIFO) con `Vector` | Stessa classe `Pila`, contenitore diverso | fatto (19) |
| D7 | C | La coda (FIFO) con `ArrayList` | `enqueue` e `dequeue` animati | da fare |
| D8 | C | La coda (FIFO) con `Vector` | Stessa classe `Coda`, contenitore diverso | da fare |
| D9 | S | Sfida: parentesi bilanciate con la pila | Consegna e soluzione | da fare |

**Blocco E - Gestione dei file**

| # | Tipo | Titolo | Esempio / idea | Stato |
|---|------|--------|----------------|-------|
| E1 | C | Leggere un file di testo | `Scanner` su `File`, riga per riga | da fare |
| E2 | C | Scrivere su un file | `PrintWriter` / `FileWriter` | da fare |
| E3 | E | Trova l'errore: file inesistente | `FileNotFoundException` gestita con `try`/`catch` | da fare |
| E4 | C | Salvare e caricare un `Vector` di oggetti | `Vector<Punto>` su file, una riga per oggetto | da fare |
| E5 | S | Sfida: rubrica su file | Consegna e soluzione | da fare |
