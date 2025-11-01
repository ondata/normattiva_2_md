# LOG.md - Registro degli Avanzamenti del Progetto

Questo file documenta gli avanzamenti significativi e le decisioni chiave del progetto `normattiva_2_md`.

## 2025-11-02

### ✅ Aggiunto flag --version/-v

- Implementato flag CLI per mostrare versione pacchetto
- Argparse action='version' con VERSION constant
- Exit automatico senza conversione
- Tests: flag lungo, corto, precedenza su input

## 2025-01-11

### 🔒 Release v1.4.2: Security Hardening

**Security release**: Risolte vulnerabilità critiche e implementate misure di protezione

#### 🔐 Fix Sicurezza Critici

- **URL validation**: Solo domini normattiva.it whitelisted, HTTPS obbligatorio
- **Path traversal protection**: Sanitizzazione path output con validazione directory traversal
- **XML bomb protection**: Limite 50MB file size, controllo pre-parsing
- **Secure HTTP**: SSL verification esplicita (`verify=True`), User-Agent corretto
- **Tempfile security**: Sostituito naming manuale con module `tempfile` Python

#### ✅ Miglioramenti Codice

- **Dead code removed**: Eliminata funzione `downgrade_headings()` non utilizzata
- **Security constants**: Definite costanti modulo per limiti e configurazione
- **User-Agent corretto**: Da browser-impersonation a `Akoma2MD/version`
- **Timeout configuration**: Estratta costante `DEFAULT_TIMEOUT = 30`

#### 🧪 Testing Sicurezza

- **11 nuovi test security**: Copertura validazione URL, path sanitization, file limits
- **Test URL rejection**: Verifica reject HTTP, domini non autorizzati, URL malformati
- **Test path traversal**: Verifica blocco tentativi accesso `/etc`, `/sys`, path con `..`
- **Test file limits**: Validazione costanti size limit corrette

#### 📚 Documentazione

- **SECURITY.md creato**: Policy sicurezza, supported versions, responsible disclosure
- **Security features documented**: Whitelisted domains, protection measures, best practices
- **Changelog sicurezza**: Documentate tutte le fix v1.4.2

#### 🔧 Breaking Changes

**NESSUNO**: Tutte le modifiche backward-compatible, validano solo input pericolosi

#### 📊 Impatto

- **Linee codice modificate**: ~150 (aggiunte security functions, aggiornati HTTP requests)
- **Performance overhead**: <1ms per validazione, impatto negligibile
- **Test suite**: 14→25 tests (11 security tests aggiunti), 25/25 passing

## 2025-11-01

### 📝 Release v1.4.1: Aggiornamento Documentazione

**Patch**: README aggiornato con esempio output gerarchia corretta

#### ✅ Modifiche
- Aggiornato esempio output README con gerarchia v1.4.0
- Descrizione dettagliata livelli heading (H1→H2→H3→H4)
- Enfasi su "machine-to-machine ready"

### 🎉 Release v1.4.0: Gerarchia Heading Strutturata Machine-to-Machine

**Breaking Change**: Implementato parser intelligente per gerarchia logica libro-style

#### ✅ Parsing Intelligente XML
- Analizzato XML: Capo e Sezione sono entrambi `<chapter>`, gerarchia nel testo `<heading>`
- Parser testuale estrae struttura: "Capo X TITOLO Sezione Y TITOLO_SEZ"
- Ricostruita gerarchia logica da heading flat XML

#### ✅ Gerarchia Corretta Book-Style
- **H1**: Titolo documento legge
- **H2**: Capo (capitolo principale)
- **H3**: Sezione (sotto-capitolo)
- **H4**: Articoli (contenuto)
- Rimosso downgrade globale, livelli assegnati durante parsing

#### ✅ Esempi Output
```markdown
# Codice dell'amministrazione digitale.
## Capo I - PRINCIPI GENERALI
### Sezione I - Definizioni, finalita'...
#### Art. 1. - Definizioni
```

#### 🔧 Modifiche Tecniche
- `parse_chapter_heading()`: ritorna `{'type', 'capo', 'sezione'}`
- `process_chapter()`: assegna livelli H2/H3/H4 in base a tipo
- Test aggiornati per nuova gerarchia

