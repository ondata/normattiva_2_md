# Valutazione API OpenData di Normattiva.it

**Data**: 2026-01-01
**Versione progetto**: v2.1.2
**Documentazione ufficiale**: https://dati.normattiva.it/Come-scaricare-i-dati
**Test eseguiti**: ✅ Verificati con curl e Python

---

## Executive Summary

Esiste un portale OpenData ufficiale di Normattiva (`dati.normattiva.it`) con **API REST pubbliche** documentate e **completamente funzionanti** per uso machine-to-machine.

### Scoperta Chiave

Le API OpenData **SONO utilizzabili** per convertire singoli atti normativi in Markdown tramite workflow M2M:

```
URL normattiva.it → Estrai parametri → API dettaglio atto → HTML strutturato → Markdown
```

**Test verificati**:
- ✅ Endpoint `/ricerca/semplice` **FUNZIONANTE** (200 OK)
- ✅ Endpoint `/atto/dettaglio-atto` funzionante (200 OK)
- ✅ Ritorna HTML ben strutturato con classi semantiche Akoma Ntoso
- ✅ Conversione HTML → Markdown testata e funzionante
- ✅ **Workflow completo ricerca→dettaglio→markdown TESTATO**
- ✅ Nessuna autenticazione richiesta
- ✅ Nessuna email richiesta per singoli atti
- ✅ **Nessun parsing URL necessario** con ricerca API

### Conclusione

**Entrambi gli approcci sono validi** per singoli atti:

| Approccio | Pro | Contro |
|-----------|-----|--------|
| **Attuale (caricaAKN)** | XML Akoma Ntoso (standard)<br>Codice collaudato<br>Stabile da anni | Endpoint non documentato |
| **API OpenData** | Ufficialmente documentato<br>HTML ben strutturato<br>Metadata arricchiti | Nuovo (da testare stabilità) |

**Raccomandazione**: Mantenere approccio attuale per v2.x, valutare API per v3.0+ quando dimostrato stabile nel tempo.

---

## Documentazione Ufficiale

**Portale**: https://dati.normattiva.it
**Documentazione API**:
- PDF: https://dati.normattiva.it/assets/come_fare_per/API_Normattiva_OpenData.pdf
- OpenAPI 3.0: https://dati.normattiva.it/assets/come_fare_per/openapi-bff-opendata.json
- Swagger UI: https://dati.normattiva.it/assets/come_fare_per/Normattiva%20OpenData.html

**Base URL**: `https://api.normattiva.it/t/normattiva.api/bff-opendata/v1`

**Autenticazione**: ❌ Nessuna (API pubbliche)

---

## Endpoint Testati

### ✅ 1. Dettaglio Atto (FUNZIONANTE)

**Endpoint**: `POST /api/v1/atto/dettaglio-atto`

**Request**:
```json
{
  "dataGU": "2004-01-17",
  "codiceRedazionale": "004G0015",
  "formatoRichiesta": "V"
}
```

**Parametri**:
- `dataGU`: Data pubblicazione Gazzetta Ufficiale (formato `YYYY-MM-DD`)
- `codiceRedazionale`: Codice atto (es. `004G0015`)
- `formatoRichiesta`: `V` (Vigente), `O` (Originale), `M` (Multivigente)

**Test eseguito** (`scripts/test_dettaglio.sh`):
```bash
curl -X POST 'https://api.normattiva.it/t/normattiva.api/bff-opendata/v1/api/v1/atto/dettaglio-atto' \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json' \
  -d '{"dataGU":"2004-01-17","codiceRedazionale":"004G0015","formatoRichiesta":"V"}'
```

**Risultato**: ✅ **200 OK** - Response completa in `output/dettaglio_response.json`

**Response**:
```json
{
  "success": true,
  "data": {
    "atto": {
      "titolo": "LEGGE 9 gennaio 2004, n. 4",
      "sottoTitolo": "<em><strong>((Disposizioni per favorire...))</strong></em>",
      "articoloHtml": "<div class=\"bodyTesto\">...</div>",
      "tipoProvvedimentoDescrizione": "LEGGE",
      "tipoProvvedimentoCodice": "PLE",
      "annoProvvedimento": 2004,
      "numeroProvvedimento": 4,
      "dataGU": "2004-01-17",
      "articoloDataInizioVigenza": "20200717",
      "articoloDataFineVigenza": "99999999"
    }
  }
}
```

