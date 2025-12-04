# 💡 Esempi Codice Completi

## Quick Reference

```python
# Import base
from normattiva2md import convert_url, convert_xml, search_law, Converter

# Conversione veloce
result = convert_url("https://www.normattiva.it/uri-res/N2Ls?urn:...")
print(result.markdown)

# Ricerca
results = search_law("legge stanca")
if results:
    print(f"Trovato: {results[0].title}")

# Uso avanzato
conv = Converter(exa_api_key="...", quiet=True)
result = conv.search_and_convert("decreto dignità")
result.save("decreto.md")
```

---

## Esempio 1: Conversione Base da URL

```python
"""
Esempio: Conversione semplice da URL normattiva.it
"""

from normattiva2md import convert_url

# URL della legge
url = "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2004-01-09;4"

# Converti
result = convert_url(url)

if result:
    # Mostra inizio markdown
    print("=== Markdown Preview ===")
    print(result.markdown[:500])
    print("...")
    
    # Mostra metadata
    print("\n=== Metadata ===")
    print(f"Data GU: {result.data_gu}")
    print(f"Codice Redazionale: {result.codice_redaz}")
    print(f"Data Vigenza: {result.data_vigenza}")
    print(f"Titolo: {result.title}")
    
    # Salva su file
    result.save("legge_stanca.md")
    print("\n✅ Salvato in legge_stanca.md")
else:
    print("❌ Conversione fallita")
```

**Output:**
```
=== Markdown Preview ===
---
url: https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2004-01-09;4
url_xml: https://www.normattiva.it/do/atto/caricaAKN?dataGU=20040117&codiceRedaz=004G0015&dataVigenza=20250130
dataGU: 20040117
codiceRedaz: 004G0015
dataVigenza: 20250130
---

# Legge 9 gennaio 2004, n. 4

Disposizioni per favorire l'accesso dei soggetti disabili agli strumenti informatici.
...

=== Metadata ===
Data GU: 20040117
Codice Redazionale: 004G0015
Data Vigenza: 20250130
Titolo: Legge 9 gennaio 2004, n. 4

✅ Salvato in legge_stanca.md
```

---

## Esempio 2: Conversione da File XML Locale

```python
"""
Esempio: Conversione da file XML locale
"""

from normattiva2md import convert_xml, FileNotFoundError

xml_file = "path/to/document.xml"

try:
    result = convert_xml(xml_file)
    
    if result:
        print(f"Titolo: {result.title}")
        print(f"Lunghezza: {len(result.markdown)} caratteri")
        
        # Salva
        result.save("output.md")
        print("✅ Conversione completata")
    else:
        print("⚠️ Conversione completata ma senza risultato")

except FileNotFoundError as e:
    print(f"❌ File non trovato: {e}")
except Exception as e:
    print(f"❌ Errore: {e}")
```

---

## Esempio 3: Ricerca in Linguaggio Naturale

```python
"""
Esempio: Ricerca documenti con linguaggio naturale
"""

from normattiva2md import search_law, APIKeyError
import os

# Configura API key (se non in .env)
os.environ['EXA_API_KEY'] = 'your-api-key-here'

try:
    # Ricerca
    results = search_law("legge stanca accessibilità")
    
    if results:
        print(f"Trovati {len(results)} risultati:\n")
        
        # Mostra tutti i risultati
        for i, r in enumerate(results, 1):
            print(f"{i}. [{r.score:.2f}] {r.title}")
            print(f"   URL: {r.url}\n")
        
        # Usa il migliore
        best = results[0]
        print(f"\n✅ Miglior match: {best.title}")
        
    else:
        print("❌ Nessun risultato trovato")

except APIKeyError as e:
    print(f"❌ API key non configurata: {e}")
    print("Configura con: export EXA_API_KEY='your-key'")
```

**Output:**
```
Trovati 5 risultati:

1. [0.95] Legge 9 gennaio 2004, n. 4
   URL: https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2004-01-09;4

2. [0.87] Decreto Legislativo 10 agosto 2018, n. 106
   URL: https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2018-08-10;106

...

✅ Miglior match: Legge 9 gennaio 2004, n. 4
```

---

## Esempio 4: Ricerca + Conversione (Pipeline)

```python
"""
Esempio: Ricerca e converti in un passo
"""

from normattiva2md import Converter

# Inizializza converter
conv = Converter(
    exa_api_key="your-key",  # o usa ENV
    quiet=True
)

# Ricerca e converti il migliore
result = conv.search_and_convert("decreto dignità")

if result:
    print(f"Trovato e convertito: {result.title}")
    result.save("decreto_dignita.md")
    print(f"Salvato: {len(result.markdown)} caratteri")
else:
    print("Nessun risultato trovato")
```

