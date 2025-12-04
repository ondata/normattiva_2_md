# 🚀 Piano Implementazione

## Overview

Implementazione incrementale in 5 fasi con test continuo.
Ogni fase è auto-contenuta e testabile indipendentemente.

---

## Fase 1: Foundation (Core Structures)

**Obiettivo**: Creare strutture base senza logica business

**File da creare:**
1. `src/normattiva2md/exceptions.py`
2. `src/normattiva2md/models.py`

**Durata stimata**: 1-2 ore

### Tasks

#### 1.1 Exceptions
```bash
# Create file
touch src/normattiva2md/exceptions.py
```

**Contenuto**: Vedi `04-exceptions.md`

**Checklist:**
- [ ] Classe base `Normattiva2MDError`
- [ ] `InvalidURLError`
- [ ] `FileNotFoundError` 
- [ ] `APIKeyError`
- [ ] `ConversionError`
- [ ] Docstrings complete
- [ ] Examples in docstrings

#### 1.2 Models
```bash
# Create file
touch src/normattiva2md/models.py
```

**Contenuto**: Vedi `03-models.md`

**Checklist:**
- [ ] `ConversionResult` dataclass
- [ ] `SearchResult` dataclass
- [ ] Metodo `ConversionResult.save()`
- [ ] Properties: `title`, `data_gu`, etc.
- [ ] `__str__()` methods
- [ ] Docstrings complete
- [ ] Type hints with `from __future__ import annotations`

#### 1.3 Test Foundation
```bash
# Create test file
touch tests/test_models.py
touch tests/test_exceptions.py
```

**Test models:**
- [ ] `ConversionResult` creation
- [ ] `ConversionResult.__str__()`
- [ ] `ConversionResult.save()`
- [ ] `ConversionResult.title` property
- [ ] `SearchResult` creation
- [ ] `SearchResult.__str__()`

**Test exceptions:**
- [ ] Gerarchia ereditarietà
- [ ] Catching con base class
- [ ] Message formatting

**Verifica:**
```bash
python -m pytest tests/test_models.py -v
python -m pytest tests/test_exceptions.py -v
```

---

## Fase 2: Core API Functions

**Obiettivo**: Implementare funzioni standalone che wrappano codice esistente

**File da creare:**
1. `src/normattiva2md/api.py` (partial - solo funzioni)

**Durata stimata**: 4-6 ore

### Tasks

#### 2.1 API Core Structure
```bash
touch src/normattiva2md/api.py
```

**Struttura iniziale:**
```python
"""
High-level API for programmatic use.
"""

from __future__ import annotations

import logging
import os
import tempfile
from typing import Optional, Dict, List

from .models import ConversionResult, SearchResult
from .exceptions import (
    InvalidURLError,
    FileNotFoundError,
    APIKeyError,
    ConversionError,
)
from .utils import load_env_file
# Import existing functions
from .normattiva_api import (
    is_normattiva_url,
    validate_normattiva_url,
    extract_params_from_normattiva_url,
    download_akoma_ntoso,
)
from .markdown_converter import convert_akomantoso_to_markdown_improved
from .xml_parser import extract_metadata_from_xml
from .exa_api import lookup_normattiva_url

logger = logging.getLogger(__name__)
```

#### 2.2 Implement `convert_url()`

**Checklist:**
- [ ] Firma funzione con type hints
- [ ] Docstring completo con examples
- [ ] Load `.env` automatico
- [ ] Validazione URL → `InvalidURLError`
- [ ] Download XML
- [ ] Conversione con existing functions
- [ ] Costruzione `ConversionResult`
- [ ] Logging appropriato
- [ ] Gestione errori (eccezioni vs None)
- [ ] Test parametro `article`
- [ ] Test parametro `with_urls`
- [ ] Test parametro `with_references`

