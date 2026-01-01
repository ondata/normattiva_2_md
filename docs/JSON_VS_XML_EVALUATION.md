# Valutazione Approcci: XML AKN vs JSON vs Approccio Attuale

**Data**: 2026-01-01
**Contesto**: Analisi comparativa tra formati disponibili dalle API OpenData

---

## Executive Summary

Le API OpenData di Normattiva forniscono **3 formati strutturati**:

1. **XML Akoma Ntoso (AKN)** - Standard legale XML
2. **JSON** - Struttura equivalente ad AKN
3. **HTML** - Solo via endpoint `/atto/dettaglio-atto` (limitato)

**Scoperta chiave**: ✅ **JSON e XML AKN hanno struttura equivalente e completa**

**Test effettuato**: Conversione JSON→Markdown funziona perfettamente (vedi `tmp/json_to_markdown_poc.py`)

---

## Confronto Formati

### 1. XML Akoma Ntoso (AKN)

**Pro**:
- ✅ Standard internazionale per documenti legislativi
- ✅ Stesso formato già processato da normattiva2md v2.x
- ✅ Codice converter già esistente e testato
- ✅ Supporta tutte le feature (articoli, modifiche, riferimenti)

**Contro**:
- ❌ Richiede parsing XML (complessità moderata)
- ❌ File più grandi (~10-50 KB per atto)

**Disponibilità**:
- ✅ Collezioni preconfezionate (ZIP)
- ✅ Collezioni asincrone (ZIP dopo workflow)
- ✅ Endpoint diretto `caricaAKN` (approccio attuale)

---

### 2. JSON

**Pro**:
- ✅ Parsing più semplice (nativo Python)
- ✅ Struttura equivalente ad AKN
- ✅ Metadata arricchiti (URN, ELI, storia versioni)
- ✅ File più compatti (~8-30 KB per atto)
- ✅ Più facile da debuggare

**Contro**:
- ❌ Richiede nuovo converter JSON→Markdown
- ❌ Non standard come AKN

**Disponibilità**:
- ✅ Collezioni preconfezionate (ZIP)
- ✅ Collezioni asincrone (ZIP dopo workflow)
- ❌ **NON disponibile via endpoint diretto singolo atto**

**Struttura JSON**:
```json
{
  "metadati": {
    "urn": "...",
    "eli": "...",
    "tipoDoc": "LEGGE",
    "numDoc": "4",
    "titoloDoc": "...",
    "dataDoc": "2004-01-09"
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

---

### 3. Approccio Attuale (caricaAKN)

**Pro**:
- ✅ **1 richiesta HTTP** per scaricare XML AKN
- ✅ **Input user-friendly** (URL permalink)
- ✅ **Nessuna autenticazione** richiesta
- ✅ **Codice esistente e testato**
- ✅ **Download immediato** (no ZIP, no email, no polling)

**Contro**:
- ❌ Richiede HTML scraping per estrarre parametri
- ❌ Fragile se struttura HTML cambia
- ❌ Non usa API ufficiali documentate

**Flusso**:
```
URL → Scraping HTML → Estrai parametri → GET caricaAKN → XML AKN → Markdown
```

---

## Workflow delle API OpenData

### Opzione A: Collezioni Preconfezionate

**Flusso**:
```
GET /collections/collection-predefinite → Scegli collezione → GET /download/collection-preconfezionata?formato=AKN&nome=X → ZIP
```

**Pro**:
- ✅ Nessuna autenticazione
- ✅ Download immediato

**Contro**:
- ❌ **Solo collezioni predefinite** (non singoli atti custom)
- ❌ Download ZIP intero (overhead)
- ❌ Nessun filtro per singolo atto

**Uso**: Download collezioni predefinite (costituzione, codici, etc.)

---

### Opzione B: Collezioni Asincrone (Custom)

**Flusso**:
```
1. POST /ricerca-asincrona/nuova-ricerca → Token
2. Conferma via email
3. PUT /ricerca-asincrona/conferma-ricerca
4. GET /ricerca-asincrona/check-status (polling)
5. GET /download/collection-asincrona/{token} → ZIP
```

**Pro**:
- ✅ **Filtri custom** (anno, numero, tipo atto)
- ✅ Può selezionare singolo atto
- ✅ Formati AKN/JSON/XML disponibili

**Contro**:
- ❌ **Workflow complesso** (5 step)
- ❌ **Richiede email** valida
- ❌ **Latenza** (minuti/ore per elaborazione)
- ❌ **Download ZIP** (no singolo file)
- ❌ **Overkill per 1 atto**

**Uso**: Batch download (decine/centinaia atti)

---

### Opzione C: Endpoint caricaAKN (Attuale)

**Flusso**:
```
GET https://www.normattiva.it/do/atto/caricaAKN?dataGU=20040117&codiceRedaz=004G0015
```

**Pro**:
- ✅ **1 richiesta HTTP diretta**
- ✅ **XML AKN immediato**
- ✅ **Nessun ZIP, email, polling**
- ✅ **Ideale per singolo atto**

**Contro**:
- ❌ Non documentato ufficialmente
- ❌ Richiede estrazione parametri da URL (HTML scraping)

**Uso**: Download singolo atto (use case normattiva2md)

---

## Proof of Concept: JSON→Markdown

**Test eseguito**: `tmp/json_to_markdown_poc.py`

**Input**: `sample_atto_json.json` (DECRETO 12 aprile 1988, n. 164)

**Output**: Markdown ben formattato con:
- ✅ YAML front matter (metadata)
- ✅ Titolo documento
- ✅ Articoli numerati
- ✅ Note articoli
- ✅ Struttura ricorsiva (commi, elenchi)

**Codice converter**:
```python
def json_to_markdown(json_data):
    # 1. Metadata (YAML front matter)
    metadati = json_data.get('metadati', {})
    md_lines = ["---"]
    md_lines.append(f"urn: {metadati.get('urn')}")
    md_lines.append(f"tipo: {metadati.get('tipoDoc')}")
    # ...
    md_lines.append("---\n")

    # 2. Articolato
    for elemento in json_data['articolato']['elementi']:
        if elemento['nomeNir'] == 'articolo':
            md_lines.append(f"## Art. {elemento['numNir']}")
            md_lines.append(elemento['testo'])

    return "\n".join(md_lines)
