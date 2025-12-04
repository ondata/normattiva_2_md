# 🏗️ Architettura API Programmabile

## Principi Guida

### 1. Non-Breaking Changes
- Zero modifiche alle funzioni esistenti
- CLI mantiene 100% compatibilità
- Nuove funzionalità = nuovi file

### 2. Separation of Concerns
```
CLI (cli.py)
    ↓
API Layer (api.py)  ← NUOVO
    ↓
Core Logic (esistente)
    ├── markdown_converter.py
    ├── normattiva_api.py
    ├── exa_api.py
    └── xml_parser.py
```

### 3. DRY (Don't Repeat Yourself)
- CLI chiama API layer
- API layer chiama core logic
- Nessuna duplicazione logica

### 4. Progressive Disclosure
```python
# Semplice: funzione standalone
result = convert_url("https://...")

# Avanzato: classe con configurazione
conv = Converter(config=...)
result = conv.convert_url("https://...")
```

## Struttura File

### File Nuovi

#### `src/normattiva2md/exceptions.py`
```python
"""
Custom exceptions per errori gravi.
Seguono gerarchia standard Python.
"""

class Normattiva2MDError(Exception):
    """Base exception for all errors"""

class InvalidURLError(Normattiva2MDError):
    """URL non valido o dominio non permesso"""

class FileNotFoundError(Normattiva2MDError):
    """File XML non trovato"""

class APIKeyError(Normattiva2MDError):
    """Exa API key mancante o invalida"""

class ConversionError(Normattiva2MDError):
    """Errore generico durante conversione"""
```

#### `src/normattiva2md/models.py`
```python
"""
Dataclasses per oggetti ritornati dall'API.
Usano @dataclass per semplicità.
"""

from dataclasses import dataclass
from typing import Optional, Dict

@dataclass
class ConversionResult:
    """Risultato di una conversione"""
    markdown: str
    metadata: Dict
    url: Optional[str] = None
    url_xml: Optional[str] = None
    
    def __str__(self) -> str:
        """Conversione automatica a string = markdown"""
        return self.markdown
    
    def save(self, path: str) -> None:
        """Salva markdown su file"""

@dataclass
class SearchResult:
    """Singolo risultato di ricerca"""
    url: str
    title: str
    score: float
```

#### `src/normattiva2md/api.py`
```python
"""
High-level API per uso programmabile.

Due interfacce:
1. Funzioni standalone (semplici)
2. Classe Converter (avanzata, stateful)
"""

# Funzioni standalone
def convert_url(...) -> Optional[ConversionResult]
def convert_xml(...) -> Optional[ConversionResult]
def search_law(...) -> List[SearchResult]

# Classe per uso avanzato
class Converter:
    """Converter con configurazione persistente"""
    
    def __init__(
        self,
        exa_api_key: Optional[str] = None,
        quiet: bool = False,
        keep_xml: bool = False
    ):
        """Inizializza converter con config"""
    
    def convert_url(...) -> Optional[ConversionResult]
    def convert_xml(...) -> Optional[ConversionResult]
    def search(...) -> List[SearchResult]
    def search_and_convert(...) -> Optional[ConversionResult]
```

### File Modificati

#### `src/normattiva2md/__init__.py`
```python
"""
Esporta API pubblica.
Questo è il punto di ingresso per utenti.
"""

from .api import (
    convert_url,
    convert_xml,
    search_law,
    Converter,
)
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
    # Funzioni
    "convert_url",
    "convert_xml",
    "search_law",
    # Classi
    "Converter",
    "ConversionResult",
    "SearchResult",
    # Eccezioni
    "Normattiva2MDError",
    "InvalidURLError",
    "FileNotFoundError",
    "APIKeyError",
    "ConversionError",
    # Version
    "__version__",
]
```

#### `src/normattiva2md/cli.py` (modifiche minime)
- Wrappa chiamate esistenti con try/except per nuove eccezioni
- Nessun refactoring pesante (rischio breaking)
- Mantiene compatibilità 100%

## Pattern: Gestione Errori Ibrida

