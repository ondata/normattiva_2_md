# Roadmap - normattiva2md

Punti da attenzionare per le prossime release, basati su code review approfondita.

## ✅ COMPLETED - v1.5.0 to v1.9.0 (2025 Releases)

### Versioni Rilasciate
- **v1.9.0** (2025-11-04): Cross-references inline nei documenti Markdown
- **v1.8.0** (2025-11-04): Download automatico leggi citate con `--with-references`
- **v1.7.0** (2025-11-03): Ricerca AI con Exa API (sostituzione Gemini)
- **v1.6.0** (2025-11-03): Supporto URL articolo-specifici e flag `--completo`
- **v1.5.0** (2025-11-02): Ricerca naturale documenti legali

### Funzionalità Implementate
- ✅ Cross-references inline con mapping URI Akoma→file path
- ✅ Download automatico leggi citate in struttura organizzata
- ✅ Ricerca AI con Exa API per lookup naturale documenti
- ✅ Supporto URL articolo-specifici (~art3, ~art16bis, etc.)
- ✅ Flag --completo per override download legge completa
- ✅ Miglioramento messaggi errore e UX CLI
- ✅ Caricamento automatico API key da .env
- ✅ Gestione graceful BrokenPipeError e KeyboardInterrupt

---

## ✅ COMPLETED - v2.0.0 to v2.0.2 (2025-11-04)

### CLI Rename: akoma2md → normattiva2md

**Status**: ✅ Completed with backward compatibility

#### Changes Made
- **Entry Points**: Both `akoma2md` and `normattiva2md` commands supported
- **Documentation**: Updated all references and examples
- **Branding**: Project renamed for better discoverability
- **Backward Compatibility**: Old command still works during transition

#### Deprecation Timeline
- **v2.0.x**: Both commands supported (current)
- **v3.0.0** (Q2 2026): `akoma2md` command deprecated with warning
- **v4.0.0** (Q1 2027): `akoma2md` command removed

#### Migration Guide
```bash
# Recommended (new)
normattiva2md input.xml output.md

# Still works (deprecated in future)
akoma2md input.xml output.md
```

---

## ✅ COMPLETED - v2.0.3 to v2.0.7 (2025-11-04)

### Search & UX Enhancements

**Status**: ✅ Completed

#### Versioni Rilasciate
- **v2.0.7** (2025-11-04): Permanent link field in frontmatter
- **v2.0.6** (2025-11-04): Cleaner search output & improved UX
- **v2.0.5** (2025-11-04): Enhanced Exa search scoring & URL conversion
- **v2.0.4** (2025-11-04): Enhanced article recognition in search
- **v2.0.3** (2025-11-04): README update on PyPI (metadata only)

#### Funzionalità Implementate
- ✅ Campo `url_permanente` nel frontmatter YAML con URN canonico e vigenza
- ✅ Output ricerca più pulito: verbose mode solo con `--debug-search`
- ✅ Scoring Exa migliorato: priorità leggi complete vs articoli specifici
- ✅ Conversione automatica URL articolo→legge completa quando appropriato
- ✅ Riconoscimento articoli esteso: "articolo 7", "art 7", "art. 7", numeri complessi (16bis, 16ter)
- ✅ Bonus/penalità intelligenti per selezione risultati Exa
- ✅ Metadata PyPI aggiornati e corretti

#### Example Output
```yaml
---
url_permanente: https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2005-03-07;82!vig=2025-01-30
---
```

---

## 🟡 NEXT RELEASE - v2.1.0 (Prossima Release)

### 1. Refactoring `main()` function

**Problema**: Funzione troppo lunga (143 linee) con responsabilità multiple

**Soluzione**:
```python
def parse_args():
    """Parse command line arguments"""
    # 30 linee

def process_url(url, output_file, keep_xml, quiet):
    """Handle URL-based conversion"""
    # 40 linee

def process_file(file_path, output_file, quiet):
    """Handle local file conversion"""
    # 20 linee

def main():
    """Main entry point - orchestration only"""
    # 30 linee
```

**Benefici**:
- Miglior testabilità
- Codice più manutenibile
- Ogni funzione < 50 linee

**File**: `convert_akomantoso.py:807-950`

---

### 2. Fix HTML Parsing Fragility

