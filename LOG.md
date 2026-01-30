# LOG.md - Registro degli Avanzamenti del Progetto

Questo file documenta gli avanzamenti significativi e le decisioni chiave del progetto `normattiva_2_md`.

## 2026-01-30

### Release v2.1.10: Progressive OpenData Fallback Retry

- Implementata strategia di retry progressiva per OpenData API
- Primo tentativo: ricerca con filtri completi (data inizio/fine + numero + anno)
- Fallback automatico: senza filtri data se primo tentativo fallisce o senza risultati
- Risolve issue #23: documenti (es. L. 118/2022) che prima fallivano con errore HTML
- Retry logic: gestisce sia errori di download che ZIP non valido
- Messaggi progressivi: avviso utente quando passa al fallback senza data
- Fix field API: da `dataInizioPubblicazione`/`dataFinePubblicazione` (corretti per OpenData)

## 2026-01-29

### Fix messaggi di progresso fallback OpenData

- Rimosso messaggio di errore fuorviante quando link caricaAKN non disponibile
- Sostituito con messaggio informativo: "⚠️ Link caricaAKN non trovato, tentativo con fallback..."
- Aggiunti indicatori di progresso per download via OpenData:
  - Messaggio iniziale "🔄 Tentativo download via API OpenData..."
  - Indicatore animato "⏳ Preparazione collezione OpenData..." con puntini durante polling
  - Messaggio di successo "✅ File XML (OpenData) salvato in: ..."
- Modificato quiet mode: messaggi di progresso visibili su stderr anche quando output va a stdout
- Messaggi soppressi solo con flag --quiet esplicito
- Fix UX: utente ora vede chiaramente che download è in corso, evita confusione su comando bloccato

## 2026-01-12

### URL con escape backslash

- Normalizzazione URL normattiva.it con backslash in CLI/API
- Aggiornati test sicurezza per URL con escape

### Documentazione release

- Aggiunta sezione GitHub Release in DEVELOPMENT.md

## 2026-01-11

### Coverage Reporting Implementation

- Configurato pytest-cov per reporting coverage
- **Coverage attuale: 40%** (1763 statements, 703 coperti)
- Moduli eccellenti (≥90%): validation.py (95%), exceptions.py (100%), constants.py (100%)
- Moduli critici con basso coverage: api.py (14%), cli.py (21%), normattiva_api.py (32%), xml_parser.py (47%)
- Aggiunta configurazione in `pyproject.toml` per pytest e coverage.py
- Documentazione coverage in `DEVELOPMENT.md` con comandi quick-start
- Analisi dettagliata gap in `tmp/coverage_analysis.md`
- Report HTML interattivo generato in `htmlcov/`
- Target prossimo sprint: 60-70% coverage
- .gitignore già configurato per htmlcov/ e .coverage
- **Aggiornato** `docs/evaluation-v2.1.5.md` con sezione update e raccomandazione #1 completata

### Project Evaluation v2.1.5

- Valutazione completa codebase senza consultare valutazioni precedenti
- Analisi strutturata: architettura, qualità codice, test, documentazione, sicurezza, performance
- Creato `docs/evaluation-v2.1.5.md` con assessment dettagliato
- Overall Grade: A- (89/100)
- Punti di forza: architettura pulita, documentazione eccellente, production-ready
- Aree miglioramento: test coverage, complessità codice, tooling (linting/mypy)
- Research notes persistite in `tmp/research_notes.md` con ipotesi competitive e livelli di confidenza

## 2026-01-06

### Pre-lancio newsletter: Aggiornamento documentazione sviluppo

- **DEVELOPMENT.md**: Aggiornata struttura progetto da `convert_akomantoso.py` (obsoleto) a `__main__.py` + `src/normattiva2md/`
- **Workaround cross-device link**: Aggiunta soluzione `TMPDIR=$PWD/tmp pip install -e .` per WSL/Linux con `/tmp` su filesystem diverso
- **EXA_API_KEY**: Documentati warning test opzionali e come configurare API key
- Progetto pronto per lancio pubblico via newsletter

## 2026-01-02

### Fix CI Test Failures + Documentation

- Fixed failing tests: `test_generate_front_matter_complete` e `test_generate_front_matter_partial` non erano sincronizzati con legal_notice introdotto in v2.1.5
- Updated tests per includere legal_notice negli expected outputs
- **Importante**: Documentazione aggiornata per richiedere sempre uso di `.venv` per build/test/publish per evitare binary bloat
  - DEVELOPMENT.md: Aggiunto avvertimento CRITICAL sulla necessità di usare venv
  - CLAUDE.md: Aggiunta sezione "Development Environment" con reference a DEVELOPMENT.md

## 2026-01-01

### 🚀 Lancio Pubblico - Normattiva2MD Pronto per il Mondo

**Attività completate per il lancio ufficiale:**
- ✅ **Coerenza configurazione**: Aggiornato setup.py per sincronizzare con pyproject.toml (name="normattiva2md")
- ✅ **PyPI**: v2.1.4 già pubblicato e disponibile via `pip install normattiva2md`
- ✅ **GitHub Release**: v2.1.4 già pubblicato con binari per Linux e Windows
- ✅ **Documentazione cittadini**: Creato `docs/QUICKSTART.md` con guida in italiano per uso pratico
- ✅ **Piano di lancio**: Creato `docs/LAUNCH_ANNOUNCEMENT.md` con strategia multicanale

**Cosa è pronto:**
- Progetto completo, testato, con all'attivo 27+ feature implementate
- Documentazione tecnica (README, API docs, OpenSpec specs)
- Documentazione per utenti non-tech (guida quick-start con esempi)
- Binari standalone per cittadini senza Python

**Prossimi step (suggeriti):**
1. Condividi su GitHub Discussions e forum tech italiani
2. Tweet su Twitter/X con i template forniti
3. Contatta comunità open data (OnData, Docs Italia)
4. Annuncia a professori universitari, ricercatori
5. Raccogli feedback per prossime versioni

**Valore proposto:**
- Per cittadini: Leggi italiane leggibili e analizzabili
- Per AI enthusiast: Leggere leggi in ChatGPT/Claude
- Per ricercatori: Strumento open source per analisi normative
- Per developer: API Python + CLI + cross-references

## 2026-01-01

### Release v2.1.4 - Supporto Type Hints per IDE

**Miglioramento esperienza sviluppo**:
- Aggiunto `py.typed` marker per abilitare type hints in IDE (VSCode, PyCharm, etc.)
- Creato `MANIFEST.in` per includere py.typed nel pacchetto distribuito
- Docstring complete già presenti ora mostrate automaticamente con autocompletamento
- Type checking supportato con mypy per code validation

**Documentazione API**:
- Aggiornato `openspec/project.md` con dipendenze Rich, flag --art e API programmabile
- Archiviate 4 proposte OpenSpec completate (add-article-filter-flag, add-project-site-ghpages, improve-cli-help-output, update-site-api-21)
- Specifiche aggiornate: cli-interface, markdown-conversion, project-website

## 2026-01-01

### Release v2.1.3 - Miglioramento Help CLI

