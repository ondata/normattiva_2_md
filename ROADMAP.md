# Roadmap - normattiva2md

Pianificazione release future e miglioramenti programmati.

**Versione corrente**: v2.1.0

Per cronologia dettagliata rilasci vedere [LOG.md](LOG.md).

---

## ✅ COMPLETATO - v2.1.0 (2026-01-01)

### API Programmabile Python

**Implementato**: API completa per uso programmatico da notebook e script Python

**Componenti creati**:
- `src/normattiva2md/api.py`: Funzioni standalone e classe Converter
- `src/normattiva2md/models.py`: Dataclass ConversionResult e SearchResult
- `src/normattiva2md/exceptions.py`: Gerarchia eccezioni custom

**Funzioni pubbliche**:
```python
from normattiva2md import convert_url, convert_xml, search_law, Converter

# Quick usage
result = convert_url("https://www.normattiva.it/...")
print(result.title)
result.save("output.md")

# Advanced usage
converter = Converter(quiet=True)
result = converter.search_and_convert("legge stanca")
```

**Eccezioni custom**:
- `Normattiva2MDError` (base)
- `InvalidURLError`, `XMLFileNotFoundError`, `APIKeyError`, `ConversionError`

**Benefici**:
- 100% backward compatible (CLI invariato)
- Uso in Jupyter notebooks
- Batch processing programmabile
- Type hints completi
- Logging invece di print()

**Documentazione**: README.md aggiornato con esempi, `examples/basic_usage.py`, `examples/batch_processing.py`

---

## 🟡 IN SVILUPPO - v2.2.0

### 1. Fix HTML Parsing Fragility

**Problema**: Uso regex per parsing HTML nella funzione `extract_params_from_normattiva_url()`

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

**File**: `src/normattiva2md/normattiva_api.py:147-170`

---

### 2. Network Error Recovery

**Problema**: Nessun retry su errori di rete nelle funzioni `extract_params_from_normattiva_url()` e `download_akoma_ntoso()`

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

**File**: `src/normattiva2md/normattiva_api.py:124, 201`

---

### 3. Complete Footnote Implementation

**Problema**: Implementazione semplificata senza global counter nella funzione `clean_text_content()`

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

**File**: `src/normattiva2md/markdown_converter.py:159-165`

---

### 4. Precompile Regex Patterns

**Problema**: Pattern regex compilati ad ogni chiamata (performance)

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

**File**: Multipli moduli in `src/normattiva2md/` (normattiva_api.py, markdown_converter.py, xml_parser.py, akoma_utils.py, utils.py)

---

## 🟢 MEDIUM PRIORITY - v2.3.0

### 5. Type Hints

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

### 6. API Documentation con Sphinx

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

### 7. CI/CD Pipeline Completo

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

### 8. Version Management

**Single source of truth**:
```python
# src/normattiva2md/__version__.py
__version__ = "2.1.0"

# pyproject.toml (recommended)
[project]
version = "2.1.0"
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

### 9. Optional Dependencies

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
    "normattiva2md[dev,test,html]"
]
```

**Installazione**:
```bash
pip install normattiva2md[dev]    # per sviluppo
pip install normattiva2md[html]   # per HTML parsing robusto
pip install normattiva2md[all]    # tutto
```

---

## 🟢 PLANNED - EUR-Lex Integration (v2.4.0)

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

**Benefici**:
✅ Complementare a Normattiva (UE + IT)
✅ Workflow già validato e testato
✅ Nessun parser XML custom (usa html2text)
✅ 80% codice già implementato
✅ API EUR-Lex gratuita e stabile

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

## 🔵 LOW PRIORITY - Future (v3.0.0)

### 10. Configuration File Support

**Feature**: `.normattiva2md.yml` per configurazione

```yaml
# .normattiva2md.yml
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
        '.normattiva2md.yml',
        '~/.config/normattiva2md/config.yml'
    ]
    for path in config_paths:
        if os.path.exists(path):
            with open(path) as f:
                return yaml.safe_load(f)
    return {}
```

---

### 11. Internazionalizzazione (i18n)

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

### 12. Batch Processing Mode

**CLI**:
```bash
# Da file con lista URL
normattiva2md --batch urls.txt --output-dir ./output/

# Con parallelizzazione
normattiva2md --batch urls.txt -o ./out/ --parallel 4
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

### 13. Validation Mode

**CLI**:
```bash
# Solo validazione, no conversione
normattiva2md --validate input.xml

# Con report dettagliato
normattiva2md --validate input.xml --verbose
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

## 📊 Metriche di Successo

### v2.2.0 Target
- [ ] Test coverage > 85%
- [ ] Funzioni max 50 linee
- [ ] Performance: +20% su documenti >1000 articoli
- [ ] Zero regressioni

### v2.3.0 Target
- [ ] Test coverage > 90%
- [ ] Type hints 100%
- [ ] Documentazione Sphinx completa
- [ ] CI/CD con multiple Python versions

### v3.0.0 Target
- [x] Architettura modulare completa (✅ completato in v2.0.23)
- [ ] Plugin system
- [ ] Multiple output formats (MD, HTML, PDF)
- [ ] Batch mode production-ready

---

## 📋 Issue GitHub da Creare

### Enhancement
1. **[Performance] Precompile regex patterns** - v2.2.0
2. **[Feature] Robust HTML parsing with BeautifulSoup** - v2.2.0
3. **[Feature] Network retry logic** - v2.2.0
4. **[DX] Add type hints throughout codebase** - v2.3.0
5. **[Feature] Configuration file support** - v3.0.0
6. **[Feature] Batch processing mode** - v3.0.0

### Bug
1. **[Bug] Complete footnote implementation with global counter** - v2.2.0

### Documentation
1. **[Docs] Setup Sphinx documentation** - v2.3.0
2. **[Docs] API reference with examples** - v2.3.0

### CI/CD
1. **[CI] Complete GitHub Actions pipeline** - v2.3.0
2. **[CI] Automated changelog generation** - v2.3.0

---

## 🎯 Timeline Proposta

**Q1 2026 (Gennaio-Marzo)**:
- v2.2.0: Feature non implementate v2.1.0
- Focus: Robustezza + Performance

**Q2 2026 (Aprile-Giugno)**:
- v2.3.0: Medium priority items
- Focus: DX + Documentation

**Q3-Q4 2026**:
- v2.4.0: EUR-Lex Integration
- v3.0.0: Major architecture + advanced features
- Focus: Plugin system + Multiple output formats

---

## 📝 Note

- Mantenere backward compatibility per CLI fino a v3.0.0
- Semantic versioning rigoroso
- Security patches immediate su tutte le versioni supportate
- Cronologia dettagliata in [LOG.md](LOG.md)

---

**Ultimo aggiornamento**: 2026-01-01
**Versione corrente**: v2.1.0