### 🎉 Release v1.3.5: Correzione Indentazione Downgrade Heading

**Bugfix**: Risolto errore indentazione nella funzione `downgrade_headings()`

#### ✅ Fix Tecnici
- Corretta indentazione blocco if/else in `downgrade_headings()`
- Ripristinato comportamento corretto downgrade heading
- Tutti i test passati dopo fix

#### 📦 Build e Distribuzione
- Creato eseguibile standalone v1.3.5
- Generati pacchetti PyPI (wheel e tar.gz)

### 🎉 Release v1.3.4: Ristrutturazione Gerarchia Markdown

**Rifacimento struttura**: Downgrade globale di tutti gli heading per gerarchia logica

#### ✅ Struttura Markdown Ottimizzata
- **Front matter + H1**: Documento inizia con front matter e H1 per titolo legge
- **Downgrade globale**: Tutti gli heading abbassati di 1 livello (H3→H2, H4→H3, etc.)
- **Gerarchia logica**: H1 (titolo) > H2 (capi) > H3 (sezioni) > H2/H3 (articoli)
- **Mantenimento struttura XML**: La gerarchia originale è preservata, solo livelli Markdown aggiustati

#### ✅ Miglioramenti Qualità
- **Consistenza sezioni**: Capitoli con "Sezione" ora uniformemente a H3 dopo downgrade
- **Leggibilità LLM**: Struttura più naturale per modelli di linguaggio
- **Standard Markdown**: Nessun salto di livelli (H1 poi H3)

#### 🧪 Testing e Qualità
- Aggiornati test per riflettere nuova gerarchia
- Tutti i test passati
- Nessuna regressione nelle funzionalità

### 🎉 Release v1.3.2: Correzione Gerarchia Heading

**Fix gerarchico**: Articoli ora rispettano la struttura documentale corretta

#### ✅ Gerarchia Heading Corretta
- **Articoli contestuali**: Gli articoli ora usano il livello corretto a seconda del contesto
- **Corretto H2→H3**: Articoli dentro capitoli ora H3 invece di H2
- **Corretto H2→H4**: Articoli dentro sezioni ora H4
- **Struttura logica**: Capitoli (H3) > Articoli (H3) > Sezioni (H4) > Articoli in sezioni (H4)

#### 🧪 Testing e Qualità
- Aggiornati test per riflettere la nuova gerarchia
- Verifica struttura documentale corretta
- Tutti i test passati

## 2025-11-01

### 🎉 Release v1.3.1: Output Pulito e Formattazione Migliorata

**Ottimizzazione UX**: Output silenzioso per stdout, formattazione front matter migliorata

#### ✅ Output Silenzioso per Stdout
- **Rimossi messaggi verbosi**: Quando output va su stdout, solo markdown senza messaggi di progresso
- **Preservati messaggi**: Quando output su file, messaggi di progresso ancora visibili
- **Flag quiet rispettato**: Logica migliorata per gestire diversi scenari di output

#### ✅ Formattazione Front Matter
- **Riga vuota aggiunta**: Spazio tra chiusura front matter e primo heading
- **Migliore leggibilità**: Separazione chiara tra metadati e contenuto

#### 🧪 Testing e Qualità
- Test di regressione completati
- Verifica output silenzioso funzionante
- Formattazione front matter corretta

## 2025-11-01

### 🎉 Release v1.3.0: Miglioramento Struttura Documenti e Metadati

**Ottimizzazione per LLM**: Struttura Markdown migliorata con front matter e gerarchia heading ottimizzata per modelli linguistici

#### ✅ Front Matter YAML
- **Metadati strutturati**: Aggiunto front matter YAML con campi `url`, `url_xml`, `dataGU`, `codiceRedaz`, `dataVigenza`
- **Estrazione automatica**: Implementata estrazione metadati da XML Akoma Ntoso e parametri URL
- **Costruzione URL**: Generazione automatica degli URL normattiva.it dal metadati estratti

#### ✅ Gerarchia Heading Riadattata
- **Titolo principale H1**: Il titolo della norma rimane prominente come H1
- **Struttura ottimizzata**: Tutti gli elementi strutturali abbassati di un livello per migliore leggibilità
- **Progressione logica**: H1 (titolo) → H2 (articoli) → H3 (capitoli/parti) → H4 (sezioni)