#### Struttura HTML Ritornato

Il campo `articoloHtml` contiene HTML **ben strutturato** con classi semantiche:

```html
<div class="bodyTesto">
  <h2 class="preamble-title-akn">La Camera dei deputati...</h2>

  <h2 class="article-num-akn" id="art_1">Art. 1</h2>
  <div class="article-pre-comma-text-akn">
    (Obiettivi e finalita)
  </div>

  <div class="art-commi-div-akn">
    <div class="art-comma-div-akn">
      <span class="comma-num-akn">1. </span>
      <span class="art_text_in_comma">
        La Repubblica riconosce e tutela...
      </span>
    </div>

    <div class="art-comma-div-akn">
      <span class="comma-num-akn">2. </span>
      <span class="art_text_in_comma">
        È tutelato...
        <div class="ins-akn" eId="ins_1">
          ((, nonchè alle strutture...))
        </div>
      </span>
    </div>
  </div>
</div>
```

**Classi CSS utilizzabili per parsing**:
- `article-num-akn`: Numero articolo
- `article-pre-comma-text-akn`: Rubrica (titolo) articolo
- `comma-num-akn`: Numero comma
- `art_text_in_comma`: Testo comma
- `ins-akn`: Modifiche legislative (da wrappare in `(( ))`)
- `del-akn`: Parti abrogate
- `preamble-*-akn`: Preambolo

---

### ✅ 2. Conversione HTML → Markdown (TESTATA)

**Script**: `scripts/api_html_to_markdown.py`

**Input**: Response JSON da API dettaglio atto
**Output**: Markdown ben formattato

**Test eseguito**:
```bash
python3 scripts/api_html_to_markdown.py
```

**Output** (`legge_stanca_from_api.md`):
```markdown
---
tipo: LEGGE
numero: 4
anno: 2004
dataGU: 2004-01-17
---

# LEGGE 9 gennaio 2004, n. 4

**((Disposizioni per favorire e semplificare l'accesso degli utenti...))**

## Art. 1

**(Obiettivi e finalita)**

1. La Repubblica riconosce e tutela il diritto di ogni persona ad accedere a tutte le fonti di informazione...

2. È tutelato e garantito, in particolare, il diritto di accesso ai servizi informatici...((, nonchè alle strutture ed ai servizi...))...
```

**Risultato**: ✅ **Conversione perfetta**

**Funzionalità converter**:
- ✅ Estrazione metadata (tipo, numero, anno, dataGU)
- ✅ Parsing articoli con numero e rubrica
- ✅ Commi numerati
- ✅ Modifiche legislative wrapped in `(( ))`
- ✅ Pulizia HTML entities (È, à, ì, etc.)
- ✅ Output identico a converter XML attuale

---

### ✅ 3. Ricerca Semplice (FUNZIONANTE)

**Endpoint**: `POST /api/v1/ricerca/semplice`

**Errori iniziali nei test** (causa 500 error):
1. ❌ **URL incompleto**: Usavo `/bff-opendata/api/v1/...` invece di `/t/normattiva.api/bff-opendata/v1/api/v1/...`
2. ❌ **Header mancante**: Non specificavo `Content-Type: application/json`
3. ❌ **Campo paginazione mancante**: Obbligatorio nella request

**Test CORRETTO** (`scripts/test_workflow_completo_funzionante.py`):
```bash
curl -X POST 'https://api.normattiva.it/t/normattiva.api/bff-opendata/v1/api/v1/ricerca/semplice' \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json' \
  -d '{
    "testoRicerca": "legge 4 2004",
    "orderType": "recente",
    "paginazione": {
      "paginaCorrente": 1,
      "numeroElementiPerPagina": 10
    }
  }'
```

**Risultato**: ✅ **200 OK**

**Response** (estratto):
```json
{
  "listaAtti": [
    {
      "numeroProvvedimento": "4",
      "annoProvvedimento": "2004",
      "denominazioneAtto": "LEGGE",
      "dataGU": "2004-01-17",
      "codiceRedazionale": "004G0015",
      "titoloAtto": "Disposizioni per favorire...",
      "descrizioneAtto": "LEGGE 9 gennaio 2004, n. 4"
    }
  ],
  "facetMap": { ... }
}
```