### Errori Gravi → Eccezioni
```python
# Sollevano eccezione
- URL invalido/non sicuro
- File non esiste
- API key mancante (quando richiesta)
- Errore parsing XML
- Network error critico
```

### Errori Soft → None
```python
# Ritornano None
- Articolo non trovato nel documento
- Ricerca senza risultati
- Conversione parzialmente fallita ma recuperabile
```

### Implementazione
```python
def convert_url(url: str, ...) -> Optional[ConversionResult]:
    # Validazione URL → ECCEZIONE se grave
    try:
        validate_normattiva_url(url)
    except ValueError as e:
        raise InvalidURLError(f"URL non valido: {e}")
    
    # Download XML
    xml_path = download_xml(url)
    if not xml_path:
        # Network error soft → None
        logger.warning(f"Download fallito per {url}")
        return None
    
    # Conversione
    try:
        result = _convert_xml_internal(xml_path, ...)
        return result
    except Exception as e:
        # Parse error grave → ECCEZIONE
        raise ConversionError(f"Errore conversione: {e}")
```

## Pattern: Logging vs Print

### Regola
- **CLI**: usa `print()` su stderr (comportamento attuale)
- **API**: usa `logging` module

### Implementazione
```python
import logging

logger = logging.getLogger(__name__)

def convert_url(url: str, quiet: bool = False) -> Optional[ConversionResult]:
    if not quiet:
        logger.info(f"Converting URL: {url}")
    
    # ...
    
    if not quiet:
        logger.info("Conversion completed")
    
    return result
```

### Configurazione Utente
```python
# Utente può configurare logging
import logging

logging.basicConfig(level=logging.INFO)

# Oppure disabilitare
logging.getLogger('normattiva2md').setLevel(logging.WARNING)
```

## Pattern: Preparazione per Async

### Struttura Codice
Separa "logica" da "I/O" per facilitare future versioni async.

```python
# ATTUALE (sincrono)
def convert_url(url: str) -> Optional[ConversionResult]:
    xml_data = _download_xml_sync(url)      # I/O
    result = _process_xml(xml_data)         # Logica
    return result

# FUTURO (async) - facile da aggiungere
async def convert_url_async(url: str) -> Optional[ConversionResult]:
    xml_data = await _download_xml_async(url)  # I/O async
    result = _process_xml(xml_data)             # Stessa logica!
    return result
```

### Benefici
- Logica riusabile tra sync/async
- Facile aggiunta versioni async in futuro
- Test più semplici (mock I/O)

## Diagramma Flusso

```
┌─────────────────────────────────────────────┐
│  User Code (notebook/script)                │
├─────────────────────────────────────────────┤
│                                             │
│  from normattiva2md import convert_url     │
│                                             │
│  result = convert_url("https://...")       │
│                                             │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│  API Layer (api.py) - NUOVO                 │
├─────────────────────────────────────────────┤
│                                             │
│  def convert_url(url, ...):                 │
│    1. Validate URL → InvalidURLError        │
│    2. Load ENV → load_env_file()            │
│    3. Download XML → _download_wrapper()    │
│    4. Convert → _convert_wrapper()          │
│    5. Return ConversionResult               │
│                                             │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│  Core Logic (esistente)                     │
├─────────────────────────────────────────────┤
│                                             │
│  • validate_normattiva_url()                │
│  • extract_params_from_normattiva_url()     │
│  • download_akoma_ntoso()                   │
│  • convert_akomantoso_to_markdown_improved()│
│  • extract_metadata_from_xml()              │
│                                             │
└─────────────────────────────────────────────┘
```

## Compatibilità CLI

Il CLI continua a funzionare esattamente come prima:

```python
# cli.py (semplificato)

def main():
    args = parse_args()
    
    # Può opzionalmente usare la nuova API internamente
    # MA il comportamento esterno rimane identico
    
    if args.input_source:
        # Comportamento attuale mantenuto
        if is_normattiva_url(args.input_source):
            # ... logica esistente ...
        else:
            # ... logica esistente ...
```

**Nota**: Il refactoring del CLI per usare l'API è OPZIONALE e può essere fatto in futuro. Per ora, CLI e API coesistono separatamente.
