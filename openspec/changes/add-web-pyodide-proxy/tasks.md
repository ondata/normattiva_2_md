## 1. Implementation
- [ ] 1.1 Estrarre una funzione di conversione pura `convert_xml_text_to_md(xml_text, metadata=None)` che non legge/scrive file.
- [ ] 1.2 Creare Cloudflare Worker che valida URL normattiva, estrae parametri (se permalink), chiama `caricaAKN`, applica limiti dimensione e risponde con CORS aperto.
- [ ] 1.3 Implementare client web (bookmarklet/estensione) che prende l’URL corrente, chiama il Worker e invia l’XML a Pyodide per la conversione.
- [ ] 1.4 Integrare backoff/rate-limit minimo (≥1s tra fetch a normattiva) nel Worker o client.
- [ ] 1.5 Aggiungere documentazione d’uso e limitazioni (niente batch riferimenti, non sostituisce CLI).
- [ ] 1.6 Eseguire smoke test manuale: permalink → Worker → XML → Markdown in Pyodide; verificare heading e front matter.
