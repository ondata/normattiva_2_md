# Valutazione API Machine-to-Machine di Normattiva.it

**Data**: 2026-01-01
**Versione progetto**: v2.1.0
**Autore**: Analisi tecnica per normattiva2md

---

## 📋 Executive Summary

È stata scoperta l'esistenza di **API Machine-to-Machine (M2M) dedicate** per normattiva.it che potrebbero rivoluzionare l'architettura di accesso ai dati del progetto normattiva2md.

**Endpoint identificato**:
```
POST https://api.normattiva.it/t/normattiva.api/bff-mobile/v1/api/v1/atto/dettaglio-atto
```

Questo documento valuta l'impatto di queste nuove API e fornisce raccomandazioni per la loro integrazione nel progetto.

---

## 🔍 Panoramica delle API M2M

### Endpoint Principale: Dettaglio Atto

**URL**: `https://api.normattiva.it/t/normattiva.api/bff-mobile/v1/api/v1/atto/dettaglio-atto`

**Metodo**: `POST`

**Content-Type**: `application/json`

**Esempio Richiesta**:
```bash
curl --location 'https://api.normattiva.it/t/normattiva.api/bff-mobile/v1/api/v1/atto/dettaglio-atto' \
  -H 'Content-Type: application/json' \
  --data '{
    "dataGU": "2004-01-17",
    "codiceRedazionale": "004G0015",
    "idArticolo": 1,
    "versione": 0
  }'
```

**Parametri**:
- `dataGU` (string): Data di pubblicazione in Gazzetta Ufficiale (formato `YYYY-MM-DD`)
- `codiceRedazionale` (string): Codice redazionale dell'atto (es. `004G0015`)
- `idArticolo` (integer, opzionale): ID dell'articolo specifico (se vuoi solo un articolo)
- `versione` (integer): Versione del documento (0 = versione originale, > 0 = modifiche successive)

### Caratteristiche Tecniche

#### Formato Risposta
- **Tipo**: JSON strutturato (presumibilmente)
- **Vantaggi**: Parsing deterministico, nessun HTML scraping
- **Dati attesi**: Metadata + contenuto XML/JSON dell'atto

#### Autenticazione
- **Tipo**: Da determinare (API Key, OAuth2, o pubblico?)
- **Nota**: Le API M2M tipicamente richiedono autenticazione

#### Rate Limiting
- **Limiti**: Da determinare (richieste/secondo, giornaliere)
- **Quota**: Da verificare se esistono limiti per utente

---

## 🆚 Confronto: Approccio Attuale vs API M2M

### Approccio Attuale (v2.1.0)

**Flusso**:
```
URL Permalink → HTML Scraping → Estrazione Parametri → Download XML → Conversione MD
```

**Metodo**:
```python
# 1. Visita pagina HTML
response = session.get(url)

# 2. Estrai parametri con regex
match_gu = re.search(r'name="atto\.dataPubblicazioneGazzetta"[^>]*value="([^"]+)"', html)
match_codice = re.search(r'name="atto\.codiceRedazionale"[^>]*value="([^"]+)"', html)

# 3. Costruisci URL download
url = f"https://www.normattiva.it/do/atto/caricaAKN?dataGU={dataGU}&codiceRedaz={codiceRedaz}&dataVigenza={dataVigenza}"

# 4. Scarica XML
response = session.get(url)
```

**Punti critici**:
- ❌ Dipende dalla struttura HTML (fragile)
- ❌ Due richieste HTTP (pagina + download)
- ❌ Parsing con regex (error-prone)
- ❌ Nessun metadata strutturato

**Vantaggi**:
- ✅ Funziona con URL permalink user-friendly
- ✅ Non richiede autenticazione
- ✅ Già implementato e testato

---

### Approccio con API M2M (proposto)

**Flusso**:
```
Parametri → API Request JSON → Risposta JSON → Estrazione Dati → Conversione MD
```

**Metodo** (ipotetico):
```python
import requests

# 1. Prepara payload
payload = {
    "dataGU": "2004-01-17",
    "codiceRedazionale": "004G0015",
    "idArticolo": 1,  # opzionale
    "versione": 0
}

# 2. Chiamata API
response = requests.post(
    'https://api.normattiva.it/t/normattiva.api/bff-mobile/v1/api/v1/atto/dettaglio-atto',
    json=payload,
    headers={'Content-Type': 'application/json', 'Authorization': 'Bearer TOKEN'}
)

# 3. Parse JSON
data = response.json()

# 4. Estrai XML o converti direttamente da JSON
xml_content = data.get('contenuto_xml') or data.get('akoma_ntoso')
```

