# 📝 Specifica API Completa

## Funzioni Standalone

### `convert_url()`

**Firma:**
```python
def convert_url(
    url: str,
    article: Optional[str] = None,
    with_urls: bool = False,
    with_references: bool = False,
    output_dir: Optional[str] = None,
    quiet: bool = False,
) -> Optional[ConversionResult]:
    """
    Converte documento da URL normattiva.it a Markdown.
    
    Args:
        url: URL normattiva.it del documento
        article: Articolo specifico da estrarre (es: "art16bis")
        with_urls: Genera link markdown per riferimenti
        with_references: Scarica anche documenti citati
        output_dir: Directory output (solo con with_references)
        quiet: Disabilita logging info
    
    Returns:
        ConversionResult con markdown e metadata, oppure None se conversione fallisce
    
    Raises:
        InvalidURLError: URL non valido o dominio non permesso
        ConversionError: Errore grave durante conversione
    
    Examples:
        >>> result = convert_url("https://www.normattiva.it/uri-res/N2Ls?urn:...")
        >>> print(result.markdown[:100])
        >>> print(result.metadata['dataGU'])
        
        >>> # Con articolo specifico
        >>> result = convert_url("https://...", article="art16bis")
        
        >>> # Con link inline
        >>> result = convert_url("https://...", with_urls=True)
    """
```

**Comportamento:**
- Valida URL → solleva `InvalidURLError` se invalido
- Carica `.env` automaticamente
- Scarica XML da normattiva.it
- Converte a Markdown
- Estrae metadata
- Ritorna `ConversionResult` o `None`

**Errori:**
- **Eccezione**: URL invalido, dominio non permesso, errore parsing XML
- **None**: Download fallito (network), articolo non trovato

---

### `convert_xml()`

**Firma:**
```python
def convert_xml(
    xml_path: str,
    article: Optional[str] = None,
    with_urls: bool = False,
    metadata: Optional[Dict] = None,
    quiet: bool = False,
) -> Optional[ConversionResult]:
    """
    Converte file XML locale a Markdown.
    
    Args:
        xml_path: Path al file XML Akoma Ntoso
        article: Articolo specifico da estrarre
        with_urls: Genera link markdown per riferimenti
        metadata: Metadata opzionali da includere nel front matter
        quiet: Disabilita logging info
    
    Returns:
        ConversionResult con markdown e metadata, oppure None se conversione fallisce
    
    Raises:
        FileNotFoundError: File XML non esiste
        ConversionError: Errore parsing XML
    
    Examples:
        >>> result = convert_xml("path/to/file.xml")
        >>> result.save("output.md")
        
        >>> # Con metadata custom
        >>> result = convert_xml(
        ...     "file.xml",
        ...     metadata={'source': 'custom', 'dataGU': '20220101'}
        ... )
    """
```

**Comportamento:**
- Verifica esistenza file → solleva `FileNotFoundError` se non esiste
- Parse XML → solleva `ConversionError` se parsing fallisce
- Converte a Markdown
- Estrae metadata da XML o usa metadata forniti
- Ritorna `ConversionResult` o `None`

**Errori:**
- **Eccezione**: File non esiste, XML malformato, parsing fallito
- **None**: Articolo non trovato (se specificato)

---

### `search_law()`

**Firma:**
```python
def search_law(
    query: str,
    exa_api_key: Optional[str] = None,
    limit: int = 5,
    quiet: bool = False,
) -> List[SearchResult]:
    """
    Cerca documenti legali usando Exa AI.
    
    Args:
        query: Query di ricerca in linguaggio naturale
        exa_api_key: Exa API key (default: usa EXA_API_KEY da ENV)
        limit: Numero massimo risultati
        quiet: Disabilita logging info
    
    Returns:
        Lista di SearchResult ordinata per relevance, lista vuota se nessun risultato
    
    Raises:
        APIKeyError: API key non configurata o invalida
    
    Examples:
        >>> results = search_law("legge stanca accessibilità")
        >>> if results:
        ...     best = results[0]
        ...     print(f"{best.title}: {best.url}")
        
        >>> # Con API key custom
        >>> results = search_law("decreto dignità", exa_api_key="custom-key")
        
        >>> # Loop su risultati
        >>> for r in results:
        ...     print(f"{r.score:.2f} - {r.title}")
    """
```