**Pseudo-code:**
```python
def convert_url(
    url: str,
    article: Optional[str] = None,
    with_urls: bool = False,
    with_references: bool = False,
    output_dir: Optional[str] = None,
    quiet: bool = False,
) -> Optional[ConversionResult]:
    # Load ENV
    load_env_file()
    
    # Validate URL → exception if invalid
    try:
        validate_normattiva_url(url)
    except ValueError as e:
        raise InvalidURLError(f"URL non valido: {e}")
    
    # Configure logging
    if quiet:
        logger.setLevel(logging.WARNING)
    
    # Extract params
    params, session = extract_params_from_normattiva_url(url, quiet=quiet)
    if not params:
        logger.warning(f"Impossibile estrarre parametri da {url}")
        return None  # Soft error
    
    # Download XML
    with tempfile.NamedTemporaryFile(suffix='.xml', delete=False) as tmp:
        xml_path = tmp.name
    
    success = download_akoma_ntoso(params, xml_path, session, quiet=quiet)
    if not success:
        logger.warning(f"Download fallito per {url}")
        return None  # Soft error
    
    # Build metadata
    metadata = {
        'dataGU': params['dataGU'],
        'codiceRedaz': params['codiceRedaz'],
        'dataVigenza': params['dataVigenza'],
        'url': url,
        'url_xml': f"https://www.normattiva.it/do/atto/caricaAKN?...",
    }
    
    # Convert
    try:
        success = convert_akomantoso_to_markdown_improved(
            xml_path,
            None,  # No file output, we'll capture markdown
            metadata,
            article,
            with_urls=with_urls,
        )
        # ... read markdown from temp file or modify function ...
    except Exception as e:
        raise ConversionError(f"Errore conversione: {e}")
    
    # Cleanup
    if not keep_xml:
        os.remove(xml_path)
    
    return ConversionResult(
        markdown=markdown_content,
        metadata=metadata,
        url=url,
        url_xml=metadata['url_xml'],
    )
```

**Nota**: Potrebbe richiedere piccola modifica a `convert_akomantoso_to_markdown_improved()` per ritornare markdown invece di scrivere file.

#### 2.3 Implement `convert_xml()`

**Checklist:**
- [ ] Firma funzione
- [ ] Docstring completo
- [ ] Check file exists → `FileNotFoundError`
- [ ] Parse XML → `ConversionError`
- [ ] Extract metadata da XML
- [ ] Conversione
- [ ] Costruzione `ConversionResult`
- [ ] Logging

#### 2.4 Implement `search_law()`

**Checklist:**
- [ ] Firma funzione
- [ ] Docstring completo
- [ ] Load ENV per API key
- [ ] Check API key → `APIKeyError`
- [ ] Call `lookup_normattiva_url()` esistente
- [ ] Parse risultati in `List[SearchResult]`
- [ ] Return lista vuota se nessun risultato
- [ ] Logging

#### 2.5 Test API Functions

```bash
touch tests/test_api.py
```

**Test `convert_url()`:**
- [ ] Conversione base da URL
- [ ] Con parametro `article`
- [ ] Con `with_urls=True`
- [ ] URL invalido solleva `InvalidURLError`
- [ ] Articolo non trovato ritorna `None`
- [ ] Mock network calls

**Test `convert_xml()`:**
- [ ] Conversione da file esistente
- [ ] File non esiste solleva `FileNotFoundError`
- [ ] XML malformato solleva `ConversionError`

**Test `search_law()`:**
- [ ] Ricerca con risultati
- [ ] Ricerca senza risultati (lista vuota)
- [ ] API key mancante solleva `APIKeyError`
- [ ] Mock Exa API

**Verifica:**
```bash
python -m pytest tests/test_api.py -v
```

---

## Fase 3: Converter Class

**Obiettivo**: Implementare classe per uso avanzato

**File da modificare:**
1. `src/normattiva2md/api.py` (add class)

**Durata stimata**: 3-4 ore

### Tasks

#### 3.1 Implement `Converter` Class

**Checklist:**
- [ ] `__init__()` con parametri configurazione
- [ ] Store config: `exa_api_key`, `quiet`, `keep_xml`
- [ ] Metodo `convert_url()` che chiama funzione standalone
- [ ] Metodo `convert_xml()` che chiama funzione standalone
- [ ] Metodo `search()` che chiama `search_law()`
- [ ] Metodo `search_and_convert()` nuovo
- [ ] Docstrings completi
- [ ] Type hints

**Structure:**
```python
class Converter:
    def __init__(
        self,
        exa_api_key: Optional[str] = None,
        quiet: bool = False,
        keep_xml: bool = False,
    ):
        self.exa_api_key = exa_api_key or os.getenv('EXA_API_KEY')
        self.quiet = quiet
        self.keep_xml = keep_xml
    
    def convert_url(self, url: str, **kwargs) -> Optional[ConversionResult]:
        # Merge instance config with kwargs
        kwargs.setdefault('quiet', self.quiet)
        return convert_url(url, **kwargs)
    
    def search(self, query: str, **kwargs) -> List[SearchResult]:
        kwargs.setdefault('exa_api_key', self.exa_api_key)
        kwargs.setdefault('quiet', self.quiet)
        return search_law(query, **kwargs)
    
    def search_and_convert(
        self,
        query: str,
        article: Optional[str] = None,
        use_best: bool = True,
        **kwargs
    ) -> Optional[ConversionResult]:
        # Search
        results = self.search(query)
        if not results:
            return None
        
        # Use best result
        if use_best:
            url = results[0].url
        else:
            # Interactive selection (futuro)
            url = self._select_interactive(results)
        
        # Convert
        return self.convert_url(url, article=article, **kwargs)
```

