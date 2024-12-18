# Function App demo: Task Management

## Description

Questo è un progetto semplice per la gestione di task. Questa parte fornisce solo la Function App.

Nei pochi metodi implementati, si può vedere come si possa utilizzare Azure Functions per creare un'applicazione serverless che comunica con un database tramite pyodbc.

La parte più cruciale del codice è assicurarsi di restituire una risposta HTTP corretta in ogni situazione. In caso di errore, è importante restituire un codice di errore HTTP e un messaggio di errore esplicito per aiutare il client a capire cosa è andato storto. Senza questo passaggio, il client non saprà come procedere perché Azure Functions restituirà un codice 500 senza messaggio.

Di conseguenza, l'uso di `try` e `except` è fondamentale per gestire le eccezioni e restituire un messaggio di errore appropriato.

## Funzionalità

- Aggiunta di task
- Lettura di task
- Aggiornamento stato task