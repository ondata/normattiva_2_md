# API OpenData Normattiva - Documentazione e Test

Questa cartella contiene la documentazione e i test per le API OpenData di Normattiva.

## Struttura

```
docs/api-opendata/
├── README.md                           # Questo file
├── M2M_API_EVALUATION.md              # Valutazione completa API M2M
├── JSON_VS_XML_EVALUATION.md          # Confronto approccio JSON vs XML
├── WORKFLOW_API_FUNZIONANTE.md        # Workflow funzionante testato
├── scripts/                            # Script di test
│   ├── test_workflow_completo_funzionante.py  # Test workflow completo
│   ├── api_html_to_markdown.py        # Converter HTML → Markdown
│   └── test_dettaglio.sh              # Test curl endpoint dettaglio
└── output/                             # Output generati dagli script (non versionato)
```

## Documentazione

### M2M_API_EVALUATION.md
Valutazione completa delle API OpenData con test dei 3 endpoint principali:
- `/atto/dettaglio-atto` ✅ FUNZIONANTE
- `/atto/dettaglio-atto-multi` ✅ FUNZIONANTE
- `/ricerca/semplice` ✅ FUNZIONANTE

### JSON_VS_XML_EVALUATION.md
Confronto approfondito tra:
- Approccio attuale (XML Akoma Ntoso)
- Approccio API JSON con HTML strutturato
- **RACCOMANDATO**: Workflow Ricerca + Dettaglio (100% API ufficiali)

### WORKFLOW_API_FUNZIONANTE.md
Descrizione del workflow funzionante testato:
1. Ricerca API → estrai `dataGU` + `codiceRedazionale`
2. Dettaglio API → scarica HTML strutturato
3. Conversione HTML → Markdown

## Script di Test

### test_workflow_completo_funzionante.py
Workflow completo funzionante:
```bash
cd docs/api-opendata/scripts
python3 test_workflow_completo_funzionante.py
```

Esegue:
1. Ricerca "legge 4 2004"
2. Estrazione parametri dalla risposta
3. Download dettaglio atto
4. Conversione in Markdown

Output salvati in `../output/`:
- `params_from_search.json`
- `dettaglio_from_search.json`
- `atto_from_workflow_completo.md`

### api_html_to_markdown.py
Converter HTML → Markdown per risposte API:
```bash
cd docs/api-opendata/scripts
python3 api_html_to_markdown.py
```

Converte `../output/dettaglio_response.json` in Markdown strutturato.

### test_dettaglio.sh
Test curl semplice per endpoint dettaglio:
```bash
cd docs/api-opendata/scripts
bash test_dettaglio.sh
```

Scarica Legge 4/2004 (Legge Stanca) in `../output/dettaglio_response.json`.

## API Endpoint

**Base URL**: `https://api.normattiva.it/t/normattiva.api/bff-opendata/v1`

**Headers richiesti**:
- `Content-Type: application/json`
- `Accept: application/json`

### Ricerca Semplice
```bash
POST /api/v1/ricerca/semplice
{
  "testoRicerca": "legge 4 2004",
  "orderType": "recente",
  "paginazione": {
    "paginaCorrente": 1,
    "numeroElementiPerPagina": 10
  }
}
```

### Dettaglio Atto
```bash
POST /api/v1/atto/dettaglio-atto
{
  "dataGU": "2004-01-17",
  "codiceRedazionale": "004G0015",
  "formatoRichiesta": "V"
}
```

## Workflow Raccomandato per v3.0+

Per la versione 3.0+ del tool `normattiva2md`, il workflow raccomandato è:

1. **Ricerca via API** invece di parsing URL
2. **Estrazione parametri** da risultati ricerca
3. **Download dettaglio** con parametri estratti
4. **Conversione HTML → Markdown** con parser esistente

**Vantaggi**:
- ✅ Nessun parsing URL necessario
- ✅ Nessuno scraping HTML
- ✅ 100% API ufficiali
- ✅ Ricerca flessibile (testo, filtri, ordinamento)
- ✅ HTML già strutturato con classi Akoma Ntoso

Vedi `JSON_VS_XML_EVALUATION.md` per dettagli completi.