#### 3.2 Test Converter Class

**Checklist:**
- [ ] Inizializzazione con config
- [ ] Config persistente tra chiamate
- [ ] `convert_url()` con config
- [ ] `search()` con config
- [ ] `search_and_convert()` pipeline completa
- [ ] Override config con kwargs

**Verifica:**
```bash
python -m pytest tests/test_api.py::TestConverterClass -v
```

---

## Fase 4: Exports & Documentation

**Obiettivo**: Esportare API pubblica e documentare

**File da modificare:**
1. `src/normattiva2md/__init__.py`
2. `README.md`
3. `docs/notebook_examples.md` (new)

**Durata stimata**: 3-4 ore

### Tasks

#### 4.1 Update `__init__.py`

```python
"""
normattiva2md - Convert Akoma Ntoso XML to Markdown

CLI usage:
    normattiva2md input.xml output.md

API usage:
    from normattiva2md import convert_url
    result = convert_url("https://www.normattiva.it/...")
"""

from .api import convert_url, convert_xml, search_law, Converter
from .models import ConversionResult, SearchResult
from .exceptions import (
    Normattiva2MDError,
    InvalidURLError,
    FileNotFoundError,
    APIKeyError,
    ConversionError,
)
from .constants import VERSION

__version__ = VERSION
__all__ = [
    # Core functions
    "convert_url",
    "convert_xml",
    "search_law",
    # Classes
    "Converter",
    "ConversionResult",
    "SearchResult",
    # Exceptions
    "Normattiva2MDError",
    "InvalidURLError",
    "FileNotFoundError",
    "APIKeyError",
    "ConversionError",
    # Version
    "__version__",
]
```

**Checklist:**
- [ ] Import tutte le funzioni pubbliche
- [ ] Import models
- [ ] Import exceptions
- [ ] `__all__` list completa
- [ ] Docstring module-level

#### 4.2 Update README.md

Aggiungere sezione dopo "💻 Utilizzo":

**Checklist:**
- [ ] Sezione "🐍 Utilizzo come Libreria Python"
- [ ] Quick start examples
- [ ] Link a `docs/notebook_examples.md`
- [ ] Esempi gestione errori
- [ ] Badge PyPI aggiornato

#### 4.3 Create `docs/notebook_examples.md`

Vedi `06-examples.md` per contenuto completo.

**Checklist:**
- [ ] Importazione base
- [ ] Esempio conversione URL
- [ ] Esempio conversione XML
- [ ] Esempio ricerca
- [ ] Esempio batch processing
- [ ] Esempio gestione errori
- [ ] Esempio classe Converter
- [ ] Esempio search_and_convert

#### 4.4 Add Docstrings

**Checklist:**
- [ ] Tutte le funzioni pubbliche hanno docstring
- [ ] Tutti i parametri documentati
- [ ] Tutti i return values documentati
- [ ] Tutte le eccezioni documentate
- [ ] Examples in docstrings
- [ ] Type hints corretti

---

## Fase 5: Examples & Polish

**Obiettivo**: Creare esempi pratici e finalizzare

**File da creare:**
1. `examples/notebook_quickstart.ipynb`
2. `examples/basic_usage.py`
3. `examples/batch_processing.py`
4. `examples/error_handling.py`

**Durata stimata**: 2-3 ore

### Tasks

#### 5.1 Create Jupyter Notebook

```bash
mkdir -p examples
touch examples/notebook_quickstart.ipynb
```

**Contenuto notebook:**
- [ ] Installazione
- [ ] Importazione
- [ ] Conversione base
- [ ] Ricerca
- [ ] Batch processing
- [ ] Gestione errori
- [ ] Tips & tricks

#### 5.2 Create Python Examples

**`examples/basic_usage.py`:**
```python
"""
Basic usage examples for normattiva2md API.
"""

from normattiva2md import convert_url

# Simple conversion
result = convert_url("https://www.normattiva.it/uri-res/N2Ls?urn:...")
print(result.markdown[:200])
print(result.metadata)
result.save("output.md")
```

**`examples/batch_processing.py`:**
```python
"""
Batch convert multiple URLs.
"""

from normattiva2md import Converter

urls = [
    "https://www.normattiva.it/...",
    "https://www.normattiva.it/...",
]

conv = Converter(quiet=True)
for i, url in enumerate(urls):
    result = conv.convert_url(url)
    if result:
        result.save(f"legge_{i:02d}.md")
```

**`examples/error_handling.py`:**
```python
"""
Proper error handling examples.
"""

from normattiva2md import convert_url, InvalidURLError, ConversionError

try:
    result = convert_url("https://...")
except InvalidURLError as e:
    print(f"URL invalido: {e}")
except ConversionError as e:
    print(f"Errore conversione: {e}")
else:
    if result:
        print("Success!")
    else:
        print("Conversione fallita (errore soft)")
```

