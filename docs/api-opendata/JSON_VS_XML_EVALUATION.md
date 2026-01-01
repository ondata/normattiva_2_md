# Valutazione Formati: XML AKN vs JSON vs HTML API

**Data**: 2026-01-01 (aggiornato con test API OpenData)
**Contesto**: Analisi comparativa tra formati disponibili da API OpenData e endpoint legacy

---

## Executive Summary

Le API OpenData di Normattiva forniscono **4 formati utilizzabili**:

1. **XML Akoma Ntoso (AKN)** - Standard legale XML
2. **JSON** - Struttura equivalente ad AKN
3. **HTML strutturato** - Via API `/atto/dettaglio-atto` ✅ **NOVITÀ TESTATA**
4. **XML NormeInRete** - Formato legacy

### Scoperta Chiave

✅ **API `/atto/dettaglio-atto` funzionante**: Ritorna HTML ben strutturato con classi semantiche Akoma Ntoso, facilmente convertibile in Markdown.

**Test completati**:
- ✅ Endpoint dettaglio atto: 200 OK
- ✅ HTML → Markdown converter: funzionante
- ✅ Output equivalente a XML AKN → Markdown

---

## Confronto Formati

### 1. XML Akoma Ntoso (AKN)

**Pro**:
- ✅ **Standard internazionale** (OASIS LegalDocML)
- ✅ Stesso formato processato da normattiva2md v2.x
- ✅ **Codice converter esistente e testato**
- ✅ Supporta tutte le feature (articoli, modifiche, riferimenti)
- ✅ Namespace semantico: `http://docs.oasis-open.org/legaldocml/ns/akn/3.0`

**Contro**:
- ⚠️ Parsing XML richiede gestione namespace
- ⚠️ File più grandi (~10-50 KB per atto)

**Disponibilità**:
- ✅ **Endpoint diretto** `caricaAKN` (approccio attuale)
- ✅ Collezioni preconfezionate (ZIP)
- ✅ Collezioni asincrone (ZIP dopo workflow)

**Esempio struttura**:
```xml
<akomaNtoso xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
  <act>
    <meta>...</meta>
    <body>
      <article eId="art_1">
        <num>1</num>
        <heading>Obiettivi e finalita</heading>
        <paragraph eId="art_1-par_1">
          <num>1.</num>
          <content>
            <p>La Repubblica riconosce...</p>
          </content>
        </paragraph>
      </article>
    </body>
  </act>
</akomaNtoso>
```

---

### 2. JSON

**Pro**:
- ✅ **Parsing nativo Python** (json.load)
- ✅ **Struttura equivalente ad AKN**
- ✅ **Metadata arricchiti** (URN, ELI, storia versioni)
- ✅ File più compatti (~8-30 KB per atto)
- ✅ Facile da debuggare

**Contro**:
- ❌ Richiede nuovo converter JSON→Markdown
- ⚠️ Non standard internazionale come AKN
- ❌ **Non disponibile via endpoint singolo** (solo collezioni ZIP)

**Disponibilità**:
- ❌ **NO endpoint diretto singolo atto**
- ✅ Collezioni preconfezionate (ZIP)
- ✅ Collezioni asincrone (ZIP dopo workflow)

**Struttura JSON** (testata con `output/sample_atto_json.json`):
```json
{
  "metadati": {
    "urn": "urn:nir:ministero.agricoltura.e.foreste:decreto:1988-04-12;164",
    "eli": "eli/id/1988/05/23/088G0223/ORIGINAL",
    "tipoDoc": "DECRETO",
    "numDoc": "164",
    "dataDoc": "1988-04-12",
    "dataPubblicazione": "1988-05-23"
  },
  "articolato": {
    "elementi": [
      {
        "nomeNir": "articolo",
        "numNir": "1",
        "rubricaNir": "Titolo articolo",
        "testo": "Testo completo...",
        "noteArt": "Note...",
        "elementi": []  // Sotto-elementi ricorsivi
      }
    ]
  }
}
```

**Converter POC**: ✅ Testato in `scripts/json_to_markdown_poc.py` - conversione perfetta

---

### 3. HTML Strutturato (API OpenData) ✅ **NOVITÀ**

**Pro**:
- ✅ **Endpoint diretto funzionante** `/atto/dettaglio-atto`
- ✅ **1 richiesta HTTP** (equivalente a caricaAKN)
- ✅ **HTML ben strutturato** con classi semantiche CSS
- ✅ **Classi naming Akoma Ntoso** (article-num-akn, comma-num-akn, etc.)
- ✅ **Parsing semplice** (BeautifulSoup o regex)
- ✅ **Metadata arricchiti** (date vigenza, tipo provvedimento, etc.)
- ✅ **API ufficialmente documentate**