**Problema**: Uso regex per parsing HTML (linee 300-328)

**Attuale**:
```python
# Fragile - si rompe se HTML cambia
match_gu = re.search(r'name="atto\.dataPubblicazioneGazzetta"[^>]*value="([^"]+)"', html)
```

**Soluzione**:
```python
from bs4 import BeautifulSoup

def extract_params_from_normattiva_url(url, session=None, quiet=False):
    soup = BeautifulSoup(html, 'html.parser')
    input_gu = soup.find('input', {'name': 'atto.dataPubblicazioneGazzetta'})
    params['dataGU'] = input_gu['value'] if input_gu else None
```

**Dependency**: `beautifulsoup4>=4.9.0`

**Benefici**:
- Più robusto a cambi HTML
- Più leggibile
- Best practice parsing HTML

**File**: `convert_akomantoso.py:300-328`

---

### 3. Network Error Recovery

**Problema**: Nessun retry su errori di rete

**Soluzione**:
```python
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def create_session_with_retry():
    session = requests.Session()
    retry = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('https://', adapter)
    return session
```

**Benefici**:
- Maggiore affidabilità
- Gestione errori temporanei
- Migliore UX

**File**: `convert_akomantoso.py:267-383`

---

### 4. Complete Footnote Implementation

**Problema**: Implementazione semplificata senza global counter (linee 230-236)

**Attuale**:
```python
# Simplified - no global counter
footnote_ref = f"[^{footnote_content[:10].replace(' ', '')}]"
```

**Soluzione**:
```python
class MarkdownGenerator:
    def __init__(self):
        self.footnote_counter = 0
        self.footnotes = []

    def add_footnote(self, content):
        self.footnote_counter += 1
        ref = f"[^{self.footnote_counter}]"
        self.footnotes.append(f"{ref}: {content}")
        return ref

    def get_footnotes_section(self):
        if not self.footnotes:
            return ""
        return "\n\n---\n\n" + "\n\n".join(self.footnotes)
```

**Benefici**:
- Footnote numerate correttamente
- Definizioni a fine documento
- Formato Markdown standard

**File**: `convert_akomantoso.py:230-236`

---

### 5. Integration Tests

**Problema**: Mancano test end-to-end e scenari errore

**Da aggiungere**:
```python
class IntegrationTests(unittest.TestCase):
    @mock.patch('requests.Session.get')
    def test_url_download_with_network_error(self, mock_get):
        """Test retry logic on network errors"""

    def test_url_to_markdown_complete_flow(self):
        """Test complete URL → Markdown conversion"""

    def test_large_xml_rejected(self):
        """Test >50MB file rejection"""

    def test_malformed_xml_handling(self):
        """Test malformed XML error handling"""
```

**File**: Nuovo `tests/test_integration.py`

---

### 6. Precompile Regex Patterns

**Problema**: Pattern compilati ad ogni chiamata (performance)

**Soluzione**:
```python
# A inizio modulo (dopo imports)
CAPO_PATTERN = re.compile(r'\bCapo\s+[IVX]+', re.IGNORECASE)
SEZIONE_PATTERN = re.compile(r'\bSezione\s+[IVX]+', re.IGNORECASE)
CHAPTER_PATTERN = re.compile(r'^((?:Capo|Sezione)\s+[IVX]+)\s+(.+)$', re.IGNORECASE)
WHITESPACE_PATTERN = re.compile(r'\s+')
SEPARATOR_PATTERN = re.compile(r'^-+$')
HIDDEN_INPUT_PATTERN = re.compile(r'name="atto\.([^"]+)"[^>]*value="([^"]+)"')

# Uso nelle funzioni:
def parse_chapter_heading(heading_text):
    has_capo = CAPO_PATTERN.search(heading_text)
    has_sezione = SEZIONE_PATTERN.search(heading_text)
```

**Benefici**:
- Performance: ~20-30% più veloce su documenti grandi
- Codice più pulito
- Best practice Python

**File**: `convert_akomantoso.py` (multiple locations)

---

## 🟢 MEDIUM PRIORITY - v1.6.0

### 7. Type Hints

**Obiettivo**: Aggiungere type hints a tutte le funzioni

