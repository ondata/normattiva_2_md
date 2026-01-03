# Analisi Fattibilità: Elenco Atti Correlati

## Obiettivo

Aggiungere un'opzione CLI per ottenere l'elenco degli atti correlati a una norma.

## API Identificata

### Endpoint

```
GET https://www.normattiva.it/do/atto/vediAttiCorrelati
```

### Parametri richiesti

- `atto.dataPubblicazioneGazzetta`: data pubblicazione GU (formato: YYYY-MM-DD)
- `atto.codiceRedazionale`: codice redazionale (es: 088G0458)
- `currentSearch`: sempre "ricerca_avanzata_aggiornamenti"

### Esempio chiamata

```bash
curl "https://www.normattiva.it/do/atto/vediAttiCorrelati?atto.dataPubblicazioneGazzetta=1988-09-12&atto.codiceRedazionale=088G0458&currentSearch=ricerca_avanzata_aggiornamenti"
```

## Formato risposta

L'API restituisce HTML con una tabella strutturata:

```html
<table id="rigaItem" summary="Aggiornamenti all'atto" class="tabella_elencoAgg">
  <thead>
    <tr>
      <th>Progr.</th>
      <th>data pubblicazione</th>
      <th>atti correlati</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td>22/09/1989</td>
      <td>
        <a href="/atto/caricaDettaglioAtto?atto.dataPubblicazioneGazzetta=1989-09-22&atto.codiceRedazionale=089G0398">
          DECRETO LEGISLATIVO 6 settembre 1989, n. 322
          (in G.U. 22/09/1989, n.222)
        </a>
        Norme sul Sistema statistico nazionale...
      </td>
    </tr>
    <!-- altri atti... -->
  </tbody>
</table>
```

## Informazioni estratte per ogni atto correlato

1. **Numero progressivo**: posizione nell'elenco
2. **Data pubblicazione**: data GU (formato: DD/MM/YYYY)
3. **Tipo atto**: DECRETO LEGISLATIVO, LEGGE, DECRETO DEL PRESIDENTE, ecc.
4. **Data e numero**: es. "6 settembre 1989, n. 322"
5. **Riferimento GU**: es. "G.U. 22/09/1989, n.222"
6. **Descrizione**: testo descrittivo dell'atto
7. **URL dettaglio**: link per accedere all'atto correlato
   - Contiene `atto.dataPubblicazioneGazzetta` e `atto.codiceRedazionale`

## Integrazione nel progetto esistente

### Parametri già disponibili

Il progetto **già estrae** i parametri necessari in `normattiva_api.py:extract_params_from_normattiva_url()`:

```python
# Linee 147-160
params = {}
match_gu = re.search(r'name="atto\.dataPubblicazioneGazzetta"[^>]*value="([^"]+)"', html)
if match_gu:
    # Formato già YYYY-MM-DD (perfetto per l'API atti correlati!)
    params["dataGU"] = match_gu.group(1).replace("-", "")  # YYYYMMDD per download XML

match_codice = re.search(r'name="atto\.codiceRedazionale"[^>]*value="([^"]+)"', html)
if match_codice:
    params["codiceRedaz"] = match_codice.group(1)
```

**NOTA**: L'API `vediAttiCorrelati` richiede la data nel formato `YYYY-MM-DD`, mentre la funzione attuale converte in `YYYYMMDD` per il download XML. Servirà mantenere entrambi i formati.

### Moduli da creare/modificare

1. **Nuova funzione in `normattiva_api.py`**:
   ```python
   def fetch_related_acts(params, session=None, quiet=False):
       """
       Recupera elenco atti correlati

       Args:
           params: dict con dataPubblicazioneGazzetta (YYYY-MM-DD) e codiceRedazionale
           session: sessione requests (opzionale)
           quiet: se True, stampa solo errori

       Returns:
           list: elenco dizionari con informazioni atti correlati
       """
   ```

2. **Nuova opzione CLI in `cli.py`**:
   ```python
   parser.add_argument(
       '--related-acts', '--atti-correlati',
       action='store_true',
       help='Mostra elenco atti correlati (solo se input è URL)'
   )
   ```

3. **Output formati supportati**:
   - **JSON**: lista strutturata di oggetti
   - **Markdown**: tabella o lista puntata
   - **Plain text**: lista semplice per pipe

### Esempio output JSON