**Contro**:
- ⚠️ HTML non è standard come XML AKN
- ⚠️ Richiede nuovo converter HTML→Markdown
- ⚠️ Stabilità da verificare (API nuove)

**Disponibilità**:
- ✅ **Endpoint diretto** `POST /api/v1/atto/dettaglio-atto`
- ✅ Nessuna autenticazione
- ✅ Nessuna email richiesta
- ✅ Response immediata

**Struttura HTML** (da `output/dettaglio_response.json`):
```json
{
  "data": {
    "atto": {
      "titolo": "LEGGE 9 gennaio 2004, n. 4",
      "articoloHtml": "<div class=\"bodyTesto\">
        <h2 class=\"article-num-akn\" id=\"art_1\">Art. 1</h2>
        <div class=\"article-pre-comma-text-akn\">(Obiettivi)</div>
        <div class=\"art-comma-div-akn\">
          <span class=\"comma-num-akn\">1. </span>
          <span class=\"art_text_in_comma\">Testo comma...</span>
        </div>
        <div class=\"ins-akn\">((Modifica legislativa))</div>
      </div>",
      "tipoProvvedimentoDescrizione": "LEGGE",
      "annoProvvedimento": 2004,
      "numeroProvvedimento": 4,
      "articoloDataInizioVigenza": "20200717"
    }
  }
}
```

**Classi CSS per parsing**:
- `article-num-akn`: Numero articolo
- `article-pre-comma-text-akn`: Rubrica
- `comma-num-akn`: Numero comma
- `art_text_in_comma`: Testo comma
- `ins-akn` / `del-akn`: Modifiche legislative
- `preamble-*-akn`: Preambolo

**Converter POC**: ✅ Testato in `scripts/api_html_to_markdown.py` - conversione perfetta

---

### 4. Approccio Attuale (caricaAKN + XML AKN)

**Pro**:
- ✅ **1 richiesta HTTP** per XML AKN
- ✅ **Input user-friendly** (URL permalink)
- ✅ **Nessuna autenticazione**
- ✅ **Codice esistente e testato** da anni
- ✅ **Download immediato** (no ZIP, no email, no polling)
- ✅ **XML Akoma Ntoso** (standard internazionale)

**Contro**:
- ⚠️ **HTML scraping** per estrarre parametri da URL
- ⚠️ Fragile se struttura HTML cambia (mitigato: stabile da anni)
- ⚠️ **Endpoint non documentato** ufficialmente

**Flusso**:
```
URL → HTML scraping → Estrai parametri → GET caricaAKN → XML AKN → Markdown
```

---

## Workflow API OpenData

### Opzione A: Endpoint Diretto HTML (TESTATO ✅)

**Use case**: Singolo atto con parametri noti

**Flusso**:
```
URL → Parsing parametri → API dettaglio-atto → HTML strutturato → Markdown
```

**Step**:
1. Estrai `dataGU` e `codiceRedazionale` da URL (parsing query string o regex)
2. `POST /api/v1/atto/dettaglio-atto` con parametri
3. Parsing HTML → Markdown

**Pro**:
- ✅ **1 richiesta HTTP**
- ✅ **Nessun HTML scraping della pagina web**
- ✅ **API ufficialmente documentate**
- ✅ **Metadata arricchiti**

**Contro**:
- ⚠️ Richiede parsing URL per estrarre parametri (come approccio attuale)
- ⚠️ Stabilità da verificare

**Test**: ✅ Completato - vedi `scripts/test_dettaglio.sh` e `scripts/api_html_to_markdown.py`

---

### Opzione A-bis: Ricerca + Dettaglio (TESTATO ✅) **RACCOMANDATO**

**Use case**: Singolo atto senza parsing URL

**Flusso**:
```
Ricerca API → dataGU + codiceRedaz → API dettaglio-atto → HTML strutturato → Markdown
```

**Step**:
1. `POST /api/v1/ricerca/semplice` con testo/tipo/anno/numero
2. Estrai `dataGU` e `codiceRedazionale` dalla response
3. `POST /api/v1/atto/dettaglio-atto` con parametri
4. Parsing HTML → Markdown

**Pro**:
- ✅ **2 richieste HTTP** (accettabile)
- ✅ **NESSUN parsing URL/HTML necessario**
- ✅ **100% API ufficiali**
- ✅ **Ricerca flessibile** (testo, filtri, ordinamento)
- ✅ **Input user-friendly** (tipo, numero, anno)