```python
from typing import Dict, List, Optional, Tuple
import xml.etree.ElementTree as ET

def clean_text_content(element: Optional[ET.Element]) -> str:
    """Extract text from element with type safety"""

def validate_normattiva_url(url: str) -> bool:
    """Validate URL with type checking"""

def extract_metadata_from_xml(root: ET.Element) -> Dict[str, str]:
    """Extract metadata with typed return"""
```

**Setup mypy**:
```toml
# pyproject.toml
[tool.mypy]
python_version = "3.7"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

**Benefici**:
- Migliore IDE support (autocomplete)
- Catch errori a compile-time
- Documentazione implicita

---

### 8. API Documentation con Sphinx

**Setup**:
```bash
pip install sphinx sphinx-rtd-theme
sphinx-quickstart docs/
```

**Configurazione**:
```python
# docs/conf.py
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]
html_theme = 'sphinx_rtd_theme'
```

**Benefici**:
- Documentazione professionale
- ReadTheDocs integration
- API reference completo

---

### 9. CI/CD Pipeline Completo

**GitHub Actions workflow**:
```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.7', '3.8', '3.9', '3.10', '3.11']
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: |
          pip install -e .[test]
          pytest --cov --cov-report=xml
      - name: Type checking
        run: mypy .
      - name: Linting
        run: ruff check .
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

**Benefici**:
- Test automatici su PR
- Coverage tracking
- Quality checks

---

### 10. Version Management

**Single source of truth**:
```python
# akoma2md/__version__.py
__version__ = "1.5.0"

# setup.py
from akoma2md.__version__ import __version__
setup(version=__version__)

# pyproject.toml
version = {attr = "akoma2md.__version__.__version__"}
```

**Automated changelog**:
```bash
# Usa conventional commits
git commit -m "feat: add retry logic"
git commit -m "fix: correct footnote numbering"

# Generate changelog
conventional-changelog -p angular -i CHANGELOG.md -s
```

---

### 11. Optional Dependencies

**pyproject.toml**:
```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "mypy>=1.0",
    "black>=23.0",
    "ruff>=0.1.0"
]
test = [
    "pytest-mock>=3.10",
    "responses>=0.23"
]
html = [
    "beautifulsoup4>=4.9.0",
    "lxml>=4.9.0"
]
all = [
    "akoma2md[dev,test,html]"
]
```

**Installazione**:
```bash
pip install akoma2md[dev]    # per sviluppo
pip install akoma2md[html]   # per HTML parsing robusto
pip install akoma2md[all]    # tutto
```

---

## 🟢 PLANNED - EUR-Lex Integration (v2.3.0)

### EUR-Lex XHTML to Markdown Converter

**Status**: 🎯 Ready for implementation - Analysis completed

**Background**: 
- EUR-Lex API esplorata e documentata (`docs/EURLEX_API.md`, `docs/EUR-LEX_INTEGRATION.md`)
- Script download funzionante (`scripts/download_eurlex.py`)
- Analisi conversione completata (`docs/EURLEX_CONVERSION_ANALYSIS.md`)
- Test tool comparativi: html2text vince (qualità ⭐⭐⭐⭐⭐)

**Obiettivo**: CLI tool per convertire legislazione EU da EUR-Lex a Markdown

**Architettura**:

```bash
# Opzione 1: Tool separato (CONSIGLIATO)
eurlex2md 32024L1385 --lang IT --output direttiva.md

# Opzione 2: Integrato in normattiva2md
normattiva2md --source eurlex 32024L1385 --lang IT
```

**Workflow Interno**:
1. Download XML Notice (metadati + URL disponibili)
2. Mappatura codice lingua (IT → ITA, EN → ENG)
3. Download XHTML da publications.europa.eu
4. Conversione XHTML → Markdown con html2text
5. Post-processing (metadata, cleanup)

**Dependencies**:
```python
html2text>=2024.2.26  # Conversione XHTML → MD
```

**Implementation Steps**:

1. **CLI Wrapper** (~100 linee)
   ```python
   # eurlex2md.py (nuovo file)
   def main():
       parser = argparse.ArgumentParser(description='Convert EUR-Lex documents to Markdown')
       parser.add_argument('celex', help='CELEX number (e.g., 32024L1385)')
       parser.add_argument('--lang', default='EN', help='Language code (IT, EN, FR, DE, ES)')
       parser.add_argument('--output', help='Output markdown file')
       parser.add_argument('--keep-xhtml', action='store_true', help='Keep intermediate XHTML')
       parser.add_argument('--quiet', action='store_true', help='Suppress progress messages')
   ```