---

## Esempio 5: Batch Processing

```python
"""
Esempio: Converti multipli documenti in batch
"""

from normattiva2md import Converter

# Lista URL da convertire
urls = [
    "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2004-01-09;4",
    "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2005-03-07;82",
    "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2022;53",
]

# Converter con configurazione
conv = Converter(quiet=True, keep_xml=False)

# Converti tutti
results = []
for i, url in enumerate(urls, 1):
    print(f"[{i}/{len(urls)}] Conversione {url}...")
    
    result = conv.convert_url(url)
    
    if result:
        filename = f"legge_{i:02d}_{result.codice_redaz}.md"
        result.save(filename)
        results.append((filename, result))
        print(f"  ✅ Salvato: {filename}")
    else:
        print(f"  ❌ Fallito")

# Report finale
print(f"\n{'='*60}")
print(f"Completati: {len(results)}/{len(urls)}")
for filename, result in results:
    print(f"  - {filename}: {result.title}")
```

**Output:**
```
[1/3] Conversione https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2004-01-09;4...
  ✅ Salvato: legge_01_004G0015.md
[2/3] Conversione https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2005-03-07;82...
  ✅ Salvato: legge_02_005G0104.md
[3/3] Conversione https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2022;53...
  ✅ Salvato: legge_03_22G00061.md

============================================================
Completati: 3/3
  - legge_01_004G0015.md: Legge 9 gennaio 2004, n. 4
  - legge_02_005G0104.md: Codice dell'amministrazione digitale
  - legge_03_22G00061.md: Legge 5 agosto 2022, n. 118
```

---

## Esempio 6: Gestione Errori Completa

```python
"""
Esempio: Gestione robusta degli errori
"""

from normattiva2md import (
    convert_url,
    InvalidURLError,
    ConversionError,
    Normattiva2MDError,
)
import logging

# Configura logging
logging.basicConfig(level=logging.INFO)

def safe_convert(url: str, output_file: str) -> bool:
    """
    Converti URL con gestione errori completa.
    
    Returns:
        True se successo, False altrimenti
    """
    try:
        # Tenta conversione
        result = convert_url(url)
        
        # Check errori soft
        if result is None:
            logging.warning(f"Conversione fallita (errore soft): {url}")
            return False
        
        # Salva
        result.save(output_file)
        logging.info(f"✅ Successo: {output_file}")
        return True
        
    except InvalidURLError as e:
        logging.error(f"❌ URL non valido: {e}")
        return False
        
    except ConversionError as e:
        logging.error(f"❌ Errore conversione: {e}")
        return False
        
    except Normattiva2MDError as e:
        # Cattura altri errori del package
        logging.error(f"❌ Errore normattiva2md: {e}")
        return False
        
    except Exception as e:
        # Errore inatteso
        logging.error(f"❌ Errore inatteso: {e}")
        return False

# Uso
urls_to_try = [
    ("https://www.normattiva.it/uri-res/N2Ls?urn:...", "legge1.md"),
    ("http://bad-domain.com/...", "legge2.md"),  # URL invalido
    ("https://www.normattiva.it/invalid", "legge3.md"),  # Conversione fallita
]

for url, output in urls_to_try:
    success = safe_convert(url, output)
    print(f"{url[:50]}... → {'✅' if success else '❌'}")
```

---

## Esempio 7: Articolo Specifico

```python
"""
Esempio: Estrai solo articolo specifico
"""

from normattiva2md import convert_url

# URL base della legge
url = "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2004-01-09;4"

# Estrai solo articolo 3
result = convert_url(url, article="art3")

if result:
    print(f"Estratto: {result.metadata.get('article', 'N/A')}")
    print(f"Titolo documento: {result.title}")
    print("\n=== Contenuto Articolo ===")
    print(result.markdown)
    
    result.save("art3.md")
else:
    print("❌ Articolo non trovato")
```

---

## Esempio 8: Con Link Inline ai Riferimenti

```python
"""
Esempio: Genera link markdown per riferimenti normativi
"""

from normattiva2md import convert_url

url = "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2005-03-07;82"

# Converti con link inline
result = convert_url(url, with_urls=True)

if result:
    print("Markdown con link ai riferimenti normativi:")
    print(result.markdown[:1000])
    
    # Conta link (approssimativo)
    num_links = result.markdown.count("](https://www.normattiva.it/")
    print(f"\nLink generati: circa {num_links}")
    
    result.save("cad_con_link.md")
```