**Vantaggi potenziali**:
- ✅ **Struttura dati garantita**: JSON schema definito
- ✅ **Una sola richiesta HTTP**: Più veloce
- ✅ **Metadata arricchiti**: Più informazioni sull'atto
- ✅ **Supporto articoli specifici**: `idArticolo` integrato
- ✅ **Versioning nativo**: `versione` per gestire modifiche
- ✅ **Robusto**: Nessun HTML parsing
- ✅ **Performance**: Potenzialmente caching server-side

**Svantaggi potenziali**:
- ❌ Richiede conversione URL → parametri
- ❌ Possibile autenticazione richiesta
- ❌ Rate limiting da gestire
- ❌ Documentazione API potenzialmente assente/limitata
- ❌ Breaking changes possibili

---

## 📊 Matrice di Valutazione

| Criterio | Approccio Attuale | API M2M | Vincitore |
|----------|-------------------|---------|-----------|
| **Robustezza** | ⭐⭐ (HTML fragile) | ⭐⭐⭐⭐⭐ (JSON schema) | 🏆 M2M |
| **Performance** | ⭐⭐⭐ (2 richieste) | ⭐⭐⭐⭐⭐ (1 richiesta) | 🏆 M2M |
| **Facilità d'uso** | ⭐⭐⭐⭐⭐ (URL diretti) | ⭐⭐⭐ (parametri richiesti) | 🏆 Attuale |
| **Metadata** | ⭐⭐ (limitati) | ⭐⭐⭐⭐⭐ (completi) | 🏆 M2M |
| **Manutenibilità** | ⭐⭐ (regex fragili) | ⭐⭐⭐⭐⭐ (API contract) | 🏆 M2M |
| **Autenticazione** | ⭐⭐⭐⭐⭐ (nessuna) | ⭐⭐ (da gestire) | 🏆 Attuale |
| **Documentazione** | ⭐⭐⭐ (reverso) | ⭐⭐ (sconosciuta) | 🏆 Attuale |
| **Articoli specifici** | ⭐⭐⭐ (custom XML filter) | ⭐⭐⭐⭐⭐ (idArticolo) | 🏆 M2M |
| **Versioning** | ⭐⭐ (dataVigenza) | ⭐⭐⭐⭐⭐ (versione param) | 🏆 M2M |

**Punteggio totale**:
- Approccio Attuale: **26/45** (58%)
- API M2M: **38/45** (84%)

---

## 🔬 Analisi Approfondita

### 1. Formato Risposta API

**Ipotesi di risposta JSON** (da verificare):

```json
{
  "success": true,
  "data": {
    "atto": {
      "tipo": "LEGGE",
      "numero": "4",
      "anno": 2004,
      "dataGU": "2004-01-17",
      "numeroGU": "15",
      "codiceRedazionale": "004G0015",
      "titolo": "Disposizioni per favorire l'accesso dei soggetti disabili agli strumenti informatici",
      "alias": "Legge Stanca"
    },
    "contenuto": {
      "formato": "akoma_ntoso_3.0",
      "xml": "<?xml version=\"1.0\"?>...",
      "versione": 0,
      "dataVigenza": "2004-01-17"
    },
    "metadata": {
      "articoliTotali": 15,
      "modificato": false,
      "provvedimentiAttuativi": 12,
      "urlPubblico": "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2004-01-09;4"
    },
    "articolo": {
      "id": 1,
      "numero": "1",
      "titolo": "Obiettivi e finalità",
      "contenuto": "..."
    }
  }
}
```

**Vantaggi risposta JSON**:
- Metadata già parsati (tipo, numero, anno, titolo)
- XML embedded o link diretto
- Supporto articolo specifico già filtrato server-side
- Informazioni aggiuntive (provvedimenti attuativi, modifiche)

### 2. Mapping URL → Parametri API

**Problema**: L'utente fornisce URL, l'API vuole parametri.

**Soluzione 1: Parsing URL**

