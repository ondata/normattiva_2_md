# Valutazione API OpenData di Normattiva.it

**Data**: 2026-01-01
**Versione progetto**: v2.1.2
**Documentazione ufficiale**: https://dati.normattiva.it/Come-scaricare-i-dati

---

## Executive Summary

Esiste un portale OpenData ufficiale di Normattiva (`dati.normattiva.it`) con **API REST pubbliche** documentate. Le API sono progettate principalmente per:

- **Ricerca** atti normativi (semplice e avanzata)
- **Download di collezioni** (ZIP con XML/JSON/HTML)
- **Dettaglio atti in formato HTML**

**Conclusione**: Le API OpenData **non sono adatte** per sostituire l'approccio attuale di `normattiva2md` perché:

1. ❌ L'endpoint `/atto/dettaglio-atto` ritorna **HTML**, non XML Akoma Ntoso
2. ❌ Per ottenere XML Akoma Ntoso serve scaricare **collezioni ZIP** (workflow complesso)
3. ❌ Non esiste endpoint diretto per scaricare singolo atto in formato XML
4. ✅ **L'approccio attuale rimane il più efficiente** per uso single-document

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

## Endpoint Principali

### 1. Ricerca Semplice

**Endpoint**: `POST /api/v1/ricerca/semplice`

**Request**:
```json
{
  "testoRicerca": "accessibilità digitale",
  "paginazione": {
    "paginaCorrente": 0,
    "numeroElementiPerPagina": 10
  }
}
```

**Response**: Lista atti con metadata (titolo, data GU, codice redazionale)

**Uso**: Trovare atti per parole chiave

---

### 2. Dettaglio Atto

**Endpoint**: `POST /api/v1/atto/dettaglio-atto`

**Request**:
```json
{
  "dataGU": "2004-01-17",
  "codiceRedazionale": "004G0015",
  "versione": 0
}
```

**Response**:
```json
{
  "success": true,
  "code": null,
  "message": null,
  "data": {
    "atto": {
      "titolo": "LEGGE 9 gennaio 2004, n. 4",
      "sottoTitolo": "...",
      "articoloHtml": "<div class=\"bodyTesto\">...</div>",
      "testoInVigore": null,
      "tipoProvvedimentoDescrizione": "LEGGE",
      "annoProvvedimento": 2004,
      "numeroProvvedimento": 4,
      "dataGU": "2004-01-17",
      "codiceRedazionale": "004G0015",
      ...
    }
  }
}
```

**⚠️ IMPORTANTE**:
- **Formato output**: HTML (`articoloHtml`)
- **NON include**: XML Akoma Ntoso
- **Parametri**: Richiede `dataGU` e `codiceRedazionale` (non URL permalink)

**Test effettuato**:
```bash
curl -X POST 'https://api.normattiva.it/t/normattiva.api/bff-opendata/v1/api/v1/atto/dettaglio-atto' \
  -H 'Content-Type: application/json' \
  -d '{
    "dataGU": "2004-01-17",
    "codiceRedazionale": "004G0015",
    "versione": 0
  }'
```

**Risultato**: ✅ Funziona, ma ritorna solo HTML

---

### 3. Download Collezioni Preconfezionate

**Endpoint**: `GET /api/v1/collections/download/collection-preconfezionata`

**Parametri**:
- `nome`: Nome collezione (es. "costituzione")
- `formato`: AKN (Akoma Ntoso XML), XML (NormeInRete), JSON, HTML, PDF, EPUB, RTF
- `formatoRichiesta`: ORIGINALE, VIGENTE, MULTIVIGENTE

**Esempio**:
```bash
curl 'https://api.normattiva.it/t/normattiva.api/bff-opendata/v1/api/v1/collections/download/collection-preconfezionata?nome=costituzione&formato=AKN&formatoRichiesta=VIGENTE'
```

**Response**: File ZIP contenente atti in formato richiesto

