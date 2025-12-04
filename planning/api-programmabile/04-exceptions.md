# ⚠️ Exceptions - Sistema Gestione Errori

File: `src/normattiva2md/exceptions.py`

## Implementazione Completa

```python
"""
Custom exceptions per normattiva2md.

Gerarchia:
    Exception
    └── Normattiva2MDError (base)
        ├── InvalidURLError
        ├── FileNotFoundError
        ├── APIKeyError
        └── ConversionError

Strategia gestione errori:
- Errori GRAVI → Eccezioni (URL invalido, file non esiste)
- Errori SOFT → None (articolo non trovato, ricerca senza risultati)
"""


class Normattiva2MDError(Exception):
    """
    Eccezione base per tutti gli errori di normattiva2md.
    
    Tutti gli errori specifici del package derivano da questa classe.
    Permette di catturare tutti gli errori del package con un singolo except.
    
    Examples:
        >>> try:
        ...     result = convert_url("https://...")
        ... except Normattiva2MDError as e:
        ...     print(f"Errore normattiva2md: {e}")
    """
    pass


class InvalidURLError(Normattiva2MDError):
    """
    Sollevata quando URL non è valido o sicuro.
    
    Casi:
    - URL non è HTTPS
    - Dominio non è normattiva.it
    - URL contiene path traversal
    - URL malformato
    
    Examples:
        >>> from normattiva2md import convert_url, InvalidURLError
        >>> 
        >>> try:
        ...     result = convert_url("http://invalid-domain.com/...")
        ... except InvalidURLError as e:
        ...     print(f"URL non valido: {e}")
    """
    pass


class FileNotFoundError(Normattiva2MDError):
    """
    Sollevata quando file XML locale non esiste.
    
    Nota: Sovrascrive built-in FileNotFoundError per consistenza
    con gerarchia Normattiva2MDError.
    
    Examples:
        >>> from normattiva2md import convert_xml, FileNotFoundError
        >>> 
        >>> try:
        ...     result = convert_xml("/path/non/esistente.xml")
        ... except FileNotFoundError as e:
        ...     print(f"File non trovato: {e}")
    """
    pass


class APIKeyError(Normattiva2MDError):
    """
    Sollevata quando Exa API key mancante o invalida.
    
    Casi:
    - API key non configurata (né ENV né parametro)
    - API key invalida (HTTP 401/403 da Exa)
    - API key scaduta
    
    Examples:
        >>> from normattiva2md import search_law, APIKeyError
        >>> 
        >>> try:
        ...     results = search_law("legge stanca")
        ... except APIKeyError as e:
        ...     print(f"Configura EXA_API_KEY: {e}")
    """
    pass


class ConversionError(Normattiva2MDError):
    """
    Sollevata quando errore durante conversione XML → Markdown.
    
    Casi:
    - XML malformato/corrotto
    - Parsing XML fallito
    - Struttura XML non riconosciuta
    - Errore I/O durante conversione
    
    Examples:
        >>> from normattiva2md import convert_xml, ConversionError
        >>> 
        >>> try:
        ...     result = convert_xml("corrupted.xml")
        ... except ConversionError as e:
        ...     print(f"Errore conversione: {e}")
    """
    pass
```

## Strategia Gestione Errori

### Errori GRAVI → Eccezioni

Sollevano eccezioni che interrompono l'esecuzione:

| Errore | Eccezione | Quando |
|--------|-----------|--------|
| URL non HTTPS | `InvalidURLError` | `convert_url()` |
| Dominio non permesso | `InvalidURLError` | `convert_url()` |
| File non esiste | `FileNotFoundError` | `convert_xml()` |
| XML corrotto | `ConversionError` | `convert_xml()`, `convert_url()` |
| API key mancante | `APIKeyError` | `search_law()` |
| API key invalida | `APIKeyError` | `search_law()` |

### Errori SOFT → None + Warning

Ritornano `None` o lista vuota con warning log:

| Errore | Ritorno | Quando |
|--------|---------|--------|
| Articolo non trovato | `None` | `convert_url(article="...")` |
| Download fallito (network) | `None` | `convert_url()` |
| Ricerca senza risultati | `[]` | `search_law()` |
| Timeout ricerca | `[]` | `search_law()` |

## Pattern di Utilizzo

### 1. Cattura Specifica

```python
from normattiva2md import (
    convert_url,
    InvalidURLError,
    ConversionError,
)

try:
    result = convert_url("https://...")
except InvalidURLError:
    print("URL non valido, controlla il link")
except ConversionError:
    print("Errore durante conversione, XML potrebbe essere corrotto")
```