**Parametri ricerca**:
```json
{
  "testoRicerca": "legge 4 2004",
  "orderType": "recente",
  "paginazione": {
    "paginaCorrente": 1,
    "numeroElementiPerPagina": 10
  }
}
```

**Response**:
```json
{
  "listaAtti": [{
    "dataGU": "2004-01-17",
    "codiceRedazionale": "004G0015",
    "numeroProvvedimento": "4",
    "annoProvvedimento": "2004"
  }]
}
```

**Test**: ✅ Completato - vedi `scripts/test_workflow_completo_funzionante.py`

---

### Opzione B: Collezioni Preconfezionate

**Use case**: Download collezioni predefinite (costituzione, codici, etc.)

**Flusso**:
```
GET /collections/collection-predefinite → Scegli collezione → GET download → ZIP (AKN/JSON/XML)
```

**Pro**:
- ✅ Nessuna autenticazione
- ✅ Download immediato
- ✅ Formati AKN/JSON/XML disponibili

**Contro**:
- ❌ Solo collezioni predefinite (non singoli atti custom)
- ❌ Download ZIP intero (overhead)

---

### Opzione C: Collezioni Asincrone (Custom)

**Use case**: Batch download (decine/centinaia atti)

**Flusso**:
```
1. POST /ricerca-asincrona/nuova-ricerca → Token (in response)
2. PUT /ricerca-asincrona/conferma-ricerca (usa token)
3. GET /ricerca-asincrona/check-status (polling)
4. GET /download/collection-asincrona → ZIP (AKN/JSON/XML)
```

**Pro**:
- ✅ **Filtri custom** (anno, numero, tipo, testo)
- ✅ Formati AKN/JSON/XML disponibili
- ✅ **Email opzionale** (token in response)
- ✅ **Completamente scriptabile**

**Contro**:
- ❌ Workflow multi-step
- ❌ Latenza elaborazione (minuti/ore)
- ❌ Download ZIP (no singolo file)
- ❌ **Overkill per 1 atto**

**Uso**: Batch (decine/centinaia atti)

---

## Proof of Concept

### POC 1: JSON → Markdown ✅

**Script**: `scripts/json_to_markdown_poc.py`

**Input**: `output/sample_atto_json.json` (DECRETO 12 aprile 1988, n. 164)

**Output**: `sample_atto_from_json.md`

**Risultato**: ✅ **Conversione perfetta** con:
- YAML front matter (metadata)
- Titolo documento
- Articoli numerati
- Note articoli
- Struttura ricorsiva (commi, elenchi)

---

### POC 2: HTML API → Markdown ✅

**Script**: `scripts/api_html_to_markdown.py`

**Input**: `output/dettaglio_response.json` (LEGGE 9 gennaio 2004, n. 4 - Legge Stanca)

**Output**: `legge_stanca_from_api.md`

**Risultato**: ✅ **Conversione perfetta** con:
- YAML front matter (metadata arricchiti)
- Titolo e sottotitolo
- Articoli con rubrica
- Commi numerati
- Modifiche legislative `(( ))`
- HTML entities convertiti (È, à, etc.)

**Confronto con XML AKN converter**: Output **equivalente**

---

## Confronto Approcci Completo

| Aspetto | caricaAKN | API Ricerca+HTML ✨ | API HTML diretto | JSON (ZIP) | XML AKN (ZIP) |
|---------|-----------|-------------------|------------------|------------|---------------|
| **Richieste HTTP** | 1 (GET) | 2 (POST) | 1 (POST) | 3-5 (async) | 3-5 (async) |
| **Parsing URL** | ✅ Necessario | ❌ **Non serve** | ✅ Necessario | ❌ No | ❌ No |
| **Formato source** | XML AKN | HTML | HTML | JSON | XML AKN |
| **Parsing** | XML | HTML | HTML | JSON | XML |
| **Standard** | ✅ AKN 3.0 | HTML AKN | HTML AKN | Custom | ✅ AKN 3.0 |
| **Metadata** | Basic | ✅ Arricchiti | ✅ Arricchiti | ✅ Arricchiti | ✅ Arricchiti |
| **API ufficiali** | ❌ No | ✅ **Sì** | ✅ Sì | ✅ Sì | ✅ Sì |
| **Stabilità** | ✅ Alta | ⚠️ Da testare | ⚠️ Da testare | ⚠️ Da testare | ⚠️ Da testare |
| **Converter** | ✅ Esistente | ✅ Testato | ✅ Testato | ✅ POC | ✅ Esistente |
| **Ricerca flessibile** | ❌ No | ✅ **Sì** | ❌ No | ✅ Sì | ✅ Sì |
| **Singolo atto** | ✅ Ottimo | ✅ **Ottimo** | ✅ Ottimo | ❌ Solo ZIP | ❌ Solo ZIP |
| **Batch** | ❌ No | ⚠️ Loop | ⚠️ Loop | ✅ Sì | ✅ Sì |
| **Latenza** | Immediata | Immediata | Immediata | Minuti/ore | Minuti/ore |