**Help con pager interattivo**:
- Aggiunto pager automatico per `--help` (navigazione con ↑↓ PgUp/PgDn, esci con `q`)
- Spaziatura migliorata tra sezioni Options per maggiore leggibilità
- Footer con istruzioni di navigazione del pager
- Aggiunto flag `-h, --help` nella documentazione help

## 2026-01-01

### Documentazione API OpenData - Struttura Versionata

**Organizzazione documentazione API OpenData Normattiva**:
- Creata struttura `docs/api-opendata/` con documentazione completa API M2M
- Spostati 3 file MD da `docs/` e `tmp/` → `docs/api-opendata/`
- Creata sottocartella `scripts/` con test funzionanti (3 script Python/Bash)
- Creata sottocartella `output/` per risultati test (non versionata)
- Aggiunto `README.md` con guida completa workflow API

**Correzioni API dopo test**:
- Endpoint `/ricerca/semplice` funzionante ✅ (errori iniziali: URL incompleto, header mancante, paginazione obbligatoria)
- Workflow completo testato: Ricerca → Dettaglio → HTML → Markdown
- Eliminata necessità di parsing URL con approccio API-first

**Script aggiornati a path relativi**:
- `test_workflow_completo_funzionante.py`: usa `OUTPUT_DIR` relativo a script
- `api_html_to_markdown.py`: converter HTML→MD con path relativi
- `test_dettaglio.sh`: bash test con output relativo
- Tutti i riferimenti `tmp/` sostituiti con `scripts/` e `output/`

**File modificati**:
- `.gitignore`: aggiunta `docs/api-opendata/output/`
- 3 MD file: aggiornati path da `tmp/` a `scripts/`/`output/`
- 3 script: convertiti da path assoluti a relativi

## 2026-01-01

### Refactoring: Uniformazione Chiamate Funzioni

**Code cleanup e miglioramenti manutenibilità**:
- Uniformate chiamate a `convert_akomantoso_to_markdown_improved()` con keyword arguments
- Rimosse ridefinizioni multiple di `quiet_mode` (definito una sola volta)
- Rimosso `getattr()` non necessario per `article_filter`
- File modificati: `cli.py`, `multi_document.py`, `test_cli_validation.py`

**Problemi risolti**:
1. Parametro `article_ref` inconsistente (posizionale vs keyword) → uniformato con keyword
2. Variabile `quiet_mode` ridefinita 3 volte → definita una sola volta all'inizio
3. Uso non necessario di `getattr()` → accesso diretto all'attributo + fix test mock

**Impatto**:
- Codice più robusto e manutenibile
- Nessun breaking change per API Python
- 53/53 test passati

## 2026-01-01

### Release v2.1.1 - Bug Fix

**Patch release**: Corretto NameError critico che impediva l'uso da URL normattiva.it