### 2. Cattura Generica

```python
from normattiva2md import convert_url, Normattiva2MDError

try:
    result = convert_url("https://...")
except Normattiva2MDError as e:
    print(f"Errore: {e}")
    # Log, retry, notifica, etc.
```

### 3. Gestione Mista (Eccezioni + None)

```python
from normattiva2md import convert_url, InvalidURLError

try:
    result = convert_url("https://...", article="art999")
except InvalidURLError as e:
    # Errore grave: URL invalido
    print(f"URL non valido: {e}")
    sys.exit(1)

# Errore soft: articolo non trovato
if result is None:
    print("Articolo non trovato nel documento")
else:
    print(result.markdown)
```

### 4. Context Manager (Futuro)

Possibile estensione futura:

```python
from normattiva2md import Converter

with Converter() as conv:
    # Auto-cleanup, error handling
    result = conv.convert_url("https://...")
```

## Messaggi di Errore

### Best Practices

**❌ Male:**
```python
raise InvalidURLError("Errore")
raise InvalidURLError(f"Invalid: {url}")
```

**✅ Bene:**
```python
raise InvalidURLError(
    f"URL non valido: '{url}'. "
    f"Deve essere HTTPS e dominio normattiva.it"
)

raise FileNotFoundError(
    f"File XML non trovato: '{xml_path}'. "
    f"Verifica che il path sia corretto."
)

raise APIKeyError(
    "Exa API key non configurata. "
    "Configura con: export EXA_API_KEY='your-key' "
    "oppure passa exa_api_key='your-key' come parametro. "
    "Registrati su: https://exa.ai"
)
```

### Caratteristiche Messaggi

- **Informativi**: Spiega cosa è andato storto
- **Actionable**: Suggerisce come risolvere
- **Context**: Include valori problematici (quando sicuro)

## Integrazione con Logging

```python
import logging
from normattiva2md.exceptions import ConversionError

logger = logging.getLogger(__name__)

def convert_url(url: str, ...) -> Optional[ConversionResult]:
    try:
        # ... conversione ...
    except Exception as e:
        logger.error(f"Errore conversione URL {url}: {e}")
        raise ConversionError(f"Errore durante conversione: {e}") from e
```

Pattern `raise ... from e` mantiene traceback originale.

## Compatibilità con CLI

Il CLI esistente può continuare a usare il suo error handling:

```python
# cli.py - comportamento attuale mantenuto

def main():
    # ... parsing args ...
    
    # Può opzionalmente usare nuove eccezioni
    try:
        result = convert_url(url)
    except InvalidURLError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)
    except ConversionError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)
    
    # Gestisce None (errori soft) come prima
    if result is None:
        print("❌ Conversione fallita", file=sys.stderr)
        sys.exit(1)
```

## Test

```python
import pytest
from normattiva2md import convert_url, InvalidURLError

def test_invalid_url_raises():
    with pytest.raises(InvalidURLError):
        convert_url("http://bad-domain.com/...")

def test_invalid_url_message():
    with pytest.raises(InvalidURLError, match="HTTPS"):
        convert_url("http://www.normattiva.it/...")

def test_article_not_found_returns_none():
    # Questo NON solleva eccezione
    result = convert_url("https://...", article="art999")
    assert result is None
```

## Documentazione Utente

### README Section

```markdown
## Gestione Errori

normattiva2md usa una strategia ibrida per gli errori:

### Errori Gravi → Eccezioni

```python
from normattiva2md import convert_url, InvalidURLError

try:
    result = convert_url("https://...")
except InvalidURLError as e:
    print(f"URL non valido: {e}")
```

### Errori Soft → None

```python
# Articolo non trovato non solleva eccezione
result = convert_url("https://...", article="art999")
if result is None:
    print("Articolo non trovato")
```

### Cattura Tutti gli Errori

```python
from normattiva2md import Normattiva2MDError

try:
    result = convert_url("https://...")
except Normattiva2MDError as e:
    print(f"Errore: {e}")
```
```

## Estensioni Future

Possibili nuove eccezioni:

```python
class NetworkError(Normattiva2MDError):
    """Errore connessione durante download"""

class RateLimitError(Normattiva2MDError):
    """Rate limit raggiunto (Exa API o normattiva.it)"""

class ValidationError(Normattiva2MDError):
    """Validazione parametri fallita"""
```