✨ **RACCOMANDATO per v3.0+**: Ricerca + Dettaglio = Nessun parsing URL + API ufficiali

---

## Raccomandazioni

### Per v2.x (Attuale - Produzione)

**✅ MANTENERE approccio attuale** (endpoint `caricaAKN`)

**Motivi**:
1. ✅ **Funziona perfettamente** da anni
2. ✅ XML Akoma Ntoso = **standard internazionale**
3. ✅ **Converter collaudato** e testato
4. ✅ **Performance ottimali** (1 richiesta HTTP)
5. ⚠️ **API nuove** - Stabilità da dimostrare nel tempo

**Nota**: API Ricerca+Dettaglio ora funzionante ma preferire caricaAKN per stabilità produzione

**Rischio accettabile**: HTML scraping URL fragile MA:
- Struttura URL stabile da anni
- Fallback possibile se cambia
- Parsing query string standard

---

### Per v3.0+ (Futuro - Valutazione)

**💡 CONSIDERARE migrazione graduale ad API OpenData**

#### Scenario 1: API Ricerca + Dettaglio (RACCOMANDATO per v3.0)

Se endpoint `/ricerca/semplice` + `/atto/dettaglio-atto` dimostrano stabilità (6-12 mesi):

```python
# Step 1: Ricerca (no parsing URL)
search_result = api_ricerca("legge 4 2004")

# Step 2: Dettaglio
html_data = api_dettaglio_atto(
    search_result['dataGU'],
    search_result['codiceRedazionale']
)

# Step 3: Conversione
markdown = convert_html_to_markdown(html_data)
```

**Vantaggi**:
- ✅ **NESSUN parsing URL** necessario
- ✅ **100% API ufficiali documentate**
- ✅ **Ricerca flessibile** (testo, filtri)
- ✅ **Input user-friendly** (tipo, numero, anno)
- ✅ Metadata arricchiti
- ✅ 2 richieste HTTP (accettabile)

**Quando**: Dopo periodo test stabilità (6-12 mesi)

**Test**: ✅ Già disponibile e funzionante (`scripts/test_workflow_completo_funzionante.py`)

---

#### Scenario 2: Hybrid Mode (Consigliato)

**Migliore dei due mondi**:

```python
# 1. API per metadata arricchiti
metadata = api_get_metadata(dataGU, codiceRedaz)

# 2. caricaAKN per XML AKN (stabile)
xml = download_via_caricaAKN(dataGU, codiceRedaz)

# 3. Converti XML con metadata API
markdown = convert_xml_to_markdown(xml, metadata_extra=metadata)
```

**Vantaggi**:
- ✅ Stabilità XML collaudato
- ✅ Metadata arricchiti da API
- ✅ Resilienza (2 fonti)

---

#### Scenario 3: Dual Mode con Fallback

```python
try:
    # Prova API OpenData
    data = api_dettaglio_atto(params)
    return convert_html(data)
except APIError:
    # Fallback su caricaAKN
    xml = download_caricaAKN(params)
    return convert_xml(xml)
```

**Vantaggi**:
- ✅ Massima resilienza
- ✅ Transizione graduale
- ✅ Zero downtime

---

### Feature Opzionali v2.3.0+

#### 1. Flag `--source-format` (Sperimentale)

```bash
# XML AKN (default)
normattiva2md "URL" output.md

# HTML da API
normattiva2md --source-format html "URL" output.md

# Auto-detect
normattiva2md --source-format auto "URL" output.md
```

**Uso**: Comparazione formati, test API

---

#### 2. Batch Mode con JSON

```bash
normattiva2md --batch-async \
  --tipo LEGGE --anno 2024 \
  --formato JSON \
  -o output/
```

**Workflow**:
1. Ricerca asincrona API → Token
2. Polling status → ZIP JSON
3. Estrazione + conversione automatica tutti atti

**Uso**: Download collezioni (decine/centinaia atti)

---

#### 3. Hybrid Metadata Mode

```bash
normattiva2md --enrich-metadata "URL" output.md
```