```python
def url_to_api_params(url):
    """
    Converte URL normattiva.it a parametri API M2M

    Input: https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2004-01-09;4
    Output: {'tipo': 'legge', 'anno': 2004, 'numero': 4, 'data': '2004-01-09'}
    """
    # Parse URN pattern
    match = re.search(r'urn:nir:stato:([^:]+):(\d{4}-\d{2}-\d{2});(\d+)', url)

    if match:
        return {
            'tipo': match.group(1),
            'data': match.group(2),
            'numero': match.group(3)
        }

    return None
```

**Problema**: URN non contiene `dataGU` e `codiceRedazionale` necessari all'API.

**Soluzione 2: Lookup endpoint**

Servirebbero endpoint aggiuntivi per risolvere URN → parametri:

```bash
# Endpoint ipotetico
GET https://api.normattiva.it/t/normattiva.api/bff-mobile/v1/api/v1/atto/lookup?urn=nir:stato:legge:2004-01-09;4

# Risposta
{
  "dataGU": "2004-01-17",
  "codiceRedazionale": "004G0015",
  "numeroGU": "15"
}
```

**Soluzione 3: Hybrid approach** (raccomandato)

Mantenere approccio attuale per estrazione parametri, usare API M2M per il fetch:

```python
# 1. Da URL estrai parametri (approccio attuale)
params = extract_params_from_normattiva_url(url)

# 2. Usa API M2M per fetch dati
data = fetch_via_m2m_api(params['dataGU'], params['codiceRedaz'])
```

### 3. Gestione Autenticazione

**Scenario A: API pubblica (best case)**
- Nessuna autenticazione richiesta
- Implementazione diretta

**Scenario B: API Key**
```python
headers = {
    'X-API-Key': os.getenv('NORMATTIVA_API_KEY'),
    'Content-Type': 'application/json'
}
```

**Implicazioni**:
- User deve registrarsi e ottenere API key
- Documentazione aggiuntiva necessaria
- Gestione errori autenticazione

**Scenario C: OAuth2 (worst case)**
- Flow complesso (client credentials, refresh token)
- Libreria aggiuntiva richiesta (`requests-oauthlib`)
- UX degradata

### 4. Rate Limiting

**Gestione necessaria**:

```python
from time import sleep
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def create_api_session():
    """Crea sessione con retry automatico"""
    session = requests.Session()

    retry = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "POST"]
    )

    adapter = HTTPAdapter(max_retries=retry)
    session.mount('https://', adapter)

    return session

def fetch_with_rate_limit(url, payload, max_retries=3):
    """Fetch con gestione 429 Too Many Requests"""
    session = create_api_session()

    for i in range(max_retries):
        response = session.post(url, json=payload)

        if response.status_code == 429:
            retry_after = int(response.headers.get('Retry-After', 60))
            print(f"Rate limit hit, retry after {retry_after}s...")
            sleep(retry_after)
            continue

        return response

    raise Exception("Max retries exceeded")
```

---

## 🎯 Raccomandazioni

### Fase 1: Esplorazione e Validazione (2-4 ore)

**Obiettivo**: Verificare fattibilità e caratteristiche API M2M

**Tasks**:
1. ✅ **Testare endpoint base**
   ```bash
   curl --location 'https://api.normattiva.it/t/normattiva.api/bff-mobile/v1/api/v1/atto/dettaglio-atto' \
     -H 'Content-Type: application/json' \
     --data '{"dataGU": "2004-01-17", "codiceRedazionale": "004G0015", "versione": 0}'
   ```

2. ✅ **Analizzare struttura risposta**
   - Formato JSON
   - Campi disponibili
   - Presenza XML Akoma Ntoso
   - Metadata aggiuntivi

3. ✅ **Verificare autenticazione**
   - Pubblico o richiede API key?
   - Come ottenere credenziali?
   - Limitazioni per utenti non autenticati?

4. ✅ **Testare rate limiting**
   - Quante richieste/secondo consentite?
   - Header `X-RateLimit-*` presenti?
   - Comportamento con burst requests

5. ✅ **Esplorare altri endpoint**
   - Endpoint di ricerca (`/search`)?
   - Endpoint di lookup URN → parametri?
   - Endpoint lista articoli?
   - Endpoint versioni/modifiche?

