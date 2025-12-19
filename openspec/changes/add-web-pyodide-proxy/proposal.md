## Why
Normattiva blocca CORS, impedendo di usare normattiva2md direttamente dal browser. Servono un proxy controllato e un bundle Pyodide leggero per offrire una conversione “light” lato web senza sostituire la CLI esistente.

## What Changes
- Creare un Cloudflare Worker/Pages Function che accetta solo endpoint normattiva (`uri-res/N2Ls`, `do/atto/caricaAKN`), applica throttling leggero e restituisce XML con CORS permessivo.
- Estrarre un entry point di conversione “pure” (input: stringa XML, output: markdown) riusando il core attuale senza dipendenze di rete/file.
- Fornire client web minimale (bookmarklet/estensione) che dalla pagina Normattiva chiama il Worker e converte con Pyodide, generando markdown scaricabile.
- Documentare limiti (niente batch citazioni, rispetto TOS, backoff ≥1s) e mantenere la CLI invariata.

## Impact
- Affected specs: markdown-conversion (aggiunta modalità web light).
- Affected code: `markdown_converter.py` (facciata string→string), packaging frontend assets, nuovo Worker repo/file. Nessun breaking change per la CLI.