**✅ Questo endpoint fornisce XML Akoma Ntoso**, ma:
- Scarica collezioni intere (non singoli atti)
- Restituisce ZIP da estrarre
- Collezioni preconfezionate (lista limitata)

---

### 4. Ricerca Asincrona (Collezioni Dinamiche)

**Workflow completo** per ottenere XML Akoma Ntoso:

#### Fase 1: Richiesta Nuova Ricerca
```http
POST /api/v1/ricerca-asincrona/nuova-ricerca
Content-Type: application/json

{
  "formato": "AKN",
  "richiestaExport": "V",
  "email": "user@example.com",
  "parametriRicerca": {
    "denominazioneAtto": "LEGGE",
    "annoProvvedimento": 2004
  }
}
```

**Response**: Token (es. `abc123xyz`)

#### Fase 2: Conferma via Email
Utente riceve email con link di conferma

#### Fase 3: Conferma Ricerca
```http
PUT /api/v1/ricerca-asincrona/conferma-ricerca
Content-Type: application/json

{
  "token": "abc123xyz"
}
```

#### Fase 4: Polling Status
```http
GET /api/v1/ricerca-asincrona/check-status/abc123xyz
```

**Response**:
```json
{
  "stato": 3,
  "descrizioneStato": "Ricerca elaborata con successo",
  "url": "https://..."
}
```

Stati possibili:
- `0`: Da confermare
- `1`: Confermata in attesa
- `2`: In elaborazione
- `3`: ✅ Completata (fornisce URL download)
- `4`: ❌ Errore

#### Fase 5: Download ZIP
```http
GET /api/v1/collections/download/collection-asincrona/{token}
```

**Response**: File ZIP con XML Akoma Ntoso

---

## Confronto: Approccio Attuale vs API OpenData

### Approccio Attuale (v2.1.2)

**Flusso**:
```
URL Permalink → Scraping HTML → Estrai parametri → Download XML diretto → Converti MD
```

**Pro**:
- ✅ **Una sola richiesta HTTP** per scaricare XML
- ✅ **Input user-friendly**: URL permalink
- ✅ **Nessuna autenticazione**
- ✅ **Download diretto** senza ZIP/estrazione
- ✅ **Filtro articolo integrato** (--art flag)

**Contro**:
- ❌ Dipende da HTML scraping (fragile)
- ❌ Richiede regex per estrarre parametri

---

### Approccio con API OpenData

#### Scenario A: Dettaglio Atto (HTML)

**Flusso**:
```
URL → Estrai parametri → POST /atto/dettaglio-atto → HTML → ??? (non utilizzabile)
```

**Pro**:
- ✅ API ufficiali documentate
- ✅ Risposta JSON strutturata

**Contro**:
- ❌ **Ritorna HTML, non XML Akoma Ntoso**
- ❌ Non utilizzabile per normattiva2md
- ❌ Richiede comunque parsing URL per parametri

---

#### Scenario B: Collezioni Asincrone (XML)

**Flusso**:
```
URL → Estrai parametri → Ricerca → Email confirm → Polling → Download ZIP → Estrai → XML
```

**Pro**:
- ✅ **Fornisce XML Akoma Ntoso**
- ✅ API ufficiali
- ✅ Supporta batch download

**Contro**:
- ❌ **Workflow complesso** (6 step vs 1)
- ❌ **Richiede email** e conferma manuale
- ❌ **Polling status** (latenza)
- ❌ **Download ZIP** (overhead)
- ❌ **Estrazione file** necessaria
- ❌ **Overkill per singolo atto**

---

## Matrice di Valutazione

| Criterio | Approccio Attuale | API `/atto/dettaglio-atto` | API Collezioni Asincrone |
|----------|-------------------|----------------------------|--------------------------|
| **Formato output** | ⭐⭐⭐⭐⭐ XML Akoma | ⭐ HTML | ⭐⭐⭐⭐⭐ XML Akoma |
| **Semplicità** | ⭐⭐⭐⭐ (1 request) | ⭐⭐⭐⭐ (1 request) | ⭐ (6 steps) |
| **Velocità** | ⭐⭐⭐⭐⭐ Immediato | ⭐⭐⭐⭐⭐ Immediato | ⭐⭐ (polling + wait) |
| **Input** | ⭐⭐⭐⭐⭐ URL | ⭐⭐ (parametri) | ⭐⭐ (parametri) |
| **Robustezza** | ⭐⭐⭐ (HTML scraping) | ⭐⭐⭐⭐⭐ (API) | ⭐⭐⭐⭐⭐ (API) |
| **Autenticazione** | ⭐⭐⭐⭐⭐ Nessuna | ⭐⭐⭐⭐⭐ Nessuna | ⭐⭐⭐ (email) |
| **Overhead** | ⭐⭐⭐⭐⭐ Minimo | ⭐⭐⭐⭐⭐ Minimo | ⭐ (ZIP extract) |
| **Uso single-doc** | ⭐⭐⭐⭐⭐ Ideale | ❌ Non applicabile | ⭐ (overkill) |
| **Uso batch** | ⭐⭐⭐ (loop) | ❌ Non applicabile | ⭐⭐⭐⭐⭐ Ideale |

**Punteggi**:
- **Approccio Attuale (single-doc)**: 36/40 (90%)
- **API `/atto/dettaglio-atto`**: Non applicabile (formato incompatibile)
- **API Collezioni Asincrone (single-doc)**: 16/40 (40%)
- **API Collezioni Asincrone (batch)**: 32/40 (80%)

---

## Raccomandazioni

### Per Uso Single-Document (caso attuale)

**✅ MANTENERE approccio attuale**: Download XML diretto via `caricaAKN` endpoint

**Motivi**:
1. Unica richiesta HTTP
2. Nessuna dipendenza da email/conferme
3. Nessun overhead ZIP
4. XML Akoma Ntoso diretto

**Miglioramento possibile**:
- Utilizzare API `/ricerca/semplice` per **validare** esistenza atto prima del download
- Mantiene approccio attuale per download XML

---

### Per Uso Batch (futuro)

**✅ VALUTARE** API Collezioni Asincrone se:
- Serve scaricare **decine/centinaia** di atti
- Accettabile latenza (minuti/ore)
- Workflow automatizzabile (email API key)

**Implementazione**:
```python
# 1. Raccogliere lista atti da scaricare
atti_list = [...]

# 2. Creare ricerca asincrona con filtri
request_async_collection(atti_list, formato="AKN")

# 3. Confermare via email API
confirm_async_request(token)

# 4. Polling status
while status != "completed":
    time.sleep(30)
    status = check_status(token)

# 5. Download ZIP
download_zip(token)

# 6. Estrazione e conversione
extract_and_convert(zip_file)
```

---

## Possibili Usi delle API OpenData

### 1. Validazione Atto

**Prima di convertire**, verificare che l'atto esista:

```python
def validate_atto(data_gu, codice_redaz):
    """Verifica esistenza atto tramite API OpenData"""
    response = requests.post(
        "https://api.normattiva.it/t/normattiva.api/bff-opendata/v1/api/v1/atto/dettaglio-atto",
        json={
            "dataGU": data_gu,
            "codiceRedazionale": codice_redaz,
            "versione": 0
        }
    )
    return response.status_code == 200
```

**Vantaggio**: Evitare download XML di atti inesistenti

---

### 2. Ricerca Atti

**Trovare atti per keyword** prima di convertirli:

```python
def search_atti(keyword):
    """Cerca atti per parola chiave"""
    response = requests.post(
        "https://api.normattiva.it/t/normattiva.api/bff-opendata/v1/api/v1/ricerca/semplice",
        json={
            "testoRicerca": keyword,
            "paginazione": {
                "paginaCorrente": 0,
                "numeroElementiPerPagina": 50
            }
        }
    )
    data = response.json()
    return data.get('listaAtti', [])

# Esempio
atti = search_atti("accessibilità")
for atto in atti:
    print(f"{atto['titoloAtto']} - {atto['dataGU']}")
    # Convertire con normattiva2md
    normattiva2md(atto['dataGU'], atto['codiceRedazionale'])
```