---

## Esempio 9: Context Manager (Future Pattern)

```python
"""
Esempio: Pattern per futuro context manager
(non ancora implementato, ma struttura preparata)
"""

# FUTURO - Non funziona ancora
# from normattiva2md import Converter
# 
# with Converter(quiet=True) as conv:
#     result = conv.convert_url("https://...")
#     result.save("output.md")
# # Auto-cleanup temp files

# ATTUALE - Equivalente manuale
from normattiva2md import Converter

conv = Converter(quiet=True, keep_xml=False)
try:
    result = conv.convert_url("https://...")
    if result:
        result.save("output.md")
finally:
    # Cleanup se necessario
    pass
```

---

## Esempio 10: Notebook Jupyter

```python
# In Jupyter notebook

# Installazione
# !pip install normattiva2md

# Import
from normattiva2md import convert_url, search_law, Converter
import os

# Configura (opzionale se già in .env)
os.environ['EXA_API_KEY'] = 'your-key'

# Ricerca interattiva
query = input("Cerca documento: ")
results = search_law(query)

if results:
    # Mostra risultati
    for i, r in enumerate(results):
        print(f"{i}: {r.title}")
    
    # Seleziona
    idx = int(input("Seleziona (numero): "))
    
    # Converti
    result = convert_url(results[idx].url)
    
    # Display in notebook
    from IPython.display import Markdown, display
    display(Markdown(result.markdown))
    
    # Salva
    result.save("selected_law.md")
else:
    print("Nessun risultato")
```

---

## Esempio 11: Async-Ready Structure (Preparazione)

```python
"""
Esempio: Struttura codice preparata per future versioni async
(attuale implementazione sincrona)
"""

from normattiva2md import convert_url

# ATTUALE: Sincrono
def batch_convert_sync(urls):
    """Converti multipli URL in sequenza"""
    results = []
    for url in urls:
        result = convert_url(url)
        results.append(result)
    return results

# FUTURO: Quando disponibile async version
# async def batch_convert_async(urls):
#     """Converti multipli URL in parallelo"""
#     import asyncio
#     from normattiva2md import convert_url_async
#     
#     tasks = [convert_url_async(url) for url in urls]
#     results = await asyncio.gather(*tasks)
#     return results

# Uso attuale
urls = ["url1", "url2", "url3"]
results = batch_convert_sync(urls)
print(f"Convertiti: {len([r for r in results if r])}/{len(urls)}")
```

---

## Pattern Comuni

### 1. Check Prima di Usare

```python
result = convert_url(url)

if result:
    # Usa result
    print(result.markdown)
else:
    # Handle None
    print("Conversione fallita")
```

### 2. Metadata Access

```python
result = convert_url(url)

# Via properties
print(result.data_gu)
print(result.codice_redaz)

# Via dict
print(result.metadata['dataGU'])
print(result.metadata.get('article', 'N/A'))
```

### 3. String Conversion

```python
result = convert_url(url)

# Tutte equivalenti per salvare markdown
with open("out.md", "w") as f:
    f.write(result.markdown)
    f.write(str(result))
    f.write(f"{result}")

# O usa helper
result.save("out.md")
```

### 4. Error Handling Pattern

```python
from normattiva2md import convert_url, InvalidURLError

try:
    result = convert_url(url)
except InvalidURLError:
    # Errore grave: URL invalido
    raise
    
# Errore soft: conversione fallita
if result is None:
    # Log e continua
    logging.warning("Conversione fallita")
    return
```

---

## Tips & Tricks

### Logging Control

```python
import logging

# Disabilita info logging
logging.getLogger('normattiva2md').setLevel(logging.WARNING)

# Oppure usa quiet parameter
result = convert_url(url, quiet=True)
```

### Reusabilità Config

```python
# Invece di ripetere parametri
for url in urls:
    result = convert_url(url, quiet=True, with_urls=True)

# Usa Converter
conv = Converter(quiet=True)
for url in urls:
    result = conv.convert_url(url, with_urls=True)
```

### Check Metadata Availability

```python
result = convert_url(url)

# Alcuni metadata potrebbero mancare
data_gu = result.metadata.get('dataGU')
if data_gu:
    print(f"Data GU: {data_gu}")
else:
    print("Data GU non disponibile")
```