#### 5.3 Final Testing

**Integration tests:**
```bash
# Test installazione package
pip install -e .

# Test import
python -c "from normattiva2md import convert_url, Converter; print('OK')"

# Test esempi
python examples/basic_usage.py
python examples/batch_processing.py
python examples/error_handling.py

# Test notebook (se jupyter installato)
jupyter nbconvert --execute examples/notebook_quickstart.ipynb
```

**Checklist:**
- [ ] Tutti i test passano
- [ ] Esempi funzionano
- [ ] Documentazione completa
- [ ] Type hints validati con mypy (opzionale)
- [ ] Nessun warning durante import
- [ ] CLI continua a funzionare

---

## Fase 6: Release Preparation

**Obiettivo**: Preparare release

**Durata stimata**: 1-2 ore

### Tasks

#### 6.1 Version Bump

**File da modificare:**
- `pyproject.toml`
- `setup.py`
- `src/normattiva2md/constants.py`

```bash
# Esempio: 2.0.22 → 2.1.0
VERSION = "2.1.0"
```

**Checklist:**
- [ ] Version bumped in tutti i file
- [ ] Version consistente ovunque
- [ ] `normattiva2md --version` corretto

#### 6.2 Update CHANGELOG

Aggiungere a `LOG.md`:

```markdown
## 2025-12-XX

### Added
- 🐍 API programmabile per uso in notebook e script Python
- Funzioni standalone: `convert_url()`, `convert_xml()`, `search_law()`
- Classe `Converter` per uso avanzato con configurazione persistente
- Models: `ConversionResult`, `SearchResult`
- Exceptions: `Normattiva2MDError` e sottoclassi
- Documentazione completa: `docs/notebook_examples.md`
- Esempi pratici in `examples/`
- Jupyter notebook quickstart

### Changed
- `__init__.py` esporta API pubblica
- README con sezione uso programmabile

### Maintained
- 100% compatibilità CLI esistente
- Nessuna breaking change
```

#### 6.3 Final Checks

**Checklist:**
- [ ] Tutti i test passano
- [ ] Documentazione aggiornata
- [ ] Examples funzionanti
- [ ] Version corretta
- [ ] CHANGELOG aggiornato
- [ ] README aggiornato
- [ ] No TODO o FIXME in codice produzione
- [ ] Licenza presente

#### 6.4 Build & Test

```bash
# Clean build
rm -rf dist/ build/ *.egg-info

# Build package
python -m build

# Test install from build
pip install dist/normattiva2md-2.1.0-py3-none-any.whl

# Verify
python -c "from normattiva2md import convert_url, __version__; print(__version__)"

# Test CLI
normattiva2md --version
```

#### 6.5 Release

```bash
# Tag version
git add .
git commit -m "Release v2.1.0 - Add programmatic API"
git tag v2.1.0
git push origin main --tags

# Upload to PyPI (se hai credenziali)
python -m twine upload dist/*
```

---

## Timeline Totale

| Fase | Durata | Milestone |
|------|--------|-----------|
| Fase 1 | 1-2h | Models & Exceptions |
| Fase 2 | 4-6h | API Functions |
| Fase 3 | 3-4h | Converter Class |
| Fase 4 | 3-4h | Docs & Exports |
| Fase 5 | 2-3h | Examples |
| Fase 6 | 1-2h | Release |
| **Totale** | **14-21h** | **Complete API** |

## Dipendenze tra Fasi

```
Fase 1 (Foundation)
    ↓
Fase 2 (API Functions) → Fase 3 (Converter Class)
    ↓                           ↓
Fase 4 (Documentation) ← ←  ← ←
    ↓
Fase 5 (Examples)
    ↓
Fase 6 (Release)
```

- Fase 1 è prerequisito per tutto
- Fase 2 e 3 possono sovrapporsi parzialmente
- Fase 4-6 sono sequenziali

## Rischi & Mitigazioni

| Rischio | Probabilità | Impatto | Mitigazione |
|---------|-------------|---------|-------------|
| Breaking change accidentale al CLI | Media | Alto | Test regressione CLI completi |
| Funzioni esistenti non ritornano markdown | Media | Medio | Piccola modifica o wrapper |
| Gestione temp files complessa | Bassa | Basso | Usa `tempfile` module |
| Logging interferisce con CLI | Bassa | Medio | Logger separati per CLI vs API |

## Success Criteria

- [ ] Tutte le funzioni API documentate e testate
- [ ] Almeno 3 esempi funzionanti
- [ ] CLI funziona identicamente a prima
- [ ] Tutti i test passano (vecchi + nuovi)
- [ ] Documentazione completa
- [ ] Release su PyPI