```json
[
  {
    "numero_progressivo": 1,
    "data_pubblicazione": "22/09/1989",
    "tipo_atto": "DECRETO LEGISLATIVO",
    "data_atto": "6 settembre 1989",
    "numero_atto": "322",
    "riferimento_gu": "G.U. 22/09/1989, n.222",
    "titolo": "Norme sul Sistema statistico nazionale...",
    "url_dettaglio": "/atto/caricaDettaglioAtto?atto.dataPubblicazioneGazzetta=1989-09-22&atto.codiceRedazionale=089G0398",
    "url_normattiva": "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:1989-09-06;322",
    "parametri": {
      "dataPubblicazioneGazzetta": "1989-09-22",
      "codiceRedazionale": "089G0398"
    }
  }
]
```

### Esempio output Markdown

```markdown
# Atti correlati a LEGGE 23 agosto 1988, n. 400

## 1. DECRETO LEGISLATIVO 6 settembre 1989, n. 322

**Pubblicazione**: 22/09/1989 (G.U. n.222)

Norme sul Sistema statistico nazionale e sulla riorganizzazione dell'Istituto nazionale di statistica...

**URL**: [Visualizza su Normattiva](https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:1989-09-06;322)

---

## 2. DECRETO LEGISLATIVO 16 dicembre 1989, n. 418

...
```

## Parsing HTML

Libreria suggerita: **BeautifulSoup4** o **lxml**

```python
from bs4 import BeautifulSoup

def parse_related_acts_html(html_content):
    """
    Estrae atti correlati dalla risposta HTML

    Args:
        html_content: HTML restituito dall'API

    Returns:
        list: atti correlati come dizionari
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table', {'id': 'rigaItem'})

    # Controllo: nessuna tabella = nessun atto correlato
    if not table:
        return []

    tbody = table.find('tbody')
    # Controllo: tbody vuoto = nessun atto correlato
    if not tbody:
        return []

    acts = []
    for row in tbody.find_all('tr'):
        cells = row.find_all('td')

        # Estrai dati...
        prog = cells[0].get_text(strip=True)
        data = cells[1].get_text(strip=True)

        # Link e informazioni atto
        link = cells[2].find('a')
        # ...

        acts.append({...})

    return acts
```

## Dipendenze aggiuntive

- `beautifulsoup4`: parsing HTML
- `lxml`: parser veloce (opzionale, ma raccomandato)

Aggiornare `setup.py`:

```python
install_requires=[
    "requests>=2.25.0",
    "python-dotenv>=0.19.0",
    "beautifulsoup4>=4.9.0",
    "lxml>=4.6.0",  # opzionale ma raccomandato
]
```

## Gestione Atti Correlati Assenti

È fondamentale prevedere la possibilità che una norma non abbia atti correlati.

### Comportamento API

L'endpoint `vediAttiCorrelati` può restituire:

1. **Tabella con dati**: lista atti correlati
2. **Tabella vuota**: `<tbody>` senza `<tr>`
3. **Tabella inesistente**: nessun elemento con `id="rigaItem"`
4. **HTML di errore**: pagina di errore generica

### Implementazione Sugerita

```python
def fetch_related_acts(params, session=None, quiet=False):
    """
    Recupera elenco atti correlati con gestione caso vuoto

    Returns:
        list: elenco atti correlati (vuoto se non presenti)
        None: errore API
    """
    url = "https://www.normattiva.it/do/atto/vediAttiCorrelati"
    payload = {
        "atto.dataPubblicazioneGazzetta": params["dataPubblicazioneGazzetta"],
        "atto.codiceRedazionale": params["codiceRedazionale"],
        "currentSearch": "ricerca_avanzata_aggiornamenti"
    }

    try:
        response = (session or requests).get(url, params=payload, timeout=30)
        response.raise_for_status()

        acts = parse_related_acts_html(response.text)

        if not acts:
            if not quiet:
                print("ℹ️  Nessun atto correlato trovato per questa norma")

        return acts

    except requests.RequestException as e:
        if not quiet:
            print(f"❌ Errore recupero atti correlati: {e}")
        return None
```

### Messaggi Utente

**Caso atti correlati presenti:**
```
✅ Trovati 3 atti correlati:
  1. DECRETO LEGISLATIVO 6 settembre 1989, n. 322
  2. DECRETO LEGISLATIVO 16 dicembre 1989, n. 418
  3. LEGGE 15 marzo 1997, n. 59
```

**Caso nessun atto correlato:**
```
ℹ️  Nessun atto correlato trovato per questa norma
```

**Caso errore API:**
```
⚠️  Impossibile recuperare atti correlati: errore HTTP 500
```

### CLI Flag Opzionale