**Comportamento:**
- Legge API key da parametro o ENV (`EXA_API_KEY`)
- Solleva `APIKeyError` se API key non disponibile
- Chiama Exa API con filtro dominio `normattiva.it`
- Ordina risultati per relevance
- Ritorna lista di `SearchResult`
- Ritorna lista vuota se nessun risultato

**Errori:**
- **Eccezione**: API key mancante, API key invalida
- **Lista vuota**: Nessun risultato trovato, network error (con warning log)

---

## Classe `Converter`

**Firma:**
```python
class Converter:
    """
    Converter con configurazione persistente.
    
    Utile per batch processing o uso ripetuto con stessa configurazione.
    
    Attributes:
        exa_api_key: Exa API key configurata
        quiet: Flag quiet mode
        keep_xml: Flag per mantenere XML scaricati
    
    Examples:
        >>> conv = Converter(exa_api_key="...", quiet=True)
        >>> result1 = conv.convert_url("https://...")
        >>> result2 = conv.convert_url("https://...")
        >>> results = conv.search("legge stanca")
    """
    
    def __init__(
        self,
        exa_api_key: Optional[str] = None,
        quiet: bool = False,
        keep_xml: bool = False,
    ):
        """
        Inizializza converter con configurazione.
        
        Args:
            exa_api_key: Exa API key (default: usa EXA_API_KEY da ENV)
            quiet: Disabilita tutti i log info
            keep_xml: Mantiene file XML scaricati temporanei
        """
```

### Metodi

#### `convert_url()`
```python
def convert_url(
    self,
    url: str,
    article: Optional[str] = None,
    with_urls: bool = False,
    with_references: bool = False,
    output_dir: Optional[str] = None,
) -> Optional[ConversionResult]:
    """
    Converte da URL usando configurazione dell'istanza.
    
    Stesso comportamento di convert_url() standalone ma usa:
    - self.quiet per logging
    - self.keep_xml per file temporanei
    """
```

#### `convert_xml()`
```python
def convert_xml(
    self,
    xml_path: str,
    article: Optional[str] = None,
    with_urls: bool = False,
    metadata: Optional[Dict] = None,
) -> Optional[ConversionResult]:
    """
    Converte da XML usando configurazione dell'istanza.
    
    Stesso comportamento di convert_xml() standalone ma usa:
    - self.quiet per logging
    """
```

#### `search()`
```python
def search(
    self,
    query: str,
    limit: int = 5,
) -> List[SearchResult]:
    """
    Ricerca documenti usando configurazione dell'istanza.
    
    Usa:
    - self.exa_api_key se configurata
    - self.quiet per logging
    """
```

#### `search_and_convert()`
```python
def search_and_convert(
    self,
    query: str,
    article: Optional[str] = None,
    with_urls: bool = False,
    use_best: bool = True,
) -> Optional[ConversionResult]:
    """
    Cerca e converte il miglior risultato in un passo.
    
    Args:
        query: Query di ricerca
        article: Articolo specifico da estrarre
        with_urls: Genera link markdown
        use_best: Se True usa miglior risultato, altrimenti chiede interattivo
    
    Returns:
        ConversionResult del miglior match, oppure None se ricerca fallisce
    
    Raises:
        APIKeyError: API key non configurata
    
    Examples:
        >>> conv = Converter(exa_api_key="...")
        >>> result = conv.search_and_convert("legge stanca")
        >>> result.save("legge_stanca.md")
    """
```

---

## Oggetti Ritornati

