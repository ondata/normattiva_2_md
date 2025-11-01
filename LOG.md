# LOG.md - Registro degli Avanzamenti del Progetto

Questo file documenta gli avanzamenti significativi e le decisioni chiave del progetto `normattiva_2_md`.

## 2025-11-01

### Automazione release binarie

- Aggiunto workflow GitHub Actions `Build Releases` (`.github/workflows/release-binaries.yml`) per creare e impacchettare eseguibili PyInstaller Linux/Windows ad ogni tag `v*` o esecuzione manuale
- Verifiche incluse nel workflow: `make test` su Linux, unittest + run CLI/exe su Windows
- Asset generati: `akoma2md-<version>-linux-x86_64.tar.gz` e `akoma2md-<version>-windows-x86_64.zip` pubblicati automaticamente nelle release taggate
- Aggiornato `README.md` con procedura operativa per pubblicare nuovi binari

### README: rimossi riferimenti release inesistenti

- Rimossa sezione "Eseguibile Standalone" con link a release inesistenti
- Riorganizzati metodi installazione: uv (raccomandato), pip, esecuzione diretta
- Chiarito che build pyinstaller è opzionale per uso locale

### Consolidamento Documentazione Verifiche

- Uniti `VERIFICATION_TASKS.md` e `VERIFICATION_REPORT.md` → `VERIFICATION.md`
- Documento sintetico: stato verifiche, fix implementati, checklist
- Rimossi file test: `test_*.md`, `output_normattiva.json`, build artifacts
- Aggiornati riferimenti in `AGENTS.md`, `.gemini/GEMINI.md`

### Fix Heading Capo/Sezione

- **IMPLEMENTATO**: Separazione automatica heading Capo/Sezione
- Aggiunte funzioni `parse_chapter_heading()` e `format_heading_with_separator()`
- Pattern regex per rilevare e splittare "Capo [N] ... Sezione [N] ..."
- Gestione modifiche legislative `(( ))` negli heading
- Formato output:
  - `## Capo I - TITOLO` (livello 2)
  - `### Sezione I - Titolo` (livello 3)
- Test riusciti su 3 documenti:
  - CAD (D.Lgs. 82/2005): 5 Capi con Sezioni, 3 senza
  - Codice Appalti (D.Lgs. 163/2006): heading complessi con modifiche
  - Costituzione: struttura diversa (TITOLO/SEZIONE) - non gestita
- Migliorata leggibilità e gerarchia degli heading
- File modificato: `convert_akomantoso.py:6-56,117-130`

### Verifiche Output Markdown (VERIFICATION_TASKS.md)

- Eseguita verifica completa su CAD (D.Lgs. 82/2005)
- **PROBLEMA CONFERMATO**: Intestazioni Capo/Sezione
  - XML combina "Capo I ... Sezione I ..." in un unico `<heading>`
  - Web normattiva.it visualizza su righe separate con gerarchia
  - Nostro MD mostra tutto su una riga → scarsa leggibilità
  - Fix proposto: Splittare heading con regex pattern matching
- **NON È PROBLEMA**: Testo "0a) AgID"
  - Presente anche su web ufficiale, non è testo abrogato
- **NON È PROBLEMA**: Testo mancante preambolo
  - "Sulla proposta..." presente correttamente nel CAD
- Creato `VERIFICATION_REPORT.md`: analisi dettagliata con proposte di fix
- Priorità fix: ALTA per heading Capo/Sezione

### Nuovo Metodo Fetch da URL

- Creato `fetch_from_url.py`: script per scaricare e convertire norme direttamente da URL normattiva.it
- Implementato parser HTML per estrarre parametri (dataGU, codiceRedaz, dataVigenza) da input hidden
- Usato `requests.Session()` per mantenere cookies e simulare browser
- Validazione risposta XML prima di salvare il file
- Debug mode: salva risposta HTML in caso di errore
- Test riusciti con URL multipli:
  - Legge 53/2022
  - Decreto Legislativo 36/2006
- Aggiornati README.md e CLAUDE.md con nuovo workflow URL-based (consigliato)
- Creato CLAUDE.md per future istanze di Claude Code

### Documentazione URL Completa

- Creato `URL_NORMATTIVA.md`: guida completa alla struttura degli URL normattiva.it
- Documentati formati URN per: decreto.legge, legge, decreto.legislativo, costituzione
- **Sintassi avanzata documentata**:
  - Modalità visualizzazione: `@originale`, `!vig=`, `!vig=AAAA-MM-GG`
  - Puntamento articoli: `~artN`, `~artNbis`, `~artNter`, etc.
  - Tutte le combinazioni possibili (8 pattern principali)
  - Tabella estensioni articoli (bis, ter, quater...quadragies)
- **Test di compatibilità riusciti**:
  - URL con `@originale` → ✅
  - URL con `~art2!vig=2009-11-10` → ✅ (dataVigenza correttamente estratta)
  - Conferma: `fetch_from_url.py` supporta tutte le sintassi avanzate
- Avvertenze su ambiguità URN e articoli inesistenti
- Creato `test_url_types.sh`: script di test automatico per diversi tipi di URL
- Aggiornato `.gitignore`: esclusi test_output/, temp_*.xml, *.debug.html

## 2025-07-18

### Inizializzazione e Setup

- Analisi iniziale dei file Python e creazione del `PRD.md`.
- Aggiornamento del `PRD.md` per riflettere l'obiettivo di conversione delle norme di `normattiva.it` per LLM/AI.
- Riorganizzazione dei file di test: eliminazione degli output `.md` dalla root, creazione della directory `test_data/` e spostamento del file XML di esempio al suo interno, con aggiunta di `README.md` esplicativo.
- Configurazione Git: inizializzazione del repository, creazione di `.gitignore` (escludendo build, compilati, temporanei e `*.xml:Zone.Identifier`) e `.gitattributes` (normalizzazione fine riga `eol=lf`).
- Aggiornamento del `README.md` iniziale per allinearlo all'obiettivo del progetto.
- Creazione del `LOG.md` per tracciare gli avanzamenti.

### Tentativo di Refactoring con JSON Intermedio

- Rinominato `convert_akomantoso.py` a `convert_json_to_markdown.py` per un approccio JSON-centrico.
- Riscritto `convert_json_to_markdown.py` per accettare JSON (output di `tulit`) e generare Markdown.
- Aggiornato `fetch_normattiva.py` per una pipeline XML -> JSON (tulit) -> Markdown (nostro script).
- Aggiornato `setup.py` per riflettere il nuovo nome del modulo.

### Ripristino e Correzioni

- Decisione di ripristinare la pipeline XML-to-Markdown diretta per maggiore controllo sulla formattazione.
- Rinominato `convert_json_to_markdown.py` a `convert_akomantoso.py`.
- Ripristinato il contenuto di `convert_akomantoso.py` alla sua versione originale (XML-based) e applicate correzioni di sintassi/indentazione.
- Aggiornato `fetch_normattiva.py` per chiamare direttamente `convert_akomantoso.py` per l'output Markdown.
- Aggiornato `setup.py` per riflettere il ripristino del nome del modulo.
- Eseguito con successo il test di conversione Markdown con la pipeline ripristinata.

### Gestione File di Output

- Rimossi tutti i file `output*.md` dalla root del progetto.
- Aggiunto il pattern `output*.md` al `.gitignore`.
- Committate e pushate le modifiche.
