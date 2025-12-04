# 📦 Models - Dataclasses

File: `src/normattiva2md/models.py`

## Implementazione Completa

```python
"""
Data models per API normattiva2md.

Definisce le strutture dati ritornate dalle funzioni API.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Dict
import sys


@dataclass
class ConversionResult:
    """
    Risultato di una conversione XML → Markdown.
    
    Contiene sia il contenuto Markdown che i metadata estratti dal documento.
    Può essere usato direttamente come stringa o salvato su file.
    
    Attributes:
        markdown: Contenuto Markdown completo del documento
        metadata: Dictionary con metadata (dataGU, codiceRedaz, etc.)
        url: URL normattiva.it originale (se conversione da URL)
        url_xml: URL del file XML Akoma Ntoso scaricato
    
    Examples:
        >>> result = convert_url("https://...")
        >>> print(result.markdown[:100])
        >>> print(result.metadata['dataGU'])
        >>> result.save("output.md")
        >>> 
        >>> # Conversione automatica a stringa
        >>> with open("out.md", "w") as f:
        ...     f.write(str(result))
    """
    
    markdown: str
    metadata: Dict[str, str]
    url: Optional[str] = None
    url_xml: Optional[str] = None
    
    def __str__(self) -> str:
        """
        Converte automaticamente a stringa = markdown.
        
        Permette di usare ConversionResult direttamente in contesti
        che si aspettano una stringa (print, f-string, file.write).
        
        Returns:
            Contenuto markdown completo
        """
        return self.markdown
    
    def save(self, path: str, encoding: str = 'utf-8') -> None:
        """
        Salva contenuto markdown su file.
        
        Args:
            path: Path del file di output
            encoding: Encoding del file (default: utf-8)
        
        Raises:
            IOError: Se errore durante scrittura file
        
        Examples:
            >>> result = convert_url("https://...")
            >>> result.save("legge.md")
            >>> result.save("/path/to/output.md", encoding="utf-8")
        """
        try:
            with open(path, 'w', encoding=encoding) as f:
                f.write(self.markdown)
        except IOError as e:
            print(f"❌ Errore durante salvataggio file: {e}", file=sys.stderr)
            raise
    
    @property
    def title(self) -> Optional[str]:
        """
        Estrae titolo dal markdown (prima riga H1 se presente).
        
        Returns:
            Titolo del documento o None se non trovato
        
        Examples:
            >>> result = convert_url("https://...")
            >>> print(result.title)
            "Legge 9 gennaio 2004, n. 4"
        """
        for line in self.markdown.split('\n'):
            if line.startswith('# '):
                return line[2:].strip()
        return None
    
    @property
    def data_gu(self) -> Optional[str]:
        """Shortcut per metadata['dataGU']."""
        return self.metadata.get('dataGU')
    
    @property
    def codice_redaz(self) -> Optional[str]:
        """Shortcut per metadata['codiceRedaz']."""
        return self.metadata.get('codiceRedaz')
    
    @property
    def data_vigenza(self) -> Optional[str]:
        """Shortcut per metadata['dataVigenza']."""
        return self.metadata.get('dataVigenza')


@dataclass
class SearchResult:
    """
    Singolo risultato di ricerca da Exa AI.
    
    Rappresenta un documento trovato durante la ricerca in linguaggio naturale.
    
    Attributes:
        url: URL normattiva.it del documento
        title: Titolo del documento
        score: Score di relevance (0.0 - 1.0, più alto = più rilevante)
    
    Examples:
        >>> results = search_law("legge stanca")
        >>> best = results[0]
        >>> print(f"{best.title} - Score: {best.score:.2f}")
        >>> print(f"URL: {best.url}")
    """
    
    url: str
    title: str
    score: float
    
    def __str__(self) -> str:
        """
        Rappresentazione stringa leggibile del risultato.
        
        Returns:
            Stringa formattata con titolo e score
        
        Examples:
            >>> result = SearchResult(url="...", title="Legge 4/2004", score=0.95)
            >>> print(result)
            "[0.95] Legge 4/2004"
        """
        return f"[{self.score:.2f}] {self.title}"
    
    def __repr__(self) -> str:
        """Rappresentazione tecnica del risultato."""
        return f"SearchResult(url={self.url!r}, title={self.title!r}, score={self.score})"


# Type aliases per chiarezza
Metadata = Dict[str, str]
SearchResults = list[SearchResult]  # Python 3.9+
# Per Python 3.7-3.8 compatibilità:
# from typing import List
# SearchResults = List[SearchResult]
```

## Note Implementazione

### 1. Dataclasses
Uso `@dataclass` per:
- Generazione automatica `__init__`, `__repr__`, `__eq__`
- Codice più conciso
- Type hints integrati
- Compatibilità Python 3.7+

### 2. Type Hints con Future Annotations
```python
from __future__ import annotations
```
Permette type hints moderni anche su Python 3.7-3.8.

### 3. Metodi Helper

#### `ConversionResult.save()`
Metodo comodo per salvare su file senza dover riscrivere logica.

#### `ConversionResult.title`
Property per accesso veloce al titolo estratto.

#### `ConversionResult.data_gu`, etc.
Properties per accesso veloce a metadata comuni.

### 4. String Conversion

`__str__()` ritorna markdown diretto per uso comodo:
```python
result = convert_url("https://...")

# Questi sono equivalenti
print(result.markdown)
print(str(result))
print(result)  # chiama __str__()

# Funziona anche in file.write()
with open("out.md", "w") as f:
    f.write(str(result))
```

### 5. SearchResult Representation

Due rappresentazioni:
- `__str__()`: User-friendly `"[0.95] Legge 4/2004"`
- `__repr__()`: Debug `"SearchResult(url='...', title='...', score=0.95)"`

## Test Examples

```python
# Test ConversionResult
result = ConversionResult(
    markdown="# Test\n\nContent",
    metadata={'dataGU': '20220101', 'codiceRedaz': 'TEST'},
    url="https://www.normattiva.it/...",
    url_xml="https://www.normattiva.it/do/atto/caricaAKN?..."
)

assert str(result) == "# Test\n\nContent"
assert result.title == "Test"
assert result.data_gu == "20220101"
assert result.codice_redaz == "TEST"

# Test SearchResult
search_result = SearchResult(
    url="https://www.normattiva.it/...",
    title="Legge 4/2004",
    score=0.95
)

assert str(search_result) == "[0.95] Legge 4/2004"
assert search_result.url.startswith("https://")
```

## Compatibilità

### Python 3.7-3.8
```python
from __future__ import annotations
from typing import List, Dict, Optional

# Usa typing.List invece di list[]
SearchResults = List[SearchResult]
```

### Python 3.9+
```python
# Può usare built-in types
SearchResults = list[SearchResult]
Metadata = dict[str, str]
```

## Estensibilità Futura

### Possibili Aggiunte

```python
@dataclass
class ConversionResult:
    # ... campi esistenti ...
    
    # Futuri campi opzionali
    references: Optional[List[str]] = None
    """Lista URL documenti citati (se with_references=True)"""
    
    warnings: Optional[List[str]] = None
    """Warning durante conversione"""
    
    statistics: Optional[Dict[str, int]] = None
    """Statistiche documento (num articoli, num commi, etc.)"""
```

Aggiungendo campi con default `None` mantiene compatibilità backward.
