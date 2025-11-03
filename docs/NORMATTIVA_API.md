# API di Normattiva.it

Questo documento descrive le API disponibili su normattiva.it per la ricerca di documenti legali.

## Stato delle API pubbliche

**Normattiva.it NON ha API JSON pubbliche documentate** per la ricerca di documenti.

## API di ricerca (HTML-based)

### Endpoint ricerca veloce

**URL**: `POST https://www.normattiva.it/ricerca/veloce/0`

**Tipo**: `application/x-www-form-urlencoded`

**Parametri**:

- `testoRicerca`: La query di ricerca (es. "decreto dignità", "legge stanca")
- `tabID`: Un identificatore univoco (può essere un timestamp o numero casuale)
- `title`: Deve essere `lbl.risultatoRicerca`

**Esempio di richiesta**:

```bash
curl -X POST 'https://www.normattiva.it/ricerca/veloce/0' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'tabID=0.123456789&title=lbl.risultatoRicerca&testoRicerca=decreto+dignità'
```

**Risposta**:

- Status: `302 Found` (redirect)
- Location: `https://www.normattiva.it/ricerca/veloce/0?tabID=...&title=lbl.risultatoRicerca&initBreadCrumb=true`
- La risposta finale è una pagina HTML con i risultati della ricerca

### Formato dei risultati

I risultati sono presentati come pagina HTML con:

- Numero totale di atti trovati (es. "Sono stati trovati 88.795 atti.")
- Lista di risultati paginati (default 20 per pagina)
- Per ogni risultato:
  - Tipo e numero dell'atto (es. "DECRETO-LEGGE 12 Luglio 2018, n. 87")
  - Descrizione breve tra parentesi quadre
  - Data e numero Gazzetta Ufficiale
  - Link al dettaglio dell'atto

**Esempio HTML risultato**:

```html
<a href="/uri-res/N2Ls?urn:nir:stato:decreto.legge:2018-07-12;87">
  DECRETO-LEGGE 12 Luglio 2018, n. 87
</a>
[Disposizioni urgenti per la dignità dei lavoratori e delle imprese.]
(GU n. 161 del 13-07-2018)
```

## Limitazioni

- **Nessuna API JSON**: I risultati sono solo in formato HTML
- **Parsing richiesto**: Per estrarre dati strutturati serve parsing dell'HTML
- **Nessuna documentazione**: Le API non sono documentate ufficialmente
- **Fragilità**: Cambiamenti alla struttura HTML romperebbero il parsing

## Soluzione attuale in akoma2md

Il progetto akoma2md usa **Gemini CLI** come intermediario intelligente per:

1. Interpretare query in linguaggio naturale
2. Cercare su normattiva.it
3. Estrarre l'URL corretto del documento

### Vantaggi dell'approccio Gemini CLI

- ✅ **Comprensione naturale**: "decreto dignità" → trova automaticamente il D.L. 87/2018
- ✅ **Robusto**: Non dipende dalla struttura HTML
- ✅ **Flessibile**: Gestisce sinonimi e varianti del nome
- ✅ **Aggiornato**: Gemini può trovare anche documenti nuovi

### Implementazione

```python
def lookup_normattiva_url(search_query):
    """
    Usa Gemini CLI per cercare l'URL normattiva.it.
    """
    prompt = f"""Cerca su normattiva.it l'URL della "{search_query}" e restituisci solo l'URL completo che inizia con https://www.normattiva.it/"""

    result = subprocess.run(
        ['gemini', '--output-format', 'json'],
        input=prompt,
        capture_output=True,
        text=True,
        timeout=60
    )

    # Estrae URL dalla risposta JSON
    json_response = json.loads(result.stdout.strip())
    response_text = json_response.get('response', '').strip()

    # Cerca pattern URL normattiva.it
    url_pattern = r'https://www\.normattiva\.it/[^\s]+'
    match = re.search(url_pattern, response_text)

    return match.group(0) if match else None
```

### Requisiti

- [Gemini CLI](https://github.com/google-gemini/gemini-cli) installato: `npm install -g @google/gemini-cli`
- API key Google AI configurata

## Alternative future

Se normattiva.it pubblicasse API JSON ufficiali, si potrebbero implementare:

1. **Ricerca diretta**:
   ```
   GET /api/v1/search?q=decreto+dignità&format=json
   ```

2. **Metadati strutturati**:
   ```json
   {
     "total": 88795,
     "results": [
       {
         "type": "decreto-legge",
         "date": "2018-07-12",
         "number": 87,
         "title": "Disposizioni urgenti per la dignità dei lavoratori",
         "url": "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legge:2018-07-12;87"
       }
     ]
   }
   ```

3. **Autocomplete**:
   ```
   GET /api/v1/suggest?q=decreto+dig&limit=10
   ```

## Risorse

- Sito: https://www.normattiva.it
- Progetto akoma2md: https://github.com/aborruso/normattiva_2_md
- Gemini CLI: https://github.com/google-gemini/gemini-cli

## Aggiornamenti

**Data analisi**: 2025-11-03

**Metodo**: Analisi con Chrome DevTools MCP delle richieste di rete durante ricerca manuale

**Conclusione**: Al momento della scrittura, normattiva.it non offre API JSON pubbliche. L'uso di Gemini CLI è l'approccio più robusto e flessibile per la ricerca in linguaggio naturale.