**Workflow**:
1. Usa caricaAKN per XML
2. Arricchisci con metadata da API
3. YAML front matter completo

**Uso**: Migliore qualità metadata senza rischi

---

## Conclusioni Finali

### Correzione Analisi Precedente

**❌ ERRATO** (analisi iniziale):
> "API OpenData non offrono endpoint diretto per singolo atto"
> "Serve email obbligatoria e workflow complesso"
> "Non adatte per uso single-document"

**✅ CORRETTO** (dopo test verificati):
- ✅ Endpoint `/ricerca/semplice` **FUNZIONANTE** (errori iniziali corretti)
- ✅ Endpoint `/atto/dettaglio-atto` **funzionante perfettamente**
- ✅ **Workflow completo ricerca→dettaglio→markdown TESTATO**
- ✅ **NESSUN parsing URL necessario** (con ricerca API)
- ✅ **Nessuna email richiesta** per singoli atti
- ✅ HTML → Markdown **testato e funzionante**
- ✅ **100% API ufficiali** disponibile

### Stato Finale

**Per uso singolo atto**:

| Formato | Disponibilità | Parsing URL | Qualità | Raccomandazione |
|---------|---------------|-------------|---------|-----------------|
| **XML AKN (caricaAKN)** | ✅ Endpoint diretto | ✅ Necessario | ✅ Standard | ✅ **Produzione v2.x** |
| **HTML (Ricerca+API)** | ✅ Ricerca + endpoint | ❌ **Non serve** | ✅ Ben strutturato | ⚠️ **v3.0+ RACCOMANDATO** |
| **HTML (API diretta)** | ✅ Endpoint diretto | ✅ Necessario | ✅ Ben strutturato | ⚠️ **v3.0+ alternativa** |
| **JSON** | ❌ Solo ZIP | ❌ N/A | ✅ Ottima struttura | ❌ Non per singoli |
| **XML AKN (ZIP)** | ❌ Solo ZIP | ❌ N/A | ✅ Standard | ❌ Overhead |

**Per uso batch**:

| Formato | Workflow | Raccomandazione |
|---------|----------|-----------------|
| **JSON (ZIP)** | Async API | ✅ **Ottimo** (parsing facile) |
| **XML AKN (ZIP)** | Async API | ✅ Buono (standard) |
| **HTML (API)** | Loop endpoint | ⚠️ Possibile ma inefficiente |

**Formati preferiti** (in ordine):

1. **Per singoli atti**:
   - `XML AKN via caricaAKN` (v2.x, produzione - 1 richiesta)
   - `HTML via Ricerca+API` ✨ (v3.0+ RACCOMANDATO - no parsing URL, 2 richieste)
   - `HTML via API diretta` (v3.0+ alternativa - 1 richiesta, parsing URL)

2. **Per batch**:
   - `JSON via ZIP` (parsing più semplice)
   - `XML AKN via ZIP` (standard)
   - `HTML via loop Ricerca+API` (flessibile ma lento)

---

## Test Files

**POC Converter**:
- ✅ `scripts/json_to_markdown_poc.py` - JSON→MD (funzionante)
- ✅ `scripts/api_html_to_markdown.py` - HTML→MD (funzionante)
- ✅ `scripts/test_workflow_completo_funzionante.py` - **Workflow Ricerca+Dettaglio completo**

**Sample Data**:
- ✅ `output/sample_atto_json.json` - JSON da collezione
- ✅ `output/dettaglio_response.json` - Response API HTML (dettaglio diretto)
- ✅ `output/dettaglio_from_search.json` - Response API HTML (da ricerca)
- ✅ `output/params_from_search.json` - Parametri estratti da ricerca
- ✅ `output/sample_json.zip` - Collezione JSON completa

**Output Test**:
- ✅ `sample_atto_from_json.md` - Markdown da JSON
- ✅ `legge_stanca_from_api.md` - Markdown da HTML API (dettaglio diretto)
- ✅ `atto_from_workflow_completo.md` - **Markdown da workflow Ricerca+Dettaglio**

**Documentazione**:
- ✅ `WORKFLOW_API_FUNZIONANTE.md` - Workflow completo testato
- ✅ `output/openapi-bff-opendata.json` - Specifica OpenAPI

---

**Data documento**: 2026-01-01
**Versione**: 2.0 (aggiornamento con test API HTML)
**Stato**: ✅ Test completati, 3 formati validati
**Conclusione**:
- XML AKN (caricaAKN) rimane ottimale per v2.x
- HTML API promettente per v3.0+ quando stabile
- JSON eccellente per batch workflows