```

**Risultato**: ✅ Conversione perfettamente funzionante

---

## Raccomandazioni

### Per normattiva2md v2.x (Uso Single-Document)

**✅ MANTENERE approccio attuale** (endpoint `caricaAKN`)

**Motivi**:
1. ✅ Unica richiesta HTTP
2. ✅ Nessuna complessità workflow
3. ✅ XML AKN diretto (formato già supportato)
4. ✅ Performance ottimali

**Rischio accettabile**: HTML scraping fragile ma mitigato da:
- Struttura HTML stabile negli anni
- Fallback possibile se cambia

---

### Per normattiva2md v3.0+ (Futuro)

**💡 VALUTARE migrazione graduale ad API OpenData**

#### Scenario 1: API Singolo Atto (se disponibile)

Se in futuro Normattiva aggiunge endpoint tipo:
```
POST /api/v1/atto/download
{
  "dataGU": "2004-01-17",
  "codiceRedazionale": "004G0015",
  "formato": "AKN"  // o "JSON"
}
→ File XML/JSON diretto (no ZIP)
```

**Allora**: Migrare immediatamente

---

#### Scenario 2: Workflow Semplificato

Se workflow asincrono viene semplificato:
- Nessuna email richiesta (API key invece)
- Risposta immediata per 1 atto
- File diretto (no ZIP)

**Allora**: Valutare migrazione

---

#### Scenario 3: Supporto JSON Diretto

Se aggiungono endpoint:
```
POST /api/v1/atto/dettaglio-atto
{
  "dataGU": "2004-01-17",
  "codiceRedazionale": "004G0015",
  "formato": "JSON_COMPLETO"  // Non solo HTML
}
→ JSON completo con articolato
```

**Allora**: Implementare converter JSON→Markdown (già testato)

---

### Feature Opzionali v2.3.0+

#### 1. Hybrid Mode (Migliore dei 2 mondi)

**Workflow**:
```python
# 1. Usa approccio attuale per download XML
xml_path = download_via_caricaAKN(url)

# 2. Arricchisci con metadata da API OpenData
metadata = get_metadata_from_api(dataGU, codiceRedaz)

# 3. Converti con metadata arricchiti
convert_to_markdown(xml_path, metadata)
```

**Vantaggi**:
- Download veloce (1 richiesta)
- Metadata completi da API ufficiali
- Nessun workflow complesso

---

#### 2. Batch Mode con API OpenData

```bash
normattiva2md --batch-async query.json -o output/
```

**Usa**:
- Ricerca asincrona API per filtri complessi
- Download collezione ZIP
- Conversione automatica tutti gli atti

**Ideale per**:
- Download decine/centinaia atti
- Ricerca per criteri (anno, tipo, keyword)

---

#### 3. Format Selection

```bash
normattiva2md --source-format json "URL" output.md
```

**Opzioni**:
- `--source-format akn`: XML Akoma Ntoso (default)
- `--source-format json`: JSON da collezione
- `--source-format auto`: Rileva automaticamente

---

## Conclusioni Finali

### Per v2.x (Attuale)

**✅ RACCOMANDAZIONE**: Mantenere approccio attuale

**Motivi**:
1. ✅ Funziona perfettamente per use case principale
2. ✅ API OpenData non offrono endpoint diretto per singolo atto
3. ✅ Workflow asincrono troppo complesso per 1 documento
4. ✅ Nessun beneficio tangibile in performance

---

### Per v3.0 (Futuro)

**💡 OPPORTUNITÀ**: API OpenData quando workflow si semplifica

**Formati preferiti** (in ordine):
1. **JSON** - Parsing più semplice, POC già funzionante
2. **XML AKN** - Standard, converter esistente
3. **HTML** - Ultima risorsa

**Prerequisiti per migrazione**:
- Endpoint diretto singolo atto (no ZIP)
- Nessuna email/polling richiesto
- Latenza accettabile (<2s)

---

## Test Files

- `tmp/sample_atto_json.json`: Esempio JSON da collezione
- `tmp/json_to_markdown_poc.py`: Converter JSON→MD funzionante
- `tmp/sample_atto_from_json.md`: Output Markdown da JSON
- `tmp/sample_json.zip`: Collezione JSON preconfezionata
- `tmp/openapi-bff-opendata.json`: Specifica API complete

---

**Data documento**: 2026-01-01
**Stato**: ✅ Analisi completata
**Conclusione**: Approccio attuale ottimale, JSON promettente per futuro