```bash
# Mostra atti correlati se presenti, ignora se assenti (nessun errore)
normattiva2md "URL" output.md --related-acts

# Fail se atti correlati non trovati (per script automatizzati)
normattiva2md "URL" output.md --related-acts --fail-if-no-related

# Silenzioso (nessun output se assenti)
normattiva2md "URL" output.md --related-acts --quiet
```

## Esempi Concreti

### Caso 1: Legge con atti correlati

**Norma**: `urn:nir:stato:legge:1988-08-23;400` (Legge 23/1988)

```bash
$ normattiva2md --related-acts "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:1988-08-23;400"

✅ Trovati 3 atti correlati:
  1. DECRETO LEGISLATIVO 6 settembre 1989, n. 322
  2. DECRETO LEGISLATIVO 16 dicembre 1989, n. 418
  3. LEGGE 15 marzo 1997, n. 59

💾 Salvati in: atti_correlati.json
```

### Caso 2: Legge senza atti correlati

**Norma**: `urn:nir:stato:legge:2022-05-05;53` (Legge 53/2022)

```bash
$ normattiva2md --related-acts "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2022-05-05;53"

ℹ️  Nessun atto correlato trovato per questa norma

💾 File atti_correlati.json vuoto creato
```

### Caso 3: Output JSON con lista vuota

```json
{
  "url_originale": "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2022-05-05;53",
  "numero_atti_correlati": 0,
  "atti_correlati": []
}
```

## Casi d'uso CLI

```bash
# 1. Mostra atti correlati come JSON
normattiva2md --related-acts "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:1988-08-23;400" --format json

# 2. Mostra atti correlati come Markdown
normattiva2md --related-acts "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:1988-08-23;400" --format markdown

# 3. Converti norma + salva atti correlati separatamente
normattiva2md "URL" output.md --related-acts --related-acts-output atti_correlati.json

# 4. Solo atti correlati, senza convertire la norma
normattiva2md --related-acts-only "URL" > atti_correlati.json
```

## Vantaggi

1. ✅ **API esistente e funzionante**: già usata dal sito web
2. ✅ **Parametri già disponibili**: estratti dalla pagina HTML
3. ✅ **Nessuna autenticazione**: API pubblica
4. ✅ **Struttura ben definita**: tabella HTML facilmente parsabile
5. ✅ **Integrazione semplice**: riusa infrastruttura esistente (session, headers, timeout)

## Limitazioni

1. ⚠️ **Formato HTML**: richiede parsing (non JSON nativo)
2. ⚠️ **Dipendenza aggiuntiva**: BeautifulSoup4
3. ⚠️ **Funziona solo da URL**: non da file XML locale (parametri non disponibili nell'XML)
4. ⚠️ **Non tutte le norme hanno atti correlati**:
   - Esempio con atti correlati: `urn:nir:stato:legge:1988-08-23;400` (Legge 23/1988)
   - Esempio senza atti correlati: `urn:nir:stato:legge:2022-05-05;53` (Legge 53/2022)
   - Bisogna gestire il caso di risposta vuota o tabella inesistente

## Stima implementazione

- **Complessità**: BASSA
- **Tempo stimato**: 2-3 ore
- **Modifiche necessarie**:
  - [ ] Aggiungere `beautifulsoup4` a `setup.py`
  - [ ] Creare funzione `fetch_related_acts()` in `normattiva_api.py`
  - [ ] Creare funzione `parse_related_acts_html()` per parsing
  - [ ] **Aggiungere controllo lista vuota** e tabella inesistente
  - [ ] Aggiungere opzioni CLI in `cli.py`
  - [ ] Aggiungere formattatori output (JSON, Markdown, plain text)
  - [ ] Test con norme **con e senza** atti correlati:
    - [ ] `urn:nir:stato:legge:1988-08-23;400` (con atti correlati)
    - [ ] `urn:nir:stato:legge:2022-05-05;53` (senza atti correlati)
  - [ ] Documentazione README

## Conclusione

✅ **FATTIBILE** - L'implementazione è semplice e ben integrata con l'architettura esistente.

L'API è pubblica, i parametri sono già estratti, e la struttura HTML è facilmente parsabile. L'unica dipendenza aggiuntiva è BeautifulSoup4, già ampiamente usata e mantenuta.

## Prossimi passi

1. Conferma con il maintainer se la feature è desiderata
2. Decidere formati output preferiti (JSON, Markdown, CSV?)
3. Implementare funzione base
4. Aggiungere test
5. Documentare nel README