#### 🧪 Testing e Qualità
- Aggiornati tutti i test esistenti per riflettere i nuovi livelli heading
- Aggiunti test completi per generazione front matter e estrazione metadati
- Suite di test completa: 14/14 tests passati
- Verifica end-to-end della conversione con metadati

#### 📚 Documentazione
- Aggiornato README.md con descrizione delle nuove funzionalità
- Aggiornato PRD.md con requisiti implementati
- Implementazione completa del change proposal OpenSpec

## 2025-11-01

### Riorganizzazione documentazione e script

- Creati `docs/` e `scripts/` per raccogliere rispettivamente documentazione ausiliaria e utility shell.
- Spostati `AGENTS.md`, `CLAUDE.md`, `COMPATIBILITY_ROADMAP.md`, `PRD.md`, `URL_NORMATTIVA.md` in `docs/`.
- Spostati `build_distribution.sh`, `test_compatibility.sh`, `test_url_types.sh` in `scripts/`.
- Aggiornati riferimenti in `README.md` e `docs/AGENTS.md` alle nuove posizioni; `LOG.md` e `VERIFICATION.md` restano in root come da linee guida.

### Automazione release binarie

- Aggiunto workflow GitHub Actions `Build Releases` (`.github/workflows/release-binaries.yml`) per creare e impacchettare eseguibili PyInstaller Linux/Windows ad ogni tag `v*` o esecuzione manuale
- Verifiche incluse nel workflow: `make test` su Linux, unittest + run CLI/exe su Windows
- Asset generati: `akoma2md-<version>-linux-x86_64.tar.gz` e `akoma2md-<version>-windows-x86_64.zip` pubblicati automaticamente nelle release taggate
- Aggiornato `README.md` con procedura operativa per pubblicare nuovi binari
- Incrementata versione progetto a `1.1.3` (`setup.py`, `pyproject.toml`) in preparazione alla release
- Eseguite release `v1.1.3-rc1` (pre-release) e `v1.1.3` tramite workflow; confermata pubblicazione asset Linux/Windows su GitHub Releases

### README: rimossi riferimenti release inesistenti

- Rimossa sezione "Eseguibile Standalone" con link a release inesistenti
- Riorganizzati metodi installazione: uv (raccomandato), pip, esecuzione diretta
- Chiarito che build pyinstaller è opzionale per uso locale

### Consolidamento Documentazione Verifiche

- Uniti `VERIFICATION_TASKS.md` e `VERIFICATION_REPORT.md` → `VERIFICATION.md`

### 🎉 Release v1.2.0: Supporto Elementi Avanzati Akoma Ntoso

**Compatibilità aumentata**: da 80-85% a **95-98%** dei documenti Normattiva testati

#### ✅ FASE 1: Quick Wins Completata
- **Note a piè di pagina** (`<akn:footnote>`): Implementato supporto con riferimenti semplificati
- **Citazioni** (`<akn:quotedStructure>`): Convertite in blockquote Markdown (`> testo`)
- **Tabelle** (`<akn:table>`): Conversione base a formato pipe-separated Markdown
- **Riferimenti normativi** (`<akn:ref>`): Supporto già presente, confermato funzionante

#### ✅ FASE 2: Strutture Gerarchiche Completata
- **Titoli** (`<akn:title>`): Render come H1 top-level con contenuto annidato
- **Parti** (`<akn:part>`): Render come H2 con supporto per chapters/articles annidati
- **Allegati** (`<akn:attachment>`): Render come sezione separata dedicata
- **Ottimizzazioni**: Migliorato parsing heading per evitare duplicazioni

#### 🧪 Testing e Qualità
- Aggiunti 6 nuovi test unitari per elementi avanzati
- Verificata retrocompatibilità con documenti esistenti
- Tutti test passano senza regressioni
- Aggiornato `COMPATIBILITY_ROADMAP.md` con stato corrente

#### 📦 Preparazione Release
- Incrementata versione progetto a `1.2.0` (`pyproject.toml`, `setup.py`)
- Aggiornato changelog con dettagli implementazione
- Pronto per tag `v1.2.0` e pubblicazione PyPI/GitHub Releases
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