2. **Integrazione html2text** (~50 linee)
   ```python
   import html2text
   
   def convert_xhtml_to_markdown(xhtml_file, output_file):
       h = html2text.HTML2Text()
       h.ignore_tables = True
       h.ignore_images = True
       h.unicode_snob = True
       h.body_width = 0  # No line wrapping
       
       with open(xhtml_file, 'r', encoding='utf-8') as f:
           html = f.read()
       
       markdown = h.handle(html)
       
       with open(output_file, 'w', encoding='utf-8') as f:
           f.write(markdown)
   ```

3. **Riuso download_eurlex.py** (~30 linee refactoring)
   - Estrarre funzioni riutilizzabili
   - Supporto library mode (oltre CLI)
   - Return paths ai file scaricati

4. **Tests** (~150 linee)
   ```python
   # tests/test_eurlex.py
   class TestEURLexConversion(unittest.TestCase):
       def test_celex_validation(self):
           """Test CELEX number format validation"""
       
       def test_language_mapping(self):
           """Test IT → ITA, EN → ENG mapping"""
       
       def test_xhtml_to_markdown(self):
           """Test XHTML conversion with test_data/eurlex_sample_it.xhtml"""
       
       def test_full_workflow(self):
           """Test complete CELEX → Markdown flow"""
   ```

5. **Documentation** (~200 linee)
   ```markdown
   # docs/EURLEX_USAGE.md
   - Installation
   - Basic usage
   - Language codes reference
   - Examples
   - Troubleshooting
   ```

**Benefici**:
✅ Complementare a Normattiva (UE + IT)
✅ Workflow già validato e testato
✅ Nessun parser XML custom (usa html2text)
✅ 80% codice già implementato
✅ API EUR-Lex gratuita e stabile

**Timeline**: 2-3 ore sviluppo + 1 ora testing

**Files da creare**:
- `eurlex2md.py` (nuovo CLI tool)
- `tests/test_eurlex.py` (test suite)
- `docs/EURLEX_USAGE.md` (user guide)

**Files da modificare**:
- `scripts/download_eurlex.py` (refactor per library mode)
- `setup.py` (aggiungere entry point `eurlex2md`)
- `README.md` (aggiungere sezione EUR-Lex)

**Deliverables**:
```bash
# CLI usage
eurlex2md 32024L1385 --lang IT -o direttiva-violenza-donne.md
eurlex2md 32016R0679 --lang EN -o gdpr.md  # GDPR in inglese
eurlex2md --list-languages  # Show all 24 EU languages
```

---

## 🔵 LOW PRIORITY - Future (v2.0.0)

### 12. Configuration File Support

**Feature**: `.akoma2md.yml` per configurazione

```yaml
# .akoma2md.yml
network:
  timeout: 60
  max_retries: 5

limits:
  max_file_size_mb: 100

output:
  format: markdown
  include_front_matter: true
  heading_style: atx  # or setext

processing:
  validate_before_convert: true
  clean_whitespace: true
```

**Caricamento**:
```python
import yaml

def load_config():
    config_paths = [
        '.akoma2md.yml',
        '~/.config/akoma2md/config.yml'
    ]
    for path in config_paths:
        if os.path.exists(path):
            with open(path) as f:
                return yaml.safe_load(f)
    return {}
```

---

### 13. Internazionalizzazione (i18n)

**Error messages in inglese**:
```python
MESSAGES = {
    'it': {
        'url_invalid': 'URL non valido: {}',
        'file_not_found': 'File non trovato: {}',
    },
    'en': {
        'url_invalid': 'Invalid URL: {}',
        'file_not_found': 'File not found: {}',
    }
}

def get_message(key, locale='it', **kwargs):
    return MESSAGES[locale][key].format(**kwargs)
```

---

### 14. Batch Processing Mode

**CLI**:
```bash
# Da file con lista URL
akoma2md --batch urls.txt --output-dir ./output/

# Da pattern
akoma2md --batch "https://normattiva.it/leggi/*.xml" -o ./leggi/

# Con parallelizzazione
akoma2md --batch urls.txt -o ./out/ --parallel 4
```