**Fix implementato:**
- Risolto NameError nella funzione di completamento forzato (issue #16)
- Il bug impediva il download automatico da URL normattiva.it
- Fix mergiato in PR #18
- Versione bumped: v2.1.0 → v2.1.1

**Distribuzione:**
- GitHub Release: https://github.com/ondata/normattiva_2_md/releases/tag/v2.1.1
- PyPI: https://pypi.org/project/normattiva2md/2.1.1/

## 2026-01-01

### Aggiornamento ROADMAP + Fix CI + Release v2.1.0

**ROADMAP.md aggiornata**:
- Versione corrente: v2.0.24 → v2.1.0
- Sezione "✅ COMPLETATO - v2.1.0": API Python documentata
- 4 feature non implementate spostate in v2.2.0 (HTML parsing, Network retry, Footnote, Regex)
- Timeline aggiornata: Q1-Q4 2026
- EUR-Lex Integration confermata per v2.4.0

**Fix GitHub Actions CI**:
- Convertito `test_api.py` da pytest a unittest
- Problema: pytest non installato in workflow
- Soluzione: unittest (già disponibile, usato da altri test)
- 15/15 test passano localmente

**Release v2.1.0 pubblicata**:
- Tag v2.1.0 ricreato su commit con fix (5e8e8d5)
- Build GitHub Actions: ✓ Success (Linux 40s, Windows 1m1s)
- Release pubblicata: https://github.com/ondata/normattiva_2_md/releases/tag/v2.1.0
- Binari disponibili: Linux (tar.gz), Windows (zip)
- Marcata come "Latest" su GitHub

## 2026-01-01

### Environment cleanup

- rimosso `venv` obsoleto
- aggiornato README.md: usa `.venv` standard
- creato DEVELOPMENT.md con setup chiaro e comandi test

### API Programmabile Python

**v2.1.0**

Aggiunta API Python per uso in notebook e script, mantenendo 100% compatibilità CLI.

**Nuovi file**:
- `src/normattiva2md/api.py`: funzioni standalone e classe Converter
- `src/normattiva2md/models.py`: dataclass ConversionResult e SearchResult
- `src/normattiva2md/exceptions.py`: gerarchia eccezioni custom
- `examples/basic_usage.py`: esempi uso base
- `examples/batch_processing.py`: esempi batch
- `tests/test_api.py`: test suite API (15 test)

**Funzioni pubbliche**:
- `convert_url(url, article, with_urls, quiet)` → ConversionResult
- `convert_xml(xml_path, article, with_urls, metadata, quiet)` → ConversionResult
- `search_law(query, exa_api_key, limit, quiet)` → List[SearchResult]
- `Converter` class per configurazione persistente e batch

**Eccezioni**:
- `Normattiva2MDError` (base)
- `InvalidURLError`, `XMLFileNotFoundError`, `APIKeyError`, `ConversionError`

**Esempio uso**:
```python
from normattiva2md import convert_url

result = convert_url("https://www.normattiva.it/...")
print(result.title)
result.save("output.md")
```

**Documentazione**: README.md aggiornato con sezione "Utilizzo come Libreria Python"

---

## 2025-12-27

### Implementazione flag `--art` per filtro articoli

**v2.0.24** | **OpenSpec**: `add-article-filter-flag`

Aggiunto parametro CLI `--art` per filtrare singoli articoli senza modificare URL:

**Implementazione**:
- `construct_article_eid()` in `xml_parser.py`: converte input utente (es: "4", "16bis") → eId Akoma ("art_4", "art_16-bis")
- Integrazione in `cli.py`: gestisce priorità `--art` > `--completo` > URL `~artN`
- Supporto estensioni: bis, ter, quater, quinquies, etc. (case-insensitive)
- Warning stderr se articolo non trovato, output con solo metadata

**Esempi uso**:
- `normattiva2md --art 4 input.xml output.md`
- `normattiva2md --art 16bis "URL" output.md`
- `normattiva2md --art 3 "URL~art5"` → override, mostra art. 3

**Documentazione aggiornata**: README.md, CLAUDE.md

**Test**: File locale, URL, estensioni, override ~artN, articolo inesistente

**Validazione**: `openspec validate add-article-filter-flag --strict` → PASS

---

### Fix ricerca naturale Exa e UX interattiva

**v2.0.23**

- Filtro risultati Exa: esclusi URL `/esporta/` non supportati e titoli con "errore"
- Gestione CTRL+C pulita in tutti gli input interattivi (ricerca, nome file, sovrascrittura)
- Prompt nome file migliorato: "(INVIO per confermare, o scrivi nome desiderato)"
- Fix carriage return `\r` per nascondere `^C` visibile

## 2025-12-25

### 📊 Analisi schema dati violenza di genere

**Attività**: Analisi comparativa normativa e integrazione schema dati

#### Documenti prodotti
- `tasks/email_riganelli/email_schema_dati.qmd`: Schema dati basato su Legge 53/2022 (aggiornato con campi età/genere mancanti)
- `tasks/email_riganelli/suggerimenti_direttiva_ue.md`: Analisi Direttiva UE 2024/1385 vs Legge IT
- `tasks/email_riganelli/spunti_ricerca_sapienza.md`: Spunti da ricerca Sapienza + risorse internazionali

#### Correzioni schema dati
- Aggiunto campo `eta_vittima` e `genere_vittima` alla tabella Vittima (Sistema Interministeriale)
- Aggiunto campo `relazione_autore_vittima`, `eta_autore`, `genere_autore` alla tabella Denunce
- Conformità con Art. 5 comma 1 Legge 53/2022

#### Gestione cardinalità (schema LONG)
- Aggiunta sezione metodologica con esempi pratici (violenza di gruppo, maltrattamenti familiari)
- **Dataset 1 "Centro Elaborazione Dati"** aggiornato con identificativi anonimi:
  - `id_evento`: episodio di violenza
  - `id_vittima_anonimizzato`: persona vittima (hash anonimizzato)
  - `id_autore_anonimizzato`: autore del reato (hash anonimizzato)
- Schema LONG permette di gestire N autori → 1 vittima, 1 autore → N vittime, reati multipli
- Aggiunto campo `data_fatto` per tracciare temporalmente gli eventi

#### Semplificazione Sistema Interministeriale
- **Dataset 2 "Sistema Interministeriale"** drasticamente semplificato:
  - Da 8 tabelle (1 principale + 7 correlate) a **1 singola tabella LONG**
  - Ogni riga = 1 evento procedurale nel percorso della vittima
  - Campi chiave: `id_vittima_anonimizzato`, `id_evento_procedurale`, `tipo_evento`, `tipo_reato`, `data_evento`
  - 10 tipi di evento: Denuncia, Misure (prevenzione/precautelari/cautelari/sicurezza), Ordini protezione, Violazioni, Arresti, Archiviazioni, Sentenze
  - Aggiunto campo `tipo_reato` per collegare eventi procedurali ai reati specifici
- Aggiunta premessa con esempio concreto di percorso vittima (8 eventi in timeline)
- Tabella esempio con 8 righe che mostrano il percorso completo dalla denuncia alla sentenza d'appello
- Nota finale spiega gestione di denunce multiple per reati diversi

#### Spunti da Direttiva UE 2024/1385
- 11 nuovi campi proposti (abuso sostanze autore, convivenza, disabilità vittima, gravidanza, etc.)
- Nuova tabella "Violazioni Ordini di Protezione" (Art. 19 UE)
- Dati aggregati: capacità case rifugio, chiamate 1522 (Art. 44 UE)
- Scadenza recepimento: 14 giugno 2027

#### Spunti da ricerca Sapienza
- Classificazione IPF (Intimate Partner Femicide) come campo aggiuntivo
- Metriche accessibilità geografica CAV (distanza, tempi percorrenza)
- Allineamento con dati Ministero Interno (già raccolti, non pubblicati in formato strutturato)
- Best practice internazionali: Spagna, UK, Messico

## 2025-12-03

### 🚀 Release v2.0.22: Export provvedimenti attuativi

**New feature**: Export legislative implementation measures (provvedimenti attuativi) to CSV

#### Changes
- New module `provvedimenti_api.py`: fetch and parse from programmagoverno.gov.it
- CLI: added `--provvedimenti` parameter (requires normattiva.it URL)
- CSV export: 7 columns (dettagli, governo, fonte_provvedimento, oggetto, provvedimento_previsto, adozione, link_al_provvedimento)
- Automatic pagination handling
- UTF-8 encoding
- File naming: `{anno}_{numero}_provvedimenti.csv`

#### Usage
```bash
normattiva2md --provvedimenti "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2024;207" legge.md
# Generates: legge.md + 2024_207_provvedimenti.csv
```

#### Credits
Feature request by Damiano Sabuzi Giuliani (issue #10)

## 2025-12-02

### 🔧 Fix GitHub Pages: Workflow Jekyll 4.3 via Actions

**Problema risolto**: GitHub Pages non supporta Jekyll 4.3 nel Gemfile

#### Soluzione implementata
- Creato workflow `.github/workflows/jekyll.yml` per build e deploy via Actions
- Usa Ruby 3.3 e dipendenze dal `docs/Gemfile`
- Build in ambiente production con baseurl dinamico
- Deploy automatico su push a main

#### Configurazione richiesta
Nelle impostazioni GitHub del repo (Settings > Pages):
- Source: "GitHub Actions"

## 2025-11-04

### 🚀 Release v2.0.7: Added Permanent Link Field to Frontmatter

**New feature**: Added `url_permanente` field to YAML frontmatter with clean URN-style URLs including vigenza date

#### 🎯 Problem Solved
- **Issue**: No clean, permanent link format in frontmatter for sharing/archiving
- **Impact**: Users couldn't easily get a standardized permanent URL for documents
- **Need**: Clean URN URLs like `https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2023-11-24;168!vig=2025-11-04`

#### 🔧 Changes Made
- **New `build_permanent_url()` function**: Constructs URN URLs with vigenza date parameter
- **Updated metadata extraction**: Added `url_permanente` field using canonical URN-NIR from XML
- **Enhanced frontmatter**: `url_permanente` now included in YAML output alongside existing URL fields
- **Canonical URN extraction**: Extracts URN-NIR from `<FRBRalias name="urn:nir">` in XML instead of constructing it
- **Format**: `{canonical_urn}!vig={vigenza_date}` using the official URN-NIR with vigenza parameter

#### 📊 Example Output
```yaml
---
url: https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2005-03-07;005G0104
url_xml: https://www.normattiva.it/do/atto/caricaAKN?dataGU=20050307&codiceRedaz=005G0104&dataVigenza=20250130
url_permanente: https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2005-03-07;82!vig=2025-01-30
dataGU: 20050307
codiceRedaz: 005G0104
dataVigenza: 20250130
---
```

## 2025-11-04

### 🚀 Release v2.0.6: Cleaner Search Output & Improved UX

**UX enhancement release**: Reduced verbose output in normal mode for cleaner user experience

#### 🎯 Problem Solved
- **Issue**: Search output was too verbose in normal mode, showing detailed results even when not in debug mode
- **Impact**: Users saw unnecessary technical details during normal searches
- **Example**: Normal searches showed "Risultati ricevuti da Exa (5):" and detailed result lists

#### 🔧 Changes Made
- **Conditional debug output**: Results listing now only shown when `--debug-search` flag is used
- **Cleaner normal mode**: Regular searches show only essential information
- **Preserved debug functionality**: `--debug-search` still shows full Exa API responses and selection details
- **Maintained conversion messages**: URL conversion notifications still appear when relevant

#### 📊 Technical Details
- **Output logic**: Added `if debug_json:` condition around verbose result display
- **Preserved functionality**: All search logic and scoring unchanged
- **Backward compatibility**: Debug mode works exactly as before

#### ✅ Validation
- **Normal mode**: `normattiva2md -s "violenza donne"` shows clean output
- **Debug mode**: `normattiva2md -s "violenza donne" --debug-search` shows full details
- **Functionality preserved**: Search accuracy and URL conversion work identically
- **Suite test**: 27/27 tests passing without regressions

#### 📦 Distribution
- **PyPI Package**: `akoma2md` v2.0.6 with cleaner search output
- **GitHub Release**: v2.0.6 tag with improved user experience
- **Backward Compatibility**: All existing functionality preserved

## 2025-11-04

### 🚀 Release v2.0.5: Enhanced Exa Search Scoring & URL Conversion

**Search enhancement release**: Improved scoring algorithm for better law document selection and automatic URL conversion

#### 🎯 Problem Solved
- **Issue**: Exa API searches often returned article-specific URLs (`~art7`) instead of complete law documents
- **Impact**: Users searching for laws would get incomplete results pointing to single articles
- **Example**: Search for "Disposizioni urgenti per favorire lo sviluppo..." returned `~art7` instead of full decree-law

#### 🔧 Changes Made
- **Smart URL conversion**: When first search result is article-specific, automatically convert to complete law URL
- **Enhanced scoring logic**:
  - +20 bonus points for exact article matches when requested
  - -10 penalty for article URLs when complete law is desired
  - +10 bonus for first result when no article specified
  - Automatic conversion of first article-specific result to complete law
- **Article recognition**: Extended regex to detect "articolo 7", "art 7", "art. 7" and complex numbers like "16bis", "16ter", etc.
- **Debug features**: `--debug-search` flag shows full Exa API JSON response
- **Manual selection**: `--auto-select` flag allows manual result picking

#### 📊 Technical Details
- **URL pattern detection**: Detects `~art{N}` patterns and strips them to get base law URL
- **Priority logic**: First result gets special handling if it's article-specific
- **Scoring algorithm**: Preference score calculation based on article requests vs. complete law needs
- **Backward compatibility**: Existing searches work unchanged, improvements are automatic

#### ✅ Validation
- **Article Search**: `normattiva2md -s "legge art 7"` correctly selects article 7
- **Law Search**: `normattiva2md -s "costituzione italiana"` selects complete constitution (not article)
- **Debug Mode**: `--debug-search` shows full Exa API response
- **Auto-selection**: Works correctly for both article-specific and complete law searches
- **Suite test**: 27/27 tests passing without regressions

#### 📦 Distribution
- **PyPI Package**: `akoma2md` v2.0.5 with enhanced search capabilities
- **GitHub Release**: v2.0.5 tag with improved article recognition and scoring
- **Backward Compatibility**: All existing functionality preserved

## 2025-11-04

### 🔍 Improved Exa Search: Better Result Selection & Debug Features

**Version 2.0.4** - Enhanced search functionality with article-specific recognition

**Enhancement**: Fixed search functionality to properly handle article-specific URLs and added debug capabilities

#### 🎯 Problem Solved
- **Issue**: Exa API often returns article-specific URLs (e.g., `~art7`) instead of complete law URLs
- **Impact**: Users searching for laws would get incomplete results pointing to single articles
- **Example**: Search for "Disposizioni urgenti per favorire lo sviluppo..." returned `~art7` instead of full decree-law

#### 🔧 Changes Made
- **Smart URL conversion**: When first search result is article-specific, automatically convert to complete law URL
- **Article-specific search**: Recognize "articolo 7", "art 7", "art. 7" patterns to select specific articles
- **Extended article recognition**: Support for complex article numbers (16bis, 16ter, etc.) with multiple formats
- **Debug features**: Added `--debug-search` flag to show full Exa JSON response
- **Manual selection**: Added `--auto-select` flag (default true) to allow manual result picking
- **Improved scoring**: Enhanced preference algorithm to prioritize requested articles (+20 bonus) or complete laws

#### 📊 Technical Details
- **URL pattern**: Detects `~art{N}` patterns and strips them to get base law URL
- **Priority logic**: First result gets special handling if it's article-specific
- **Debug output**: Shows all search results with scores and allows user selection
- **Backward compatibility**: Existing searches work unchanged, improvements are automatic

**Breaking change**: Renamed command-line interface for better discoverability

#### 🎯 Motivation
- **Current name**: `akoma2md` was generic and didn't clearly indicate Italian legal document focus
- **New name**: `normattiva2md` better communicates the tool's specialization in normattiva.it documents
- **User impact**: Existing users will need to update scripts/commands

#### 🔧 Changes Made
- **Entry points**: Updated console_scripts in setup.py and project.scripts in pyproject.toml
- **Documentation**: Updated all README.md references, examples, and installation instructions
- **Branding**: Changed project title from "Akoma2MD" to "Normattiva2MD"
- **Build process**: Updated PyInstaller examples and release asset naming

#### ✅ Validation
- **Tests**: All existing tests pass, functionality unchanged
- **CLI**: New command `normattiva2md --help` works correctly
- **Conversion**: Basic XML conversion functionality verified

### 📦 Release v2.0.3: README Update on PyPI

**Metadata-only release**: Refresh PyPI package metadata

#### 🔧 Changes
- **PyPI Badge Fix**: Corrected README badge to point to `akoma2md` package on PyPI
- **Metadata Refresh**: Updated package description and README on PyPI
- **No Functional Changes**: Same dual CLI functionality as v2.0.2

#### 📦 Distribution
- **PyPI Package**: `akoma2md` v2.0.3 with corrected metadata
- **GitHub Release**: v2.0.3 tag for consistency

#### ✅ Verification
The README on PyPI now correctly shows:
- PyPI badge pointing to `akoma2md` package
- Installation instructions for `akoma2md` package
- Both `normattiva2md` and `akoma2md` CLI commands documented

### 🚀 Release v2.0.4: Enhanced Article Recognition in Search

**Enhancement release**: Improved search functionality with better article-specific recognition

#### 🔧 Changes
- **Article Pattern Recognition**: Extended regex to recognize "articolo 7", "art 7", "art. 7" and complex numbers like "16bis"
- **Smart Article Selection**: +20 bonus points for URLs containing the exact requested article
- **Automatic Law Conversion**: When no article specified, automatically converts article-specific URLs to complete laws
- **Debug Features**: `--debug-search` flag shows full Exa API JSON response
- **Manual Selection**: `--auto-select` flag allows manual result picking

#### 📦 Distribution
- **PyPI Package**: `akoma2md` v2.0.4 with enhanced search capabilities
- **GitHub Release**: v2.0.4 tag with improved article recognition

#### ✅ Verification
- **Article Search**: `normattiva2md -s "legge art 7"` correctly selects article 7
- **Law Search**: `normattiva2md -s "legge stanca"` selects complete law (not article)
- **Debug Mode**: `--debug-search` shows full Exa API response
- **Backward Compatibility**: All existing functionality preserved

### 🚀 Release v2.0.2: Backward Compatibility - Both CLI Names Supported

**Patch release**: Added backward compatibility for smooth migration

#### 🆕 New Features
- **Dual CLI Support**: Both `akoma2md` and `normattiva2md` commands now work
- **Seamless Migration**: Existing scripts continue to work without changes
- **Transition Period**: Users can migrate gradually to the new command name

#### 🔧 Technical Changes
- **Entry Points**: Added both command names in setup.py and pyproject.toml
- **Same Functionality**: Both commands execute identical code
- **Future Deprecation**: `akoma2md` command may be deprecated in future major version

#### 📦 Distribution
- **PyPI Package**: `akoma2md` v2.0.2 with dual CLI support
- **Installation**: `pip install akoma2md` provides both `akoma2md` and `normattiva2md` commands
- **Usage**: Either command works identically

#### ✅ Migration Path
```bash
# Both of these work:
akoma2md --version        # Old command (still works)
normattiva2md --version   # New command (recommended)
```

## 2025-11-04

### 🚀 Release v1.9.4: Critical Bug Fix - Missing Time Import

**Emergency fix**: Resolved critical runtime error in --with-references mode

#### 🐛 Critical Bug Fixed
- **Issue**: `name 'time' is not defined` error when using `--with-references`
- **Root Cause**: Missing `import time` statement in convert_akomantoso.py
- **Impact**: Rate limiting feature completely broken in v1.9.3
- **Fix**: Added missing import time to enable time.sleep(1) functionality

#### 🔧 Technical Details
- **Code change**: Added `import time` to imports section
- **Functionality**: Rate limiting now works correctly with 1-second delays between downloads
- **Backward compatibility**: No breaking changes, only fixes broken feature

#### ✅ Testing & Validation
- **All tests pass**: 27/27 unit tests successful
- **Rate limiting verified**: 1-second delays now properly applied in batch downloads
- **No regressions**: Existing functionality unaffected

#### 📦 Release Details
- **Version**: 1.9.4 (hotfix release)
- **PyPI**: https://pypi.org/project/akoma2md/1.9.4/
- **GitHub**: Tag v1.9.4 with automated binary builds
- **Urgency**: Critical fix for broken core feature

## 2025-11-04

### 🚀 Release v1.9.3: Rate Limiting for Respectful Usage

**New feature**: Added 1-second delay between HTTP requests in --with-references mode to respect server usage limits

#### ✨ New Feature: Rate Limiting

- **Rate limiting implemented**: 1-second delay between each download in --with-references batch mode
- **Respectful usage**: Prevents overwhelming normattiva.it servers during bulk downloads
- **No impact on functionality**: Delay only applies to batch downloads, not single document requests
- **Implementation**: Added time.sleep(1) in the download loop with import time

#### 🔧 Technical Details

- **Code changes**: Added import time, modified convert_with_references() loop
- **OpenSpec completed**: Proposal archived as implemented
- **Testing**: All existing tests pass (27/27), rate limiting verified

#### 📦 Ready for Release

- **Version**: 1.9.3 ready for PyPI and GitHub Releases
- **Backward compatibility**: Maintained, no breaking changes
- **Quality**: OpenSpec proposal completed, code reviewed

## 2025-11-04

### 🚀 Release v1.9.2: Fix Critico Cross-References

**Release correttiva urgente**: Risoluzione completa problema collegamenti incrociati

#### 🐛 Fix Critico Cross-References
- **Problema**: La funzionalità `--with-references` non generava collegamenti cliccabili alle leggi citate
- **Sintomi**: Log mostrava "64 riferimenti aggiunti" ma nessun link nel documento Markdown
- **Causa radice**: Mapping URI Akoma → percorsi file non funzionante per discrepanze codici redazionali
- **Soluzione**: Nuovo sistema di mapping diretto URL normattiva.it → percorsi file locali

#### 🔧 Implementazione Tecnica
- **Mapping rivisto**: Da URI Akoma complessi a mapping diretto URL→file path
- **Conversione dinamica**: URI Akoma convertiti in URL normattiva.it al momento del linking
- **Supporto directory**: `--with-references` ora accetta nomi directory personalizzati
- **Robustezza**: Eliminata dipendenza da codici redazionali inconsistenti

#### ✅ Validazione Completa
- **Test end-to-end**: Verificati collegamenti funzionanti in documenti reali
- **Esempi funzionanti**: `[legge 1912/555](refs/012U0555_19120630.md)` ora cliccabili
- **Suite test**: 27/27 test passando senza regressioni
- **Compatibilità**: Mantenuta retrocompatibilità completa

#### 📦 Distribuzione
- **Versione**: 1.9.2 con fix critico applicato
- **Urgenza**: Release correttiva per funzionalità chiave
- **Qualità**: Test completi, documentazione aggiornata

## 2025-11-04

### 🚀 Release v1.9.1: Fix Cross-References e Aggiornamento Roadmap

**Correzioni critiche e consolidamento**: Fix funzionalità cross-references e aggiornamento documentazione

#### 🐛 Fix Cross-References
- **Problema risolto**: I collegamenti alle leggi citate non venivano generati correttamente
- **Causa**: Mapping URI Akoma non corrispondeva ai codici redazionali dei file scaricati
- **Soluzione**: Nuovo approccio che mappa direttamente URL normattiva.it ai percorsi file
- **Risultato**: Collegamenti funzionanti come `[legge 1912/555](refs/012U0555_19120630.md)`

#### 📝 Aggiornamenti Documentazione
- **ROADMAP.md aggiornato**: Riflette versione corrente 1.9.0 e funzionalità completate
- **Stato versioni**: Allineamento tra documentazione e codice effettivo
- **Cronologia releases**: Documentate versioni v1.5.0-v1.9.0 con funzionalità implementate

#### 🔧 Miglioramenti Tecnici
- **Supporto directory personalizzate**: `--with-references` ora accetta nomi directory specifici
- **Mapping URL diretto**: Eliminata complessità mapping URI Akoma→file path
- **Conversione URI robusta**: Funzione `akoma_uri_to_normattiva_url()` per conversioni accurate

#### 🧪 Testing e Validazione
- **Test end-to-end**: Verificata generazione collegamenti incrociati funzionanti
- **Suite test completa**: 27/27 test passando senza regressioni
- **Funzionalità operative**: Cross-references, download leggi citate, ricerca Exa tutte funzionanti

#### 📦 Distribuzione
- **Versione**: 1.9.1 pronta per PyPI e GitHub Releases
- **Compatibilità**: Mantenuta completa retrocompatibilità
- **Qualità**: Fix critici implementati, documentazione allineata

## 2025-11-04

### 🚀 Release v1.9.0: Cross-References Inline nei Documenti Markdown

**Nuova funzionalità**: Collegamenti cliccabili automatici nei documenti Markdown quando si usa `--with-references`

#### ✨ Funzionalità Implementata
- **Cross-references inline**: I riferimenti `<ref>` nei documenti diventano link Markdown cliccabili
- **Mapping URI Akoma**: Conversione automatica da URI Akoma Ntoso a percorsi relativi dei file scaricati
- **Integrazione `--with-references`**: I collegamenti vengono aggiunti automaticamente durante la riconversione della legge principale
- **Supporto pattern URI**: Gestione di diversi tipi di URI (legge, decreto-legge, decreto legislativo, costituzione)

#### 🔧 Implementazione Tecnica
- **Modifica `clean_text_content()`**: Aggiunto parametro `cross_references` per abilitare link generation
- **Propagazione parametro**: Aggiornata tutta la call hierarchy per passare il mapping dei riferimenti
- **Funzione mapping**: `build_cross_references_mapping()` costruisce mapping URI→file path
- **Riconversione automatica**: Dopo download leggi citate, riconversione legge principale con link attivi

#### 📚 Esempi Utilizzo
```bash
# Crea struttura con collegamenti cliccabili
akoma2md --with-references "url-legge" output.md

# Risultato: main.md con riferimenti come [articolo 14](refs/400_19880823.md)
```

#### 🧪 Testing e Qualità
- **Test unitari**: Tutti test esistenti passati (27/27)
- **Test cross-references**: Verificata generazione link funzionante
- **Backward compatibility**: Nessun impatto quando non si usa `--with-references`
- **OpenSpec completato**: Proposal archiviata come implementata

#### 📦 Distribuzione
- **Versione**: 1.9.0 pronta per PyPI e GitHub Releases
- **Compatibilità**: Mantenuta retrocompatibilità completa
- **Documentazione**: README aggiornato con esempi cross-references

## 2025-11-04

### 🚀 Release v1.8.0: Download Automatico Leggi Citare

- **Nuova funzionalità `--with-references`**: Scarica automaticamente tutte le leggi citate in una struttura di cartelle organizzata
- Creazione automatica di cartelle con legge principale + riferimenti
- Estrazione intelligente dei riferimenti da tag XML `<ref>`
- File indice per navigazione tra documenti correlati
- Supporto per deduplicazione e gestione errori nei download batch
- Esempio: `akoma2md --with-references "url-legge"` crea `codice_data/main.md` + `refs/*.md` + `index.md`

## 2025-11-04

### 🚀 Release v1.7.4: Miglioramento Messaggi Errore

- Messaggi errore più informativi quando input invalido
- Guida utente con 3 modalità d'uso: URL normattiva.it, file XML locale, ricerca con `-s`
- Fix UX per errori comuni tipo `akoma2md "legge stanca"`

## 2025-11-04

### 🚀 Release v1.7.3: Fix BrokenPipeError

- Gestito `BrokenPipeError` quando stdout viene chiuso prematuramente
- Fix per piping a `less`, `head`, `more` e simili
- Gestito anche `KeyboardInterrupt` (CTRL+C) in modo graceful
- No più traceback quando si esce da pager

### 🚀 Release v1.7.2: Fix Query Exa API

- Rimosso parametro ridondante `site:normattiva.it` dalla query Exa
- Filtro dominio già gestito correttamente da `includeDomains` parameter
- Query più pulita e aderente alla documentazione ufficiale Exa

## 2025-11-03

### 🚀 Release v1.7.1: Caricamento Automatico .env

**Miglioramento usabilità:** Caricamento automatico dell'API key Exa dal file .env senza esportazione manuale

#### ✨ Nuove Funzionalità
- **Caricamento Automatico .env**: L'API key di Exa viene caricata automaticamente dal file `.env` all'avvio del programma
- **Configurazione Semplificata**: Basta creare un file `.env` con `EXA_API_KEY="your-key"` - niente più esportazioni manuali
- **Retrocompatibilità**: Le variabili d'ambiente esportate continuano a funzionare normalmente

#### 🔧 Implementazione Tecnica
- **Funzione load_env_file()**: Carica automaticamente le variabili dal file `.env` alla partenza
- **Parsing Sicuro**: Gestione corretta di virgolette e commenti nel file `.env`
- **Fallback Graceful**: Se il file `.env` non esiste o ha errori, il programma continua normalmente

#### 🧪 Testing e Qualità
- **Funzionalità Verificata**: Ricerca funziona senza esportazione manuale dell'API key
- **Retrocompatibilità**: Variabili d'ambiente esportate continuano a funzionare
- **Sicurezza**: File `.env` già incluso nel `.gitignore`

#### 📦 Distribuzione
- **Versione**: 1.7.1 con changelog completo
- **PyPI**: Pubblicazione automatica su Python Package Index
- **GitHub Releases**: Binari standalone per Linux e Windows
- **Documentazione**: README aggiornato con istruzioni per entrambi i metodi di configurazione

## 2025-11-03

### 🚀 Release v1.7.0: Ricerca AI con Exa - Performance e Semplicità

**Maggiore velocità e semplicità:** Sostituzione infrastruttura ricerca da Gemini CLI a Exa AI API con prestazioni significativamente migliorate

#### ✨ Nuove Funzionalità Principali
- **Exa AI Integration**: Passaggio da Gemini CLI a Exa AI API per ricerca intelligente documenti legali
- **Configurazione Semplificata**: Solo variabile d'ambiente `EXA_API_KEY` invece di installazione CLI esterna
- **Ricerca Ottimizzata**: Utilizzo `includeDomains: ["normattiva.it"]` per ricerche mirate e precise
- **Performance Migliorata**: Risposte più veloci grazie alla specializzazione di Exa per web search

#### 🔧 Miglioramenti Tecnici
- **API Moderna**: Integrazione diretta con Exa AI API invece di subprocess CLI
- **Caricamento Automatico**: API key caricata automaticamente dal file `.env` all'avvio
- **Gestione Errori**: Timeout 30s, validazione HTTP status, parsing JSON robusto
- **Sicurezza**: API key protetta in file `.env` (già nel `.gitignore`)
- **Codice Pulito**: Refactoring completo di `lookup_normattiva_url()` senza dipendenze esterne

#### 🧪 Testing e Qualità
- **Test End-to-End**: Validazione con ricerche reali ("legge stanca", "decreto dignità", "costituzione italiana")
- **Suite Completa**: Tutti test unitari aggiornati per mockare Exa API
- **Conversione Verificata**: XML→Markdown con front matter e struttura gerarchica corretta
- **Retrocompatibilità**: Mantenuta interfaccia CLI esistente (`--search/-s`)

#### 📦 Distribuzione
- **Versione**: 1.7.0 con changelog completo
- **PyPI**: Pubblicazione automatica su Python Package Index
- **GitHub Releases**: Binari standalone per Linux e Windows
- **Documentazione**: README aggiornato con istruzioni Exa AI

## 2025-11-03

### 🔄 Sostituzione Gemini con Exa per Ricerca AI

**Cambio infrastruttura ricerca:** Passaggio da Gemini CLI a Exa AI API per funzionalità di ricerca naturale documenti legali

#### ✅ Modifiche Implementate
- **Sostituzione API**: Rimpiazzato Gemini CLI con Exa AI API per ricerca intelligente
- **Configurazione semplificata**: Passaggio da installazione CLI esterna a variabile d'ambiente EXA_API_KEY
- **Ricerca ottimizzata**: Utilizzo `includeDomains` per limitare ricerca esclusivamente a normattiva.it
- **Codice aggiornato**: Refactoring completo funzione `lookup_normattiva_url()` con gestione errori migliorata
- **Test aggiornati**: Tutti test di regressione modificati per mockare Exa API invece di Gemini CLI

#### 🔧 Dettagli Tecnici
- **Endpoint API**: `https://api.exa.ai/search` con parametri ottimizzati per ricerca legale
- **Query format**: `{search_query} site:normattiva.it` per precisione risultati
- **Gestione errori**: Timeout 30s, validazione HTTP status, parsing JSON robusto
- **Compatibilità**: Mantenuta interfaccia CLI esistente (`--search/-s`)

#### 🧪 Testing e Validazione
- **Test end-to-end**: Ricerca "legge stanca" → Decreto Legislativo 4/2004 ✅
- **Test multipli**: Ricerca "decreto dignità" → Decreto-legge 87/2018 ✅
- **Test costituzione**: Ricerca "costituzione italiana" → Costituzione 1947 ✅
- **Conversione completa**: XML→Markdown con front matter e struttura gerarchica corretta
- **Suite test**: Tutti test unitari passano senza regressioni

#### 📦 Impatto
- **Dipendenze**: Rimossa necessità installazione Gemini CLI, aggiunta configurazione API key
- **Performance**: Risposta più veloce con ricerca domain-specific
- **Manutenibilità**: Codice più semplice senza gestione subprocess esterni
- **Sicurezza**: API key protetta in file .env (già nel .gitignore)

## 2025-11-05

### 🚀 Aggiunto Flag --with-urls per Link Markdown Articoli Citati

**Nuova funzionalità**: Flag `--with-urls` per generare link markdown agli articoli citati su normattiva.it

#### ✨ Funzionalità Implementata
- Nuovo parametro `--with-urls` nella CLI
- Genera link markdown agli articoli citati, senza scaricare i documenti
- Documentazione aggiornata: README, help CLI, esempi d'uso
- Nessun impatto su download batch (`--with-references`)

#### 📚 Esempi Utilizzo
```bash
normattiva2md --with-urls input.xml output.md
normattiva2md --with-urls "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2022;53" legge_con_link.md
```

### 🚀 Rilascio Versione 1.6.1

**Miglioramenti principali:**
- ✅ Rimozione supporto URL esportazione atto intero non funzionanti
- ✅ Miglioramento gestione URL normattiva.it con messaggi di errore chiari
- ✅ Pulizia codice e rimozione funzioni obsolete

#### ✨ Miglioramenti Implementati
- **Rimozione URL Esportazione**: Gli URL `/esporta/attoCompleto` non sono più supportati perché richiedono autenticazione
- **Messaggi di Errore Migliorati**: Messaggi chiari che guidano l'utente a usare URL permalink (URN)
- **Supporto Esclusivo Permalink**: Solo URL URN funzionanti sono supportati per garantire affidabilità
- **Pulizia Codice**: Rimozione funzioni e logica obsolete per URL di esportazione

#### 🔧 Miglioramenti Tecnici
- Validazione più rigorosa degli URL di input
- Messaggi di errore informativi per URL non supportati
- Mantenimento compatibilità con URL permalink esistenti

#### 📦 Pubblicazione PyPI
- ✅ Pacchetto v1.6.1 caricato con successo su PyPI
- ✅ Verifica installazione riuscita da repository remoto

#### 🚀 Rilascio GitHub
- ✅ Release v1.6.1 creata automaticamente con binari Linux e Windows
- ✅ CI/CD pipeline completata con successo

#### 📦 Distribuzione
- Versione 1.6.1 disponibile su PyPI
- Binari standalone per Linux e Windows generati automaticamente
- Compatibilità mantenuta con versioni precedenti

## 2025-11-05

### 🚀 Rilascio Versione 1.6.0

**Nuove funzionalità principali:**
- ✅ Supporto URL articolo-specifici (`~art3`, `~art16bis`, etc.)
- ✅ Flag `--completo` (`-c`) per forzare download legge completa
- ✅ Migliorato riconoscimento Gemini CLI nel PATH

#### ✨ Funzionalità Aggiunte
- **URL Articolo-Specifici**: Possibilità di convertire singoli articoli da URL normattiva.it
- **Flag --completo**: Override per scaricare legge completa anche con URL articolo-specifici
- **Ricerca AI Migliorata**: Gemini CLI ora riconosciuto correttamente in tutti gli ambienti

#### 🔧 Miglioramenti Tecnici
- Implementazione robusta del riconoscimento comandi nel PATH

#### 📦 Pubblicazione PyPI
- ✅ Pacchetto v1.6.0 caricato con successo su PyPI
- ✅ Verifica installazione riuscita da repository remoto

#### 🚀 Rilascio GitHub
- ✅ Release v1.6.0 creata automaticamente con binari Linux e Windows
- ✅ CI/CD pipeline completata con successo
- Gestione errori migliorata per configurazioni Gemini incomplete
- Documentazione aggiornata con nuovi esempi di utilizzo

#### 📦 Distribuzione
- Versione 1.6.0 disponibile su PyPI
- Binari standalone per Linux e Windows generati automaticamente
- Compatibilità mantenuta con versioni precedenti

## 2025-11-05

### ✅ Aggiunto Flag --completo per Override Articolo-Specifico

**Nuova funzionalità**: Flag `--completo` (`-c`) per forzare download legge completa anche con URL articolo-specifico

#### ✨ Funzionalità Implementata
- Nuovo parametro `--completo` / `-c` nella CLI
- Override automatico del filtro articolo quando flag attivo
- Conversione completa del documento anche con URL `~artN`
- Mantenimento metadata originale con riferimento articolo per tracciabilità
- Compatibilità totale con URL legge completa (nessun effetto)

#### 🔧 Implementazione Tecnica
- Modifica `argparse` per aggiungere flag `--completo`
- Logica condizionale in `main()` per override filtro articolo
- Aggiornamento metadata per includere riferimento articolo originale
- Aggiornamento help text e esempi CLI

#### 📚 Esempi Utilizzo
```bash
# Conversione articolo specifico
akoma2md "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto-legge:2018-07-12;87~art3" art3.md

# Forza conversione completa stesso URL
akoma2md "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto-legge:2018-07-12;87~art3" --completo legge_completa.md
```

## 2025-11-04

### ✅ Aggiunto Supporto URL Articolo-Specifico

**Nuova funzionalità**: Supporto per URL che puntano ad articoli specifici nelle leggi

#### ✨ Funzionalità Implementata
- Riconoscimento automatico URL con riferimenti articolo (`~art3`, `~art16bis`, etc.)
- Filtraggio documenti XML per estrarre solo l'articolo richiesto
- Generazione metadata con riferimento articolo nel front matter
- Validazione esistenza articolo nel documento con messaggi errore chiari
- Mantenimento compatibilità con URL legge completi

#### 🔧 Implementazione Tecnica
- Nuove funzioni: `parse_article_reference()`, `filter_xml_to_article()`
- Modifica pipeline conversione per gestire documenti singolo-articolo
- Aggiornamento generazione front matter per includere campo `article`
- Estensioni articolo supportate: bis, ter, quater, quinquies, sexies, etc.

#### 📚 Esempi URL Supportati
- `https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto-legge:2018-07-12;87~art3`
- `https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2022;53~art16bis`

## 2025-11-03

### ✅ Aggiunto Supporto URL Atto Intero

**Nuova funzionalità**: Supporto per URL di esportazione "atto intero" di normattiva.it

#### ✨ Funzionalità Implementata
- Riconoscimento automatico URL atto intero (`/esporta/attoCompleto?`)
- Estrazione parametri direttamente dalla query string dell'URL
- Conversione automatica in URL legge equivalente per processamento
- Mantenimento compatibilità con URL legge esistenti

#### 🔧 Implementazione Tecnica
- Nuove funzioni: `is_normattiva_export_url()`, `convert_export_url_to_law_url()`
- Modifica `extract_params_from_normattiva_url()` per gestire due tipi di URL
- Validazione parametri URL con regex per formato corretto
- Conversione URN automatica da parametri estratti

#### 📚 Documentazione Aggiornata
- Aggiornati esempi CLI con URL atto intero
- Migliorati help text per input supportati
- Aggiunti commenti esplicativi per i due path di processamento URL

#### 🧪 Testing
- Test regressione con URL legge esistenti
- Test nuovi URL atto intero
- Test error handling per URL invalidi
- Suite test completa: tutti passati

## 2025-11-02

### ✅ Release v1.5.0 Completata con Successo

**Stato**: Release v1.5.0 distribuita correttamente
- ✅ **Problema risolto**: Binari ora hanno nomi versione corretti (1.5.0)
- ✅ **Tag corretto**: v1.5.0 punta al commit con funzionalità ricerca completa
- ✅ **Workflow riuscito**: GitHub Actions completato con binari corretti generati
- ✅ **Release creata**: https://github.com/ondata/normattiva_2_md/releases/tag/v1.5.0
- ✅ **Binari disponibili**: Linux (21.9MB) e Windows (9.4MB) con versione corretta
- ✅ **PyPI aggiornato**: Versione 1.5.0 disponibile per installazione
- ✅ **Documentazione aggiornata**: Chiariti requisiti per funzionalità ricerca

#### 🐛 Problema Risolto: Nomi Binari Errati
- **Issue**: Prima release aveva binari nominati `akoma2md-1.4.2-*` invece di `1.5.0`
- **Causa**: Tag v1.5.0 creato su commit senza funzionalità ricerca
- **Fix**: Tag spostato su commit corretto, workflow rigenerato, release ricreata
- **Risultato**: Binari ora correttamente nominati `akoma2md-1.5.0-*`

#### 📦 Distribuzione
- **PyPI**: `pip install akoma2md==1.5.0`
- **GitHub Releases**: Binari standalone per sistemi senza Python
- **Installazione Gemini CLI**: Richiesta per funzionalità ricerca (`gemini --help`)

### 🔍 Test Funzionalità Ricerca
Comando testato: `python3 convert_akomantoso.py --search "legge di bilancio 2024"`
- ✅ Gemini CLI integrato correttamente
- ✅ URL trovato: https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2023-12-30;213
- ✅ Conversione XML→Markdown completata
- ✅ Documento: "Bilancio di previsione dello Stato per l'anno finanziario 2024"

## 2025-11-02

### 🚀 Release v1.5.0: Ricerca Naturale con Gemini CLI

**Nuova funzionalità principale**: Ricerca intelligente di documenti legali in linguaggio naturale

#### ✨ Nuove Funzionalità
- Aggiunto flag `--search/-s` per ricerca in linguaggio naturale
- Integrazione con Gemini CLI per ricerca intelligente su normattiva.it
- Conversione automatica da nome a URL a documento Markdown
- Mantenimento compatibilità con metodi esistenti

#### 🔧 Implementazione Tecnica
- Nuovo modulo `lookup_normattiva_url()` con Gemini CLI headless
- Parsing JSON strutturato per risposte AI
- Gestione errori robusta per CLI non installato/configurato
- Tests unitari e di integrazione completi

#### 📚 Documentazione
- Aggiornato README con esempi ricerca naturale
- Istruzioni complete installazione e configurazione Gemini CLI
- Esempi pratici per tutti i metodi di input

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

## 2025-12-04

### Planning: API Programmabile

Creata pianificazione completa per rendere normattiva2md usabile da notebook e script Python:

**Documentazione creata:**
- 7 documenti tecnici dettagliati (architettura, specs, models, exceptions, plan, examples, index)
- Piano implementazione 6 fasi (14-21h totali)

**Decisioni architetturali:**
- Stile misto: funzioni standalone + classe `Converter`
- Output: oggetto `ConversionResult` con markdown + metadata
- Errori: strategia ibrida (eccezioni gravi + None per soft errors)
- Type hints completi (Python 3.7+ compatible)
- Logging invece di print() per API
- Struttura preparata per future versioni async

**File pianificati:**
- `src/normattiva2md/exceptions.py` - sistema eccezioni custom
- `src/normattiva2md/models.py` - dataclasses ConversionResult, SearchResult
- `src/normattiva2md/api.py` - API programmabile
- `examples/notebook_quickstart.ipynb` - Jupyter notebook dimostrativo
- `docs/notebook_examples.md` - esempi pratici completi

**Compatibilità:** 100% backward compatible - CLI funziona esattamente come prima

**Prossimo step:** Review pianificazione → implementazione Fase 1 (Foundation)
## 2026-01-02

### Aggiunta Avviso Legale su README, CLI e Front Matter

**Conformità legale:** Aggiunto avviso legale prominente sullo status ufficiale dei documenti

**Modifiche implementate:**
- **README.md**: Nuova sezione `⚠️ Avvertenza legale` subito dopo introduzione
- **cli.py - Rich help**: Panel visuale rosso/giallo con avvertenza alla apertura help
- **cli.py - argparse epilog**: Avvertenza anche nel footer standard `--help`
- **markdown_converter.py**: Campo `legal_notice` nel front matter YAML di ogni documento

**Avviso fornito:**
- I testi presenti in Normattiva non hanno carattere di ufficialità
- L'unico testo ufficiale è quello pubblicato sulla Gazzetta Ufficiale Italiana
- Utilizzo solo a scopo informativo

**Posizionamento strategico:**
1. Prima di usare il tool → README
2. Quando richiede aiuto → CLI
3. Nel documento generato → Front matter YAML

**Impatto:** Nessuno breaking change, avvertenza informativa, importante per conformità legale

## 2026-01-01
- Improved CLI help output with Rich library for better readability and organization

## 2026-01-29
### Fallback OpenData AKN + flag for OpenData

- **Fallback automatico**: se l'export Akoma (`caricaAKN`) non è disponibile, usa OpenData AKN (ZIP) per recuperare il file XML.
- **Nuovo flag CLI**: `--opendata` per forzare il download via OpenData su qualsiasi norma.
- **API Python**: `convert_url(..., force_opendata=True)` per forzare OpenData.
- **Selezione XML**: scelta automatica del file di vigenza più adatto dal pacchetto ZIP.

## 2026-01-21
- Bumped version to v2.1.7 for upcoming release