**Parametri estratti** (utilizzabili per `/atto/dettaglio-atto`):
- ✅ `dataGU`: Data Gazzetta Ufficiale
- ✅ `codiceRedazionale`: Codice identificativo atto
- ✅ Metadata: tipo, numero, anno, titolo

---

## Workflow Completo

### Workflow 1: Da URL Normattiva (Raccomandato)

**Input**: URL permalink normattiva.it

**Step**:

1. **Estrai parametri da URL** (parsing standard, no HTML scraping):

   ```python
   from urllib.parse import urlparse, parse_qs

   # Da URL tipo: /uri-res/N2Ls?urn:nir:stato:legge:2004:4
   # O da: /do/atto/caricaAKN?dataGU=20040117&codiceRedaz=004G0015

   parsed = urlparse(url)
   query = parse_qs(parsed.query)

   # Estrazione con regex o parsing query string
   dataGU = query.get('dataGU')[0]  # Formato YYYYMMDD → converti in YYYY-MM-DD
   codiceRedaz = query.get('codiceRedaz')[0]
   ```

2. **Chiama API dettaglio atto**:

   ```python
   import requests

   payload = {
       "dataGU": "2004-01-17",
       "codiceRedazionale": "004G0015",
       "formatoRichiesta": "V"
   }

   response = requests.post(
       "https://api.normattiva.it/t/normattiva.api/bff-opendata/v1/api/v1/atto/dettaglio-atto",
       json=payload,
       headers={"Content-Type": "application/json"}
   )

   atto_data = response.json()
   ```

3. **Converti HTML → Markdown**:

   ```python
   from api_html_to_markdown import api_response_to_markdown

   markdown = api_response_to_markdown(atto_data)

   with open('output.md', 'w') as f:
       f.write(markdown)
   ```

**Pro**:
- ✅ 1 richiesta API (equivalente ad approccio attuale)
- ✅ Nessun HTML scraping della pagina web
- ✅ Parsing URL standard (query string o regex)
- ✅ Output immediato

**Contro**:
- ⚠️ Richiede parsing URL per estrarre parametri (stesso problema approccio attuale)

---

### Workflow 2: Da Ricerca API (FUNZIONANTE ✅)

**Input**: Parametri ricerca (tipo, numero, anno, testo)

**Step**:

1. **Ricerca atto**:

   ```python
   search_payload = {
       "testoRicerca": "legge 4 2004",
       "orderType": "recente",
       "paginazione": {
           "paginaCorrente": 1,
           "numeroElementiPerPagina": 10
       }
   }

   search_response = requests.post(
       "https://api.normattiva.it/t/normattiva.api/bff-opendata/v1/api/v1/ricerca/semplice",
       headers={"Content-Type": "application/json"},  # IMPORTANTE!
       json=search_payload
   )

   risultati = search_response.json()['listaAtti']
   ```

   **Response**:
   ```json
   {
     "listaAtti": [
       {
         "dataGU": "2004-01-17",
         "codiceRedazionale": "004G0015",
         "numeroProvvedimento": "4",
         "annoProvvedimento": "2004",
         "denominazioneAtto": "LEGGE",
         "descrizioneAtto": "LEGGE 9 gennaio 2004, n. 4"
       }
     ]
   }
   ```

2. **Estrai parametri e chiama dettaglio**:

   ```python
   atto = risultati[0]

   dettaglio_response = requests.post(
       ".../api/v1/atto/dettaglio-atto",
       json={
           "dataGU": atto['dataGU'],
           "codiceRedazionale": atto['codiceRedazionale'],
           "formatoRichiesta": "V"
       }
   )
   ```

3. **Converti HTML → Markdown** (come Workflow 1 step 3)

**Pro**:
- ✅ **Nessun parsing URL necessario**
- ✅ Ricerca flessibile (parole chiave, titolo, testo)
- ✅ **Workflow 100% API ufficiali**
- ✅ Filtri avanzati disponibili

**Test completo**: `scripts/test_workflow_completo_funzionante.py`

---

### Workflow 3: Export Asincrono (Batch)

**Use case**: Download di collezioni (decine/centinaia atti)

**Step**:

1. **Crea richiesta export**:

   ```bash
   curl -X POST '.../api/v1/ricerca-asincrona/nuova-ricerca' \
     -H 'Content-Type: application/json' \
     -d '{
       "email": "user@example.com",
       "filtri": {
         "tipo": "LEGGE",
         "anno": "2024"
       },
       "formato": "JSON",
       "formatoRichiesta": "V"
     }'
   ```

   **Response**:
   ```json
   {
     "token": "ABC123XYZ",
     "status": "PENDING"
   }
   ```

   **⚠️ IMPORTANTE**:
   - Il campo `email` è **OPZIONALE** (canale di notifica)
   - Il `token` è **disponibile subito nella response**
   - Non serve attendere email per proseguire

2. **Conferma richiesta** (usa token dalla response):

   ```bash
   curl -X PUT '.../api/v1/ricerca-asincrona/conferma-ricerca' \
     -d '{"token": "ABC123XYZ"}'
   ```

3. **Polling status**:

   ```bash
   curl '.../api/v1/ricerca-asincrona/check-status/ABC123XYZ'
   ```

   **Response quando pronto**:
   ```json
   {
     "status": "COMPLETED",
     "downloadUrl": "..."
   }
   ```

   Oppure URL in header `x-ipzs-location`

4. **Download ZIP**:

   ```bash
   curl '.../api/v1/collections/download/collection-asincrona/ABC123XYZ' \
     -o collezione.zip
   ```

**Pro**:
- ✅ Batch di atti
- ✅ Formato JSON/XML/AKN disponibili
- ✅ **Email opzionale** (token in response)
- ✅ Completamente scriptabile

**Contro**:
- ❌ Overhead per singolo atto
- ❌ Latenza elaborazione (minuti)
- ❌ ZIP da estrarre

---

## Confronto Approcci

| Aspetto | Approccio Attuale (caricaAKN) | API OpenData (dettaglio-atto) |
|---------|-------------------------------|-------------------------------|
| **Input** | URL normattiva.it | URL o parametri ricerca |
| **Richieste HTTP** | 1 (GET diretto XML) | 1 (POST API) |
| **Formato source** | XML Akoma Ntoso | HTML strutturato |
| **Parsing** | XML con lxml | HTML con regex/BeautifulSoup |
| **Complessità parsing** | Media (namespace XML) | Media (classi CSS) |
| **Standard** | ✅ Akoma Ntoso 3.0 | HTML con naming Akoma Ntoso |
| **Autenticazione** | Nessuna | Nessuna |
| **Email required** | No | No |
| **Scraping HTML pagina** | Sì (estrazione parametri) | Sì (estrazione parametri) |
| **API ufficiali** | No (endpoint non documentato) | ✅ Sì (documentate) |
| **Stabilità** | ✅ Alta (anni utilizzo) | ⚠️ Media (nuove, da testare) |
| **Metadata arricchiti** | No | ✅ Sì (date vigenza, tipo, etc.) |
| **Batch support** | No | ✅ Sì (export asincrono) |
| **Output converter** | Markdown | Markdown (equivalente) |

---

## Raccomandazioni

### Per v2.x (Attuale - Produzione)

**✅ MANTENERE approccio attuale** (endpoint `caricaAKN`)

**Motivi**:
1. ✅ **Stabilità collaudata** - Funziona da anni senza problemi
2. ✅ **XML Akoma Ntoso** - Standard internazionale, converter testato
3. ✅ **Equivalenza pratica** - Stesso numero richieste HTTP
4. ✅ **Rischio zero** - Nessuna necessità di migration
5. ⚠️ **API nuove** - Da testare stabilità nel tempo

---

### Per v3.0+ (Futuro - Valutazione)

**💡 VALUTARE migrazione ad API OpenData**

#### Stato Attuale
- ✅ Endpoint `/ricerca/semplice` **FUNZIONANTE** (test verificati)
- ✅ Endpoint `/atto/dettaglio-atto` funzionante
- ✅ **Workflow completo testato e validato**
- ⚠️ Stabilità da dimostrare nel tempo (6-12 mesi)

#### Vantaggi migrazione
- ✅ **API ufficialmente documentate** e supportate
- ✅ **Nessun parsing URL/HTML** necessario
- ✅ **Ricerca flessibile** (testo, tipo, anno, filtri)
- ✅ **Metadata arricchiti** (date vigenza, storia versioni)
- ✅ **Supporto batch nativo** (export asincrono)
- ✅ **Workflow 100% API ufficiali**

#### Opzioni implementazione

