# Quick Start - Gazzetta Ufficiale API Client

Guida rapida 5 minuti per iniziare subito.

## Setup (30 secondi)

```bash
# Installa dipendenze
pip install requests beautifulsoup4

# Scarica il client
curl -O https://path/to/gazzetta_api_client.py
```

## Prima ricerca (1 minuto)

```python
from gazzetta_api_client import GazzettaUfficialeClient

# Crea client
client = GazzettaUfficialeClient()

# Cerca "ambiente" nel titolo
results = client.search(title="ambiente")

# Mostra risultati
print(f"Trovati: {results['total_results']} atti")

for r in results['results'][:5]:  # Primi 5
    print(f"\n{r['act_type']}: {r['title'][:60]}...")
    print(f"Link: https://www.gazzettaufficiale.it{r['link']}")
```

**Output**:
```
Trovati: 247 atti

DECRETO: Misure urgenti per la tutela dell'ambiente...
Link: https://www.gazzettaufficiale.it/atto/...

LEGGE: Disposizioni in materia di ambiente...
Link: https://www.gazzettaufficiale.it/atto/...
```

## Casi d'uso comuni

### 1. Cercare per tipo atto

```python
# Solo decreti
results = client.search(
    act_type="decreto",
    title="salute"
)
```

### 2. Cercare in un periodo

```python
# Gennaio 2024
results = client.search(
    title="covid",
    pub_start_day="01",
    pub_start_month="01",
    pub_start_year="2024",
    pub_end_day="31",
    pub_end_month="01",
    pub_end_year="2024"
)
```

### 3. Scaricare più pagine

```python
all_results = []

for page in range(3):  # Prime 3 pagine
    r = client.search(title="energia", page=page)
    all_results.extend(r['results'])

print(f"Totale: {len(all_results)} atti")
```

### 4. Salvare in CSV

```python
import csv

results = client.search(title="sostenibilità")

with open('risultati.csv', 'w', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=[
        'act_type', 'act_date', 'title', 'gu_reference'
    ])
    writer.writeheader()
    
    for r in results['results']:
        writer.writerow({
            'act_type': r.get('act_type', ''),
            'act_date': r.get('act_date', ''),
            'title': r.get('title', ''),
            'gu_reference': r.get('gu_reference', '')
        })
```

### 5. Salvare in JSON

```python
import json

results = client.search(title="clima")

with open('risultati.json', 'w', encoding='utf-8') as f:
    json.dump(results['results'], f, ensure_ascii=False, indent=2)
```

## Struttura risultato

Ogni risultato contiene:

```python
{
    "act_type": "DECRETO",               # Tipo atto
    "act_date": "15 gennaio 2024",       # Data (opzionale)
    "gu_reference": "(GU n.17 ...)",     # Riferimento GU
    "link": "/atto/...",                 # Link dettaglio
    "title": "Inserimento del...",       # Titolo completo
    "emettitore": "MINISTERO..."         # Emettitore (opzionale)
}
```

## Parametri principali

| Parametro | Descrizione | Esempio |
|-----------|-------------|---------|
| `title` | Parole nel titolo | `"ambiente"` |
| `text` | Parole nel testo | `"clima"` |
| `act_type` | Tipo provvedimento | `"decreto"` |
| `pub_start_year` | Anno inizio | `"2024"` |
| `pub_end_year` | Anno fine | `"2024"` |
| `page` | Numero pagina (0-based) | `0`, `1`, `2`... |

## Modalità ricerca testo

```python
# AND: TUTTE le parole
results = client.search(
    title="ministero salute",
    title_search_type="ALL_WORDS"  # Default
)

# OR: ALMENO UNA parola
results = client.search(
    title="ministero salute",
    title_search_type="SOME_WORDS"
)

# Frase esatta
results = client.search(
    title="ministero della salute",
    title_search_type="ENTIRE_STRING"
)
```

## Troubleshooting

### Nessun risultato

```python
results = client.search(title="test")

if not results['has_results']:
    print("Nessun risultato trovato")
else:
    print(f"Trovati {results['total_results']} atti")
```

### Gestire errori

```python
from requests.exceptions import RequestException

try:
    results = client.search(title="test")
except RequestException as e:
    print(f"Errore: {e}")
```

### Debug HTML

```python
results = client.search(title="test")

# Salva HTML per debug
with open('debug.html', 'w') as f:
    f.write(results['raw_html'])
```

## Limiti

- **Max 500 risultati** (6 pagine ~100/pagina)
- **No rate limiting**: usa con moderazione
- **Solo Serie Generale**: altre serie non supportate

## Prossimi passi

1. **Tutorial completo**: `python examples_tutorial.py`
2. **Documentazione**: leggi `README.md`
3. **Codice sorgente**: studia `gazzetta_api_client.py`

## Supporto

Per domande o problemi:
1. Leggi `README.md` - Troubleshooting
2. Esegui `python examples_tutorial.py` - Esempio 11
3. Controlla `raw_html` nel risultato per debug

---

**Tempo totale setup + prima ricerca**: ~2 minuti ⚡
