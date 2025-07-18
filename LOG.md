# LOG.md - Registro degli Avanzamenti del Progetto

Questo file documenta gli avanzamenti significativi, le decisioni chiave e le modifiche importanti apportate al progetto `normattiva_2_md`.

## 2025-07-18

### Inizializzazione del Progetto e Setup Iniziale

- **Analisi Iniziale e Creazione PRD:** Analizzati i file `.py` (`convert_akomantoso.py`, `setup.py`) per dedurre la funzionalità del tool. Creato il documento `PRD.md` nella root del progetto, descrivendo le funzionalità, i requisiti tecnici e di usabilità.
- **Aggiornamento PRD con Obiettivo di Alto Livello:** Il `PRD.md` è stato aggiornato per riflettere l'obiettivo specifico del tool: convertire norme da `normattiva.it` in Markdown per l'utilizzo con LLM e AI (creazione di bot basati su norme legali).
- **Riorganizzazione dei File di Test:**
    - Eliminati i file Markdown di output di test (`output.md`, `output_improved.md`, ecc.) dalla root.
    - Creata la directory `test_data/`.
    - Spostato il file XML di esempio (`20050516_005G0104_VIGENZA_20250130.xml`) in `test_data/`.
    - Aggiunto un `README.md` all'interno di `test_data/` per documentare lo scopo e l'utilizzo dei file di test.
- **Configurazione Git:**
    - Inizializzato il repository Git (`git init`).
    - Creato il file `.gitignore` per escludere directory di build (`build/`, `dist/`), file compilati (`*.pyc`, `__pycache__/`), file temporanei e specifici di Windows (`.DS_Store`, `Thumbs.db`, `*.xml:Zone.Identifier`).
    - Creato il file `.gitattributes` per normalizzare i fine riga (`eol=lf`) per i file `.py`, `.md` e `.xml`, garantendo la compatibilità cross-platform (Windows/Linux).
- **Aggiornamento README.md:** La descrizione iniziale del `README.md` è stata aggiornata per allinearsi all'obiettivo di alto livello del progetto (conversione di norme da `normattiva.it` per LLM/AI).
- **Creazione LOG.md:** Questo file è stato creato per tracciare gli avanzamenti del progetto.