##### A) Hybrid Mode (Consigliato per transizione)
```python
# 1. Usa API per metadata
metadata = api_get_metadata(dataGU, codiceRedaz)

# 2. Usa caricaAKN per XML (più stabile)
xml = download_via_caricaAKN(dataGU, codiceRedaz)

# 3. Converti con metadata arricchiti
convert_to_markdown(xml, metadata_extra=metadata)
```

**Pro**: Migliore dei due mondi - stabilità XML + metadata API

##### B) Full API Mode
```python
# Tutto via API OpenData
html_data = api_dettaglio_atto(dataGU, codiceRedaz)
markdown = convert_html_to_markdown(html_data)
```

**Pro**: Approccio ufficiale e documentato

##### C) Dual Mode con fallback
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

**Pro**: Massima resilienza

---

### Feature Opzionali v2.3.0+

#### 1. Flag `--use-api` (Sperimentale)

```bash
normattiva2md --use-api "URL" output.md
```

**Comportamento**:
- Usa API OpenData invece di caricaAKN
- Metadata arricchiti in YAML front matter
- Stesso output Markdown

**Uso**: Test comparativo, utenti che preferiscono API ufficiali

#### 2. Batch Mode

```bash
normattiva2md --batch-async \
  --tipo LEGGE --anno 2024 \
  --formato JSON \
  -o output/
```

**Comportamento**:
- Usa workflow export asincrono
- Scarica ZIP
- Converte automaticamente tutti gli atti

**Uso**: Download collezioni intere

---

## Test File

**Script test**:
- ✅ `scripts/test_dettaglio.sh` - Test curl endpoint dettaglio atto
- ✅ `scripts/api_html_to_markdown.py` - Converter HTML→Markdown funzionante
- ✅ `scripts/test_workflow_completo_funzionante.py` - **Workflow completo ricerca→dettaglio→markdown**

**Output test**:
- ✅ `output/dettaglio_response.json` - Response API dettaglio atto
- ✅ `output/dettaglio_from_search.json` - Response dettaglio da ricerca
- ✅ `output/params_from_search.json` - Parametri estratti da ricerca
- ✅ `legge_stanca_from_api.md` - Markdown da HTML API
- ✅ `atto_from_workflow_completo.md` - Markdown da workflow completo

**Documentazione**:
- ✅ `WORKFLOW_API_FUNZIONANTE.md` - Documentazione workflow completo
- ✅ `output/openapi-bff-opendata.json` - Specifica OpenAPI ufficiale

---

## Conclusioni

### Correzione Analisi Precedente

**❌ ERRATO** (prima dei test):
> "Le API non offrono endpoint diretto per singolo atto"
> "Serve email e workflow complesso"
> "API non adatte per sostituire approccio attuale"

**✅ CORRETTO** (dopo test verificati):
- ✅ Endpoint `/atto/dettaglio-atto` **funzionante perfettamente**
- ✅ Ritorna HTML **ben strutturato** e facilmente convertibile
- ✅ **Nessuna email richiesta** per singoli atti
- ✅ Workflow **equivalente** in complessità ad approccio attuale
- ✅ Email **opzionale** solo per export asincroni (token in response)

### Stato Finale

**Per uso singolo atto**:
- ✅ API OpenData **COMPLETAMENTE UTILIZZABILI**
- ✅ Approccio attuale **EQUIVALENTE** in complessità
- ✅ **Entrambi validi**, scelta basata su:
  - **Stabilità**: caricaAKN collaudato da anni
  - **Standard**: XML AKN vs HTML strutturato
  - **Ufficialità**: API documentate vs endpoint non documentato
  - **Metadata**: Basic vs arricchiti

**Per uso batch**:
- ✅ API OpenData **SUPERIORI**
- ✅ Export asincrono completamente scriptabile
- ✅ Nessuna email necessaria (token in response)
- ✅ Formati multipli (JSON, XML, AKN, HTML)

**Raccomandazione finale**:
- **v2.x**: Mantenere caricaAKN (stabilità collaudata)
- **v3.0+**: Valutare API quando dimostrata stabilità
- **Batch**: Considerare API da subito (vantaggio chiaro)

---

**Data documento**: 2026-01-01
**Versione**: 2.0 (riscrittura completa con test verificati)
**Status**: ✅ Test completati, workflow validato
**Prossimi step**: Monitorare stabilità API, testare in produzione quando mature