### `ConversionResult`

```python
@dataclass
class ConversionResult:
    """Risultato conversione documento."""
    
    markdown: str
    """Contenuto Markdown del documento convertito"""
    
    metadata: Dict[str, str]
    """
    Metadata estratti:
    - dataGU: Data pubblicazione Gazzetta Ufficiale
    - codiceRedaz: Codice redazionale
    - dataVigenza: Data vigenza
    - url: URL originale (se da URL)
    - url_xml: URL del file XML
    - article: Articolo estratto (se specificato)
    - url_permanente: URL permanente (se presente in XML)
    """
    
    url: Optional[str] = None
    """URL normattiva.it originale (se conversione da URL)"""
    
    url_xml: Optional[str] = None
    """URL del file XML Akoma Ntoso"""
    
    def __str__(self) -> str:
        """Ritorna markdown come stringa."""
        return self.markdown
    
    def save(self, path: str) -> None:
        """
        Salva markdown su file.
        
        Args:
            path: Path file output
        
        Raises:
            IOError: Errore scrittura file
        
        Examples:
            >>> result = convert_url("https://...")
            >>> result.save("output.md")
        """
```

**Uso:**
```python
result = convert_url("https://...")

# Accesso markdown
print(result.markdown[:100])

# Accesso metadata
print(result.metadata['dataGU'])
print(result.metadata['codiceRedaz'])

# Conversione automatica a stringa
print(str(result))
with open("output.md", "w") as f:
    f.write(str(result))

# Metodo helper
result.save("output.md")

# Usabile in f-string
print(f"Documento:\n{result}")
```

---

### `SearchResult`

```python
@dataclass
class SearchResult:
    """Singolo risultato di ricerca."""
    
    url: str
    """URL normattiva.it del documento"""
    
    title: str
    """Titolo del documento"""
    
    score: float
    """Score di relevance (0.0 - 1.0)"""
```

**Uso:**
```python
results = search_law("legge stanca")

if results:
    # Miglior risultato
    best = results[0]
    print(f"Titolo: {best.title}")
    print(f"URL: {best.url}")
    print(f"Score: {best.score:.2f}")
    
    # Loop su tutti
    for r in results:
        print(f"{r.score:.2f} - {r.title}")
        
    # Converti il migliore
    result = convert_url(results[0].url)
```

---

## Eccezioni

### Gerarchia

```
Exception
└── Normattiva2MDError (base)
    ├── InvalidURLError
    ├── FileNotFoundError
    ├── APIKeyError
    └── ConversionError
```

### Dettagli

```python
class Normattiva2MDError(Exception):
    """Eccezione base per tutti gli errori del package."""

class InvalidURLError(Normattiva2MDError):
    """URL non valido o dominio non permesso."""

class FileNotFoundError(Normattiva2MDError):
    """File XML non trovato."""

class APIKeyError(Normattiva2MDError):
    """Exa API key mancante o invalida."""

class ConversionError(Normattiva2MDError):
    """Errore durante conversione XML → Markdown."""
```

### Gestione

```python
from normattiva2md import (
    convert_url,
    InvalidURLError,
    ConversionError,
)

try:
    result = convert_url("https://invalid-domain.com/...")
except InvalidURLError as e:
    print(f"URL non valido: {e}")
except ConversionError as e:
    print(f"Errore conversione: {e}")
```

---

## Type Hints

Tutte le funzioni includono type hints completi:

```python
from __future__ import annotations  # Python 3.7+ compatibility

from typing import Optional, Dict, List

def convert_url(
    url: str,
    article: Optional[str] = None,
    with_urls: bool = False,
    with_references: bool = False,
    output_dir: Optional[str] = None,
    quiet: bool = False,
) -> Optional[ConversionResult]:
    ...
```

Questo permette:
- Autocompletamento IDE
- Type checking con `mypy`
- Migliore documentazione
- Compatibilità Python 3.7+