---

### 3. Metadata Enrichment

**Arricchire** output Markdown con metadata da API:

```python
def get_metadata(data_gu, codice_redaz):
    """Ottieni metadata atto da API"""
    response = requests.post(
        "https://api.normattiva.it/t/normattiva.api/bff-opendata/v1/api/v1/atto/dettaglio-atto",
        json={
            "dataGU": data_gu,
            "codiceRedazionale": codice_redaz,
            "versione": 0
        }
    )
    atto = response.json()['data']['atto']

    return {
        'titolo': atto['titolo'],
        'sottotitolo': atto['sottoTitolo'],
        'tipo': atto['tipoProvvedimentoDescrizione'],
        'numero': atto['numeroProvvedimento'],
        'anno': atto['annoProvvedimento'],
        'data_gu': f"{atto['annoGU']}-{atto['meseGU']:02d}-{atto['giornoGU']:02d}",
        'numero_gu': atto['numeroGU']
    }

# Aggiungere a front matter YAML
---
titolo: LEGGE 9 gennaio 2004, n. 4
tipo: LEGGE
numero: 4
anno: 2004
data_gu: 2004-01-17
numero_gu: 13
---
```

---

## Limitazioni API OpenData

1. **Nessun endpoint XML singolo atto**: Solo collezioni ZIP
2. **Workflow asincrono complesso**: Email + polling + download
3. **Richiede parametri specifici**: `dataGU` + `codiceRedazionale` (non URL)
4. **Rate limiting**: Non documentato (da testare)
5. **Formato HTML**: Endpoint dettaglio non fornisce XML

---

## Conclusioni Finali

### Per normattiva2md v2.x

**✅ RACCOMANDAZIONE**: **Mantenere approccio attuale**

**Motivi**:
1. ✅ Approccio attuale funziona perfettamente per use case single-document
2. ✅ API OpenData non forniscono XML via endpoint diretto
3. ✅ Workflow collezioni asincrone è overkill per singoli atti
4. ✅ Nessun beneficio tangibile in performance o robustezza

---

### Possibili Integrazioni Future

**Feature opzionali** da considerare per v2.3.0+:

1. **Validazione pre-download**:
   ```bash
   normattiva2md --validate "URL"  # Verifica esistenza via API
   ```

2. **Ricerca interattiva**:
   ```bash
   normattiva2md --search "accessibilità"  # Mostra lista atti
   normattiva2md --search "accessibilità" --convert-all  # Batch conversion
   ```

3. **Metadata enrichment**:
   ```bash
   normattiva2md --enrich "URL"  # Aggiunge metadata completo da API
   ```

4. **Batch mode con collezioni**:
   ```bash
   normattiva2md --batch-async "query.json"  # Usa API collezioni
   ```

---

## Risorse

### Documentazione
- **Portale OpenData**: https://dati.normattiva.it
- **Guida download**: https://dati.normattiva.it/Come-scaricare-i-dati
- **Swagger UI**: https://dati.normattiva.it/assets/come_fare_per/Normattiva%20OpenData.html
- **PDF Specs**: https://dati.normattiva.it/assets/come_fare_per/API_Normattiva_OpenData.pdf
- **OpenAPI 3.0**: https://dati.normattiva.it/assets/come_fare_per/openapi-bff-opendata.json

### Test Effettuati
- `tmp/test_api_correct.py`: Test endpoint dettaglio-atto
- `tmp/test_api_formats.py`: Test formati payload diversi
- `tmp/test_full_response.py`: Salvataggio risposta completa
- `tmp/api_response_full.json`: Esempio risposta API reale
- `tmp/openapi-bff-opendata.json`: Specifica OpenAPI completa

---

**Data documento**: 2026-01-01
**Stato**: ✅ Analisi completata
**Prossimi step**: Nessuno (approccio attuale rimane ottimale)