6. ✅ **Documentare esempi**
   - Request/response per casi comuni
   - Error codes e handling
   - Edge cases (articolo inesistente, versione invalida)

**Deliverable**:
- Documento `docs/M2M_API_SPECIFICATION.md` con API specs complete
- Script `scripts/test_m2m_api.py` con test esplorativi

---

### Fase 2: Proof of Concept (1-2 giorni)

**Obiettivo**: Implementare wrapper API M2M senza modificare architettura esistente

**Tasks**:
1. Creare modulo `src/normattiva2md/m2m_api.py`

   ```python
   """
   Wrapper per le API Machine-to-Machine di normattiva.it
   """
   import requests
   from typing import Dict, Optional
   from .constants import M2M_API_BASE_URL, DEFAULT_TIMEOUT

   class NormativaM2MClient:
       """Client per API M2M di normattiva.it"""

       def __init__(self, api_key: Optional[str] = None):
           self.base_url = M2M_API_BASE_URL
           self.api_key = api_key
           self.session = requests.Session()

       def fetch_atto_dettaglio(
           self,
           data_gu: str,
           codice_redazionale: str,
           id_articolo: Optional[int] = None,
           versione: int = 0
       ) -> Dict:
           """
           Scarica dettaglio atto tramite API M2M

           Args:
               data_gu: Data GU in formato YYYY-MM-DD
               codice_redazionale: Codice redazionale (es. 004G0015)
               id_articolo: ID articolo specifico (opzionale)
               versione: Versione documento (0=originale)

           Returns:
               Dizionario con risposta API
           """
           payload = {
               "dataGU": data_gu,
               "codiceRedazionale": codice_redazionale,
               "versione": versione
           }

           if id_articolo:
               payload["idArticolo"] = id_articolo

           headers = {'Content-Type': 'application/json'}
           if self.api_key:
               headers['Authorization'] = f'Bearer {self.api_key}'

           response = self.session.post(
               f'{self.base_url}/atto/dettaglio-atto',
               json=payload,
               headers=headers,
               timeout=DEFAULT_TIMEOUT
           )

           response.raise_for_status()
           return response.json()

       def extract_akoma_ntoso(self, api_response: Dict) -> str:
           """Estrae XML Akoma Ntoso dalla risposta API"""
           # Da adattare in base alla struttura effettiva
           return api_response.get('data', {}).get('contenuto', {}).get('xml', '')
   ```

2. Creare script di confronto performance

   ```python
   # scripts/benchmark_m2m.py
   import time
   from normattiva2md.normattiva_api import extract_params_from_normattiva_url, download_akoma_ntoso
   from normattiva2md.m2m_api import NormativaM2MClient

   def benchmark():
       url = "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2004-01-09;4"

       # Metodo attuale
       start = time.time()
       params, session = extract_params_from_normattiva_url(url)
       download_akoma_ntoso(params, '/tmp/test_old.xml', session)
       time_old = time.time() - start

       # Metodo M2M
       start = time.time()
       client = NormativaM2MClient()
       data = client.fetch_atto_dettaglio(params['dataGU'], params['codiceRedaz'])
       xml = client.extract_akoma_ntoso(data)
       time_m2m = time.time() - start

       print(f"Metodo attuale: {time_old:.2f}s")
       print(f"Metodo M2M: {time_m2m:.2f}s")
       print(f"Speedup: {time_old/time_m2m:.2f}x")
   ```

3. Testare integrazione con flusso esistente

**Deliverable**:
- Modulo `m2m_api.py` funzionante
- Benchmark comparativo
- Test suite per M2M client

---

### Fase 3: Integrazione Graduale (2-3 giorni)

**Obiettivo**: Integrare API M2M mantenendo backward compatibility

**Architettura proposta**:

```
┌─────────────────────────────────────────┐
│            CLI / API Entry              │
│         (normattiva2md command)         │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│         URL/File Detection              │
│  (is_normattiva_url, is_file, ...)     │
└────────────────┬────────────────────────┘
                 │
         ┌───────┴────────┐
         ▼                ▼
    ┌─────────┐    ┌──────────────┐
    │  File   │    │ Normattiva   │
    │  Input  │    │     URL      │
    └────┬────┘    └──────┬───────┘
         │                │
         │                ▼
         │         ┌──────────────────────┐
         │         │  Parameter Extractor │ ← Mantiene approccio attuale
         │         │  (HTML scraping)     │   per robustezza
         │         └──────┬───────────────┘
         │                │
         │                ▼
         │         ┌──────────────────────┐
         │         │   Fetcher Strategy   │
         │         │  (M2M API Fallback)  │ ← NUOVO: Scelta dinamica
         │         └──────┬───────────────┘
         │                │
         │          ┌─────┴─────┐
         │          ▼           ▼
         │    ┌──────────┐  ┌─────────────┐
         │    │ M2M API  │  │  HTTP GET   │ ← Fallback se M2M fallisce
         │    │  (new)   │  │ (attuale)   │
         │    └─────┬────┘  └──────┬──────┘
         │          └───────┬──────┘
         ▼                  ▼
    ┌────────────────────────────────┐
    │      XML Akoma Ntoso           │
    └────────────┬───────────────────┘
                 ▼
    ┌────────────────────────────────┐
    │   Markdown Converter           │
    │   (nessuna modifica)           │
    └────────────┬───────────────────┘
                 ▼
    ┌────────────────────────────────┐
    │      Markdown Output           │
    └────────────────────────────────┘
```

**Implementazione**:

```python
# src/normattiva2md/fetcher_strategy.py
from typing import Optional, Tuple
import sys
from .m2m_api import NormativaM2MClient
from .normattiva_api import download_akoma_ntoso

class FetcherStrategy:
    """Strategia di fetch con fallback M2M API → HTTP GET"""

    def __init__(self, prefer_m2m: bool = True, api_key: Optional[str] = None):
        self.prefer_m2m = prefer_m2m
        self.m2m_client = NormativaM2MClient(api_key) if prefer_m2m else None

    def fetch_xml(
        self,
        params: dict,
        output_path: str,
        session=None,
        quiet: bool = False
    ) -> bool:
        """
        Scarica XML con strategia fallback

        1. Tenta M2M API (se abilitata)
        2. Fallback a HTTP GET (metodo attuale)
        """
        # Prova M2M API prima
        if self.prefer_m2m and self.m2m_client:
            try:
                if not quiet:
                    print("⚡ Tentativo download via M2M API...", file=sys.stderr)

                # Converti parametri al formato M2M
                data_gu = params.get('dataGU', '').replace('', '-')  # YYYYMMDD → YYYY-MM-DD
                codice_redaz = params.get('codiceRedaz', '')

                # Fetch via M2M
                response = self.m2m_client.fetch_atto_dettaglio(
                    data_gu=data_gu,
                    codice_redazionale=codice_redaz,
                    versione=0
                )

                # Estrai XML
                xml_content = self.m2m_client.extract_akoma_ntoso(response)

                if xml_content:
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(xml_content)

                    if not quiet:
                        print(f"✅ Download M2M API completato: {output_path}", file=sys.stderr)

                    return True

            except Exception as e:
                if not quiet:
                    print(f"⚠️  M2M API fallita: {e}", file=sys.stderr)
                    print("   Fallback a metodo tradizionale...", file=sys.stderr)

        # Fallback a metodo tradizionale
        return download_akoma_ntoso(params, output_path, session, quiet)
```

**Modifica `api.py`**:

```python
# Aggiungere parametro per abilitare M2M
def convert_url(
    url: str,
    output_md_path: Optional[str] = None,
    keep_xml: bool = False,
    article_filter: Optional[str] = None,
    with_urls: bool = False,
    use_m2m_api: bool = True,  # ← NUOVO parametro
    m2m_api_key: Optional[str] = None,  # ← NUOVO parametro
    quiet: bool = False
) -> Optional[str]:
    """Convert URL to Markdown using M2M API if available"""

    # ... codice esistente ...

    # Usa strategia di fetch
    fetcher = FetcherStrategy(
        prefer_m2m=use_m2m_api,
        api_key=m2m_api_key
    )

    success = fetcher.fetch_xml(params, xml_path, session, quiet)

    # ... resto del codice ...
```

**Aggiornamento CLI**:

```python
# src/normattiva2md/cli.py
@click.option(
    '--use-m2m-api/--no-m2m-api',
    default=True,
    help='Usa API M2M di normattiva.it (default: abilitato con fallback)'
)
@click.option(
    '--m2m-api-key',
    envvar='NORMATTIVA_M2M_API_KEY',
    help='API key per M2M API (opzionale, letto da env NORMATTIVA_M2M_API_KEY)'
)
def main(..., use_m2m_api, m2m_api_key):
    # ...
    convert_url(url, ..., use_m2m_api=use_m2m_api, m2m_api_key=m2m_api_key)
```

**Vantaggi approccio graduale**:
- ✅ Zero breaking changes
- ✅ M2M API opt-in (o opt-out con `--no-m2m-api`)
- ✅ Fallback automatico se M2M fallisce
- ✅ Test A/B facile

**Deliverable**:
- Modulo `fetcher_strategy.py`
- Aggiornamento API e CLI
- Test suite completa
- Documentazione aggiornata

---

### Fase 4: Ottimizzazione e Features Avanzate (3-5 giorni)

**Obiettivo**: Sfruttare appieno le capacità delle API M2M

**Features da implementare**:

1. **Supporto versioni multiple**
   ```python
   normattiva2md --version 1 "URL"  # Versione con prima modifica
   normattiva2md --version all "URL" -o legge.md  # Tutte le versioni
   ```

2. **Diff tra versioni**
   ```python
   normattiva2md --diff 0:1 "URL" -o diff.md  # Diff originale → prima modifica
   ```

3. **Metadata enrichment**
   ```python
   # Front matter YAML arricchito
   ---
   tipo: LEGGE
   numero: 4
   anno: 2004
   alias: Legge Stanca
   articoli_totali: 15
   provvedimenti_attuativi: 12
   modificato: false
   versioni_disponibili: [0, 1, 2]
   ---
   ```

4. **Batch download ottimizzato**
   ```python
   # Sfrutta M2M API per download paralleli
   normattiva2md --batch urls.txt --parallel 5 -o output/
   ```

5. **Caching intelligente**
   ```python
   # Cache risposte M2M API
   from functools import lru_cache

   @lru_cache(maxsize=100)
   def fetch_atto_dettaglio_cached(...):
       return fetch_atto_dettaglio(...)
   ```

---

## 📈 Roadmap Implementazione

### Timeline Proposta

| Fase | Durata | Milestone |
|------|--------|-----------|
| **Fase 1: Esplorazione** | 2-4 ore | Documentazione API completa |
| **Fase 2: POC** | 1-2 giorni | Wrapper M2M funzionante |
| **Fase 3: Integrazione** | 2-3 giorni | Release v2.2.0-beta con M2M |
| **Fase 4: Ottimizzazione** | 3-5 giorni | Release v2.3.0 con features avanzate |

**Totale stimato**: 1-2 settimane di sviluppo

---

### Versioning

**v2.2.0-alpha** (Fase 1+2)
- API M2M esplorazione e POC
- Documentazione tecnica
- Benchmark

**v2.2.0-beta** (Fase 3)
- Integrazione M2M con fallback
- Flag `--use-m2m-api` / `--no-m2m-api`
- Test suite completa

**v2.2.0** (Stabile)
- M2M API abilitata di default
- Fallback HTTP GET automatico
- Documentazione utente

**v2.3.0** (Features avanzate)
- Supporto versioni multiple
- Metadata arricchiti
- Batch processing ottimizzato
- Caching

---

## ⚠️ Rischi e Mitigazioni

| Rischio | Probabilità | Impatto | Mitigazione |
|---------|-------------|---------|-------------|
| **API M2M non pubblica** | Media | Alto | Mantenere approccio attuale come default |
| **Autenticazione complessa** | Media | Medio | Supporto opzionale, documentazione chiara |
| **Rate limiting severo** | Alta | Medio | Caching, retry logic, fallback HTTP |
| **Formato risposta incompatibile** | Bassa | Alto | POC dettagliato prima di implementazione |
| **API instabile/deprecated** | Bassa | Alto | Fallback automatico, monitoring |
| **Breaking changes API** | Media | Medio | Versioning client, test automatizzati |
| **Performance peggiore** | Bassa | Basso | Benchmark comparativo, opt-out disponibile |

