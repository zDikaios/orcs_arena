Arena - Progetto Object Oriented Programming
=

Descrizione
-
Questo progetto è un semplice gioco a turni sviluppato in Python
come esercizio di programmazione orientata agli oggetti.
Il giocatore può affrontare una serie di nemici in un’arena,
scegliendo tra classi con abilità diverse, usare oggetti e salvare
il suo progresso.
I nemici aumentano di difficoltà ogni round e il loro comportamento
cambia in base allo stadio raggiunto

Requisiti
-
- Python 3.13

Struttura del Progetto
-
Il progetto è organizzato in più file Python per una migliore
manutenibilità:
- `main.py`: Menu principale e loop di gioco
- `characters.py`: Definisce le classi Character, Mago, Guerriero e le loro abilità
- `nemici.py`: Definisce la classe Enemy e le sue abilità
- `items.py`: Definisce gli oggetti utilizzabili nel gioco
- `creatore.py`: Factory per creare i personaggi dei giocatori
- `saveload.py`: Gestisce la logica del salvataggio e caricamento del gioco tramite file txt
- `utilities.py`: Contiene funzioni utili per il gioco
- `strategianemica.py`: Design pattern che determina il comportamento dei nemici
- `README.md`: Questo file :)
- (opzionale) `salvataggio.txt` File di salvataggio

Guida all'avvio
-
Eseguire il main