**Implementazione**:
```python
def batch_convert(url_file, output_dir, parallel=1):
    with open(url_file) as f:
        urls = [line.strip() for line in f]

    if parallel > 1:
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=parallel) as executor:
            executor.map(lambda url: convert_url(url, output_dir), urls)
    else:
        for url in urls:
            convert_url(url, output_dir)
```

---

### 15. Validation Mode

**CLI**:
```bash
# Solo validazione, no conversione
akoma2md --validate input.xml

# Con report dettagliato
akoma2md --validate input.xml --verbose
```

**Output**:
```
✅ File XML valido
✅ Struttura Akoma Ntoso 3.0 corretta
✅ Metadati completi
⚠️  Avviso: Footnote senza definizione
📊 Statistiche:
   - Articoli: 127
   - Capitoli: 8
   - Sezioni: 15
```

---

### 16. Modularizzazione Codebase

**Nuova struttura**:
```
akoma2md/
├── __init__.py          # Package init
├── __version__.py       # Version
├── cli.py              # CLI logic (~150 linee)
├── converter.py        # Conversione core (~400 linee)
├── parser.py           # XML parsing (~300 linee)
├── network.py          # HTTP/URL handling (~150 linee)
├── metadata.py         # Metadata extraction (~100 linee)
├── security.py         # Validation/security (~100 linee)
└── utils.py            # Utilities (~50 linee)
```

**Benefici**:
- Codice più organizzato
- Import selettivi
- Testing più facile
- Riuso componenti

---

## 📊 Metriche di Successo

### v2.1.0 Target (Current Sprint)
- [ ] Test coverage > 85%
- [ ] Funzioni max 50 linee
- [ ] Performance: +20% su documenti >1000 articoli
- [ ] Zero regressioni

### v2.2.0 Target
- [ ] Test coverage > 90%
- [ ] Type hints 100%
- [ ] Documentazione Sphinx completa
- [ ] CI/CD con multiple Python versions

### v3.0.0 Target
- [ ] Architettura modulare completa
- [ ] Plugin system
- [ ] Multiple output formats (MD, HTML, PDF)
- [ ] Batch mode production-ready

---

## 📋 Issue GitHub da Creare

### Enhancement
1. **[Performance] Precompile regex patterns** - v2.1.0
2. **[Feature] Robust HTML parsing with BeautifulSoup** - v2.1.0
3. **[Feature] Network retry logic** - v2.1.0
4. **[DX] Add type hints throughout codebase** - v2.2.0
5. **[Feature] Configuration file support** - v3.0.0
6. **[Feature] Batch processing mode** - v3.0.0

### Bug
1. **[Bug] Complete footnote implementation with global counter** - v2.1.0

### Refactor
1. **[Refactor] Split main() into smaller functions** - v2.1.0
2. **[Refactor] Modularize codebase into package** - v3.0.0

### Documentation
1. **[Docs] Setup Sphinx documentation** - v2.2.0
2. **[Docs] API reference with examples** - v2.2.0

### Testing
1. **[Testing] Add integration tests** - v2.1.0
2. **[Testing] Add network error scenarios** - v2.1.0

### CI/CD
1. **[CI] Complete GitHub Actions pipeline** - v2.2.0
2. **[CI] Automated changelog generation** - v2.2.0

---

## 🎯 Timeline Proposta

**Q4 2025 (Novembre-Dicembre)**:
- v2.1.0: High priority refactoring items
- Focus: Performance + Robustezza

**Q1 2026 (Gennaio-Marzo)**:
- v2.2.0: Medium priority items
- Focus: DX + Documentation

**Q2-Q4 2026**:
- v3.0.0: Major architecture + advanced features
- Focus: Modularizzazione + Plugin system

---

## 📝 Note

- Mantenere backward compatibility per `akoma2md` fino a v3.0.0
- Deprecation warning per `akoma2md` command da v3.0.0
- Rimozione `akoma2md` command in v4.0.0
- Semantic versioning rigoroso
- Security patches immediate su tutte le versioni supportate

---

**Ultimo aggiornamento**: 2025-12-03
**Versione corrente**: v2.0.18