**Strategia generale**:
- 🛡️ **Fallback sempre disponibile**: Metodo HTTP GET attuale rimane come safety net
- 🧪 **Testing estensivo**: Ogni fase validata con test automatizzati
- 📚 **Documentazione**: Ogni breaking change documentato

---

## 🎯 Metriche di Successo

### Performance
- [ ] M2M API ≥ 2x più veloce di HTTP GET
- [ ] Latenza < 500ms per richiesta singola
- [ ] Supporto ≥ 10 richieste/secondo

### Qualità
- [ ] Test coverage ≥ 80% per modulo M2M
- [ ] Zero regressioni su casi d'uso esistenti
- [ ] Fallback funziona in 100% dei casi di errore M2M

### User Experience
- [ ] Zero breaking changes per utenti esistenti
- [ ] Documentazione completa con esempi
- [ ] Messaggi errore chiari per problemi autenticazione/rate limit

---

## 💡 Domande Aperte

### Da chiarire nella Fase 1

1. **Autenticazione**:
   - ❓ L'API M2M richiede autenticazione?
   - ❓ Se sì, come si ottiene l'API key?
   - ❓ Esistono limitazioni per utenti non autenticati?

2. **Endpoints disponibili**:
   - ❓ Esiste endpoint `/atto/lookup` per URN → parametri?
   - ❓ Esiste endpoint `/atto/search` per ricerca?
   - ❓ Esiste endpoint `/atto/versioni` per lista versioni?
   - ❓ Esiste endpoint `/articolo/dettaglio` per singoli articoli?

3. **Rate limiting**:
   - ❓ Quante richieste/secondo consentite?
   - ❓ Quota giornaliera?
   - ❓ Header `X-RateLimit-*` disponibili?

4. **Formato dati**:
   - ❓ La risposta include XML Akoma Ntoso completo?
   - ❓ O include già JSON strutturato pronto per conversione?
   - ❓ Quali metadata sono disponibili?

5. **Versioning**:
   - ❓ Come funziona il parametro `versione`?
   - ❓ 0 = originale, 1+ = modifiche successive?
   - ❓ Come si ottiene lista versioni disponibili?

6. **Articoli**:
   - ❓ `idArticolo` è il numero progressivo o l'eId?
   - ❓ Server-side filtering degli articoli funziona?
   - ❓ Risposta include solo l'articolo richiesto?

---

## 📚 Referenze

### Endpoint Identificati

- **Dettaglio Atto**: `POST /t/normattiva.api/bff-mobile/v1/api/v1/atto/dettaglio-atto`
- **Base URL**: `https://api.normattiva.it`

### Documentazione Correlata

- `docs/NORMATTIVA_API.md`: Analisi API HTML-based attuale
- `docs/evaluation.md`: Valutazione generale progetto v2.1.0
- `src/normattiva2md/normattiva_api.py`: Implementazione attuale

### Link Esterni

- **ChatGPT Conversation**: https://chatgpt.com/share/69565cde-c15c-8002-8dab-5126c1c2782b (dettagli API M2M)
- **Normattiva.it**: https://www.normattiva.it
- **Progetto GitHub**: https://github.com/ondata/normattiva_2_md

---

## 🏁 Conclusioni

Le **API Machine-to-Machine di normattiva.it** rappresentano un'opportunità significativa per:

1. ✅ **Migliorare robustezza**: Eliminare HTML scraping fragile
2. ✅ **Aumentare performance**: Ridurre numero richieste HTTP
3. ✅ **Arricchire metadata**: Accesso a dati strutturati
4. ✅ **Semplificare manutenzione**: API contract invece di regex
5. ✅ **Abilitare nuove features**: Versioning, diff, batch processing

**Raccomandazione**:
🚀 **Procedere con l'esplorazione** (Fase 1) per validare la fattibilità e poi implementare gradualmente con approccio **fallback-first** per garantire zero breaking changes.

L'integrazione delle API M2M può portare normattiva2md da **v2.1.0** (production-ready) a **v2.3.0** (enterprise-grade) mantenendo la stabilità e affidabilità del progetto.

---

**Prossimo step**: Eseguire Fase 1 (Esplorazione) e creare documento `M2M_API_SPECIFICATION.md` con tutti i dettagli tecnici.

---

**Data creazione**: 2026-01-01
**Stato**: 📝 Draft - In attesa di validazione tecnica Fase 1
