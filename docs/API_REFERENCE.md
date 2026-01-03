# API Reference per Developer

Documentazione completa dell'API di `normattiva2md` per uso come libreria Python.

## Indice

- [Installazione](#installazione)
- [Funzioni esportate](#funzioni-esportate)
- [Classi](#classi)
- [Eccezioni](#eccezioni)
- [Esempi completi](#esempi-completi)

## Installazione

```bash
pip install normattiva2md
```

## Funzioni esportate

### `convert_url(url, article=None, with_urls=False, quiet=False)`

Converte un documento da URL normattiva.it in Markdown.

**Parametri:**

- `url` (str): URL completo di normattiva.it
- `article` (str, opzionale): Numero articolo da estrarre (es: `"3"`, `"16bis"`)
- `with_urls` (bool, default: False): Genera link markdown ai riferimenti normativi
- `quiet` (bool, default: False): Disabilita logging su stderr

**Ritorna:** `ConversionResult` o `None` se articolo non trovato

**Esempio:**

```python
from normattiva2md import convert_url

result = convert_url(
    "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2004-01-09;4",
    article="3",
    quiet=True
)

if result:
    print(result.markdown)
    result.save("articolo.md")
```

---

### `convert_xml(xml_path, article=None, with_urls=False, quiet=False)`

Converte un file XML Akoma Ntoso locale in Markdown.

**Parametri:**

- `xml_path` (str): Percorso file XML
- `article` (str, opzionale): Numero articolo da estrarre
- `with_urls` (bool, default: False): Genera link markdown ai riferimenti
- `quiet` (bool, default: False): Disabilita logging

**Ritorna:** `ConversionResult` o `None` se articolo non trovato

**Esempio:**

```python
from normattiva2md import convert_xml

result = convert_xml("documento.xml", article="4")
result.save("output.md")
```

---

### `search_law(query, exa_api_key=None, num_results=5)`

Ricerca leggi in linguaggio naturale usando Exa AI.

**Parametri:**

- `query` (str): Query in linguaggio naturale
- `exa_api_key` (str, opzionale): API key Exa AI (default: da env var)
- `num_results` (int, default: 5): Numero risultati da restituire

**Ritorna:** Lista di `SearchResult`

**Esempio:**

```python
from normattiva2md import search_law

results = search_law("legge stanca accessibilità")
for r in results:
    print(f"[{r.score:.2f}] {r.title}")
    print(f"  URL: {r.url}")
```

---

## Classi

### `Converter`

Classe per uso avanzato con configurazione persistente.

**Metodi:**

```python
conv = Converter(exa_api_key=None, quiet=False)
```

- `exa_api_key` (str, opzionale): API key Exa AI
- `quiet` (bool, default: False): Disabilita logging

#### `convert_url(url, article=None, with_urls=False)`

Converte da URL normattiva.it.

#### `convert_xml(xml_path, article=None, with_urls=False)`

Converte da file XML locale.

#### `search_law(query, num_results=5)`

Ricerca leggi in linguaggio naturale.

#### `search_and_convert(query, num_results=1)`

Ricerca e converte automaticamente il miglior risultato.

**Esempio:**

```python
from normattiva2md import Converter

conv = Converter(quiet=True)

# Ricerca e conversione
result = conv.search_and_convert("decreto dignità")
result.save("decreto.md")

# Batch processing
urls = [
    "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2004-01-09;4",
    "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2005-03-07;82",
]

for url in urls:
    result = conv.convert_url(url)
    if result:
        print(f"Convertito: {result.title}")
```

---

### `ConversionResult`

Oggetto contenente il risultato della conversione.

**Attributi:**

```python
result.markdown      # str: Contenuto markdown completo
result.metadata      # dict: Metadati YAML completi
result.url           # str: URL documento
result.url_xml       # str: URL XML
result.title         # str: Titolo documento
result.data_gu       # str: Data Gazzetta Ufficiale (YYYYMMDD)
result.codice_redaz  # str: Codice redazionale
result.data_vigenza  # str: Data vigenza (YYYYMMDD)
```

**Metodi:**

```python
result.save(filepath)  # Salva markdown su file
```

**Esempio:**

```python
result = convert_url("https://www.normattiva.it/...")
print(result.markdown[:500])
print(result.title)
result.save("legge.md")
```

---

### `SearchResult`

Oggetto contenente il risultato della ricerca.

**Attributi:**

```python
result.url    # str: URL normattiva.it
result.title  # str: Titolo documento
result.score  # float: Punteggio preferenza (maggiore = migliore)
```

---

## Eccezioni

### `Normattiva2MDError`

Eccezione base per tutti gli errori del package.

### `InvalidURLError`

Errore per URL non validi o dominio non permesso.

**Esempio:**

```python
try:
    result = convert_url("https://example.com/not-normattiva")
except InvalidURLError as e:
    print(f"URL non valido: {e}")
```

### `XMLFileNotFoundError`

Errore per file XML non trovato.

### `ConversionError`

Errore durante conversione XML→Markdown.

### `APIKeyError`

Errore per API key Exa AI mancante o non valida.

**Esempio:**

```python
from normattiva2md import (
    convert_url,
    InvalidURLError,
    ConversionError,
    APIKeyError,
    Normattiva2MDError,
)

try:
    result = convert_url("https://www.normattiva.it/...")
except InvalidURLError as e:
    print(f"URL non valido: {e}")
except ConversionError as e:
    print(f"Errore conversione: {e}")
except APIKeyError as e:
    print(f"API key mancante: {e}")
except Normattiva2MDError as e:
    print(f"Errore generico: {e}")
```

---

## Esempi completi

### Estrazione singolo articolo

```python
from normattiva2md import convert_url

url = "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2004-01-09;4"

# Articolo semplice
result = convert_url(url, article="3")
print(result.markdown)

# Articolo con estensione
result = convert_url(url, article="16bis")
print(result.markdown)

# Articolo non trovato (ritorna None)
result = convert_url(url, article="999")
if result is None:
    print("Articolo non trovato")
```

### Link automatici ai riferimenti

```python
from normattiva2md import convert_url

result = convert_url(url, with_urls=True)

# Il markdown contiene link come:
# [D.Lgs. 27 maggio 2022, n. 82](https://www.normattiva.it/...)
print(result.markdown)
```

### Batch processing con pandas

```python
from normattiva2md import convert_url
import pandas as pd

urls = [
    "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2004-01-09;4",
    "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2005-03-07;82",
]

data = []
for url in urls:
    result = convert_url(url, quiet=True)
    if result:
        data.append({
            "titolo": result.title,
            "data_gu": result.data_gu,
            "codice_redaz": result.codice_redaz,
            "lunghezza": len(result.markdown),
        })

df = pd.DataFrame(data)
print(df)
```

### Ricerca con Exa AI

```python
from normattiva2md import search_law, Converter

# Funzione semplice
results = search_law("legge stanca accessibilità")
for r in results[:3]:
    print(f"[{r.score:.2f}] {r.title}")

# Ricerca e conversione automatica
conv = Converter()
result = conv.search_and_convert("decreto dignità")
if result:
    result.save("decreto.md")
```

### Gestione errori robusta

```python
from normattiva2md import (
    convert_url,
    InvalidURLError,
    ConversionError,
    APIKeyError,
)

def safe_convert(url, article=None):
    try:
        result = convert_url(url, article=article, quiet=True)
        if result is None:
            print(f"Articolo {article} non trovato")
            return None
        return result
    except InvalidURLError as e:
        print(f"URL non valido: {e}")
    except ConversionError as e:
        print(f"Errore conversione: {e}")
    except APIKeyError as e:
        print(f"API key mancante: {e}")
    return None

result = safe_convert("https://www.normattiva.it/...", article="3")
if result:
    result.save("articolo.md")
```

---

## Come scoprire metodi

In un ambiente Python interattivo:

```python
# 1. help() per documentazione completa
from normattiva2md import Converter
help(Converter)

# 2. dir() per lista metodi e attributi
print(dir(Converter))

# 3. introspezione
print(Converter.__doc__)
```

---

## Altre risorse

- **Quickstart interattivo**: [examples/quickstart.ipynb](../examples/quickstart.ipynb)
- **README principale**: [README.md](../README.md)
- **Guida URL**: [URL_NORMATTIVA.md](URL_NORMATTIVA.md)
