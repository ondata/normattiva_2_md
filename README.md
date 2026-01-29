# 🔄 Normattiva2MD - Convertitore Akoma Ntoso in Markdown

[![Versione PyPI](https://img.shields.io/pypi/v/normattiva2md.svg)](https://pypi.org/project/normattiva2md/)
[![Versione Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://python.org)
[![Licenza](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![deepwiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/ondata/normattiva_2_md)

**Normattiva2MD** è uno strumento da riga di comando progettato per convertire documenti XML in formato **Akoma Ntoso** (in particolare le norme pubblicate su `normattiva.it`) in documenti **Markdown** leggibili e ben formattati. L'obiettivo principale è offrire un formato compatto e immediatamente riutilizzabile quando le norme devono essere fornite come contesto a un **Large Language Model (LLM)** o elaborate in pipeline di Intelligenza Artificiale.

---

## ⚠️ Avvertenza legale

**I testi presenti nella banca dati "Normattiva" non hanno carattere di ufficialità.**

**L'unico testo ufficiale e definitivo è quello pubblicato sulla Gazzetta Ufficiale Italiana a mezzo stampa, che prevale in casi di discordanza.**

Gli utenti di questo strumento devono essere consapevoli che i documenti convertiti da normattiva.it sono forniti a scopo informativo e non hanno valore legale ufficiale. Per qualsiasi utilizzo legale o giuridico, consultare sempre la versione ufficiale pubblicata sulla Gazzetta Ufficiale Italiana.

---

👉 Se vuoi una **panoramica eccellente** di normattiva2md leggi [**questo wiki**](https://deepwiki.com/ondata/normattiva_2_md) generato dall'AI.

---

## 🎯 Perché Markdown per le norme?

Convertire le norme legali da XML Akoma Ntoso a Markdown offre vantaggi significativi:

- **📝 Ottimizzato per LLM**: Il formato Markdown è ideale per modelli linguistici di grandi dimensioni (Claude, ChatGPT, ecc.), permettendo di fornire intere normative come contesto per analisi, interpretazione e risposta a domande legali
- **🤖 Applicazioni AI**: Facilita la creazione di chatbot legali, assistenti normativi e sistemi di Q&A automatizzati
- **👁️ Leggibilità**: Il testo è immediatamente comprensibile sia da persone che da sistemi automatici, senza tag XML complessi
- **🔍 Ricerca e analisi**: È un formato ottimale per indicizzazione, ricerca semantica e processamento del linguaggio naturale
- **📊 Documentazione**: Si integra con facilità in wiki, basi di conoscenza e piattaforme di documentazione

## 🚀 Caratteristiche

- ✅ **Conversione completa** da XML Akoma Ntoso a Markdown
- ✅ **Filtro articolo CLI** con flag `--art` (es: `--art 4`, `--art 16bis`) senza modificare URL
- ✅ **Supporto URL articolo-specifico** (`~art3`, `~art16bis`, etc.) per estrarre singoli articoli
- ✅ **Gestione degli articoli** con numerazione corretta
- ✅ **Supporto per le modifiche legislative** con evidenziazione `((modifiche))`
- ✅ **Gerarchia book-style intelligente** con parsing strutturato (H1→H2→H3→H4)
- ✅ **Front matter YAML** con metadati completi (URL, dataGU, codiceRedaz, dataVigenza, article)
- ✅ **Machine-to-machine ready** per LLM, RAG e parsing automatici
- ✅ **CLI flessibile** con argomenti posizionali e nominati
- ✅ **Gestione errori robusta** con messaggi informativi
- ✅ **Dipendenze minime**: requests (URL fetch), rich (output terminalizzato)
- ✅ **Ricerca in linguaggio naturale** richiede [Exa AI API](https://exa.ai) per l'integrazione AI
- ✅ **Modalità debug interattiva** (v2.0.16+) con download guidato e nomi file intelligenti

## 📦 Installazione

### Installazione da PyPI (Raccomandato)

Il pacchetto è pubblicato su [PyPI](https://pypi.org/project/normattiva2md/) come `normattiva2md`.

```bash
# Con uv
uv tool install normattiva2md

# Con pip
pip install normattiva2md

# Utilizzo
normattiva2md input.xml output.md
```

### Configurazione Exa AI API (opzionale - per ricerca in linguaggio naturale)

Per utilizzare la funzionalità di ricerca in linguaggio naturale (`--search`), è necessario configurare una [API key di Exa AI](https://exa.ai).

#### Metodo 1: File .env (Raccomandato)

Crea un file `.env` nella directory del progetto:

```bash
# Crea il file .env
echo 'EXA_API_KEY="your-exa-api-key-here"' > .env

# Verifica che sia configurato
cat .env
```

Il programma caricherà automaticamente l'API key dal file `.env` all'avvio.

### Metodo 2: Variabile d'ambiente (Linux/macOS)

```bash
# Configura la variabile d'ambiente con la tua API key
export EXA_API_KEY='your-exa-api-key-here'

# Verifica che sia configurata
echo $EXA_API_KEY
```

### Metodo 3: Parametro CLI (per uso temporaneo)

```bash
# Passa l'API key direttamente come parametro
normattiva2md -s "legge stanca accessibilità" --exa-api-key "your-exa-api-key" output.md
```

### Installazione da sorgenti

```bash
git clone https://github.com/ondata/normattiva_2_md.git
cd normattiva_2_md
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate  # Windows
pip3 install -e .
normattiva2md input.xml output.md
```

### Esecuzione diretta (senza installazione)

```bash
git clone https://github.com/ondata/normattiva_2_md.git
cd normattiva_2_md
python3 __main__.py input.xml output.md
```


## 🐍 Utilizzo come Libreria Python

> **Nota:** Per vedere esempi pratici e testare la libreria, puoi aprire il notebook Jupyter di esempio: [examples/quickstart.ipynb](examples/quickstart.ipynb)
>
> **📚 Documentazione API completa:** [docs/API_REFERENCE.md](docs/API_REFERENCE.md) - Tutti i metodi, classi, eccezioni con esempi dettagliati.

Oltre al CLI, `normattiva2md` è utilizzabile come libreria Python nei tuoi script o notebook Jupyter:

### Quick Start

```python
from normattiva2md import convert_url, convert_xml, search_law

# Conversione da URL
result = convert_url("https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2004-01-09;4")
print(result.markdown[:500])
print(result.title)
print(result.metadata)
result.save("legge_stanca.md")

# Conversione da file XML locale
result = convert_xml("documento.xml")
result.save("output.md")

# Ricerca in linguaggio naturale (richiede Exa API key)
results = search_law("legge stanca accessibilità")
for r in results:
    print(f"[{r.score:.2f}] {r.title}")
    print(f"  URL: {r.url}")
```

### Classe Converter per Uso Avanzato

```python
from normattiva2md import Converter

# Converter con configurazione persistente
conv = Converter(
    exa_api_key="your-key",  # o usa EXA_API_KEY da .env
    quiet=True
)

# Ricerca e conversione in un passo
result = conv.search_and_convert("decreto dignità")
result.save("decreto_dignita.md")

# Batch processing
urls = [
    "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2004-01-09;4",
    "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2005-03-07;82",
]
for i, url in enumerate(urls):
    result = conv.convert_url(url)
    if result:
        result.save(f"legge_{i+1}.md")
```

### Gestione Errori

```python
from normattiva2md import (
    convert_url,
    InvalidURLError,
    ConversionError,
    APIKeyError,
    Normattiva2MDError,
)

try:
    result = convert_url("https://www.normattiva.it/...")
except InvalidURLError as e:
    print(f"URL non valido: {e}")
except ConversionError as e:
    print(f"Errore conversione: {e}")
except Normattiva2MDError as e:
    print(f"Errore: {e}")

# Gestione errori soft (ritornano None)
result = convert_url(url, article="999")
if result is None:
    print("Articolo non trovato")
```

### Opzioni Avanzate

```python
# Estrai singolo articolo
result = convert_url(url, article="16bis")

# Genera link markdown ai riferimenti
result = convert_url(url, with_urls=True)

# Modalità silenziosa (no logging)
result = convert_url(url, quiet=True)
```

### Oggetti Ritornati

- **`ConversionResult`**: Contiene `markdown`, `metadata`, `url`, `url_xml` + helper come `title`, `data_gu`, `save()`
- **`SearchResult`**: Contiene `url`, `title`, `score`

## 💻 Utilizzo

### Metodo 1: Da URL Normattiva (consigliato)

La CLI riconosce automaticamente gli URL di `normattiva.it` e scarica il documento Akoma Ntoso prima di convertirlo:

```bash
# Conversione diretta URL → Markdown (output su file)
normattiva2md "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2022;53" legge.md

# Forza download via OpenData (quando manca export Akoma)
normattiva2md --opendata "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2022;53" legge.md

# Conversione diretta con output su stdout (utile per pipe)
normattiva2md "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2005-03-07;82"

# Conversione articolo specifico (solo art. 3)
normattiva2md "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto-legge:2018-07-12;87~art3" art3.md

# Conversione articolo con estensione (art. 16-bis)
normattiva2md "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2022;53~art16bis" art16bis.md

# Forza conversione completa anche con URL articolo-specifico
normattiva2md "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto-legge:2018-07-12;87~art3" --completo legge_completa.md
normattiva2md -c "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2022;53~art16bis" legge_completa.md

# Conservare l'XML scaricato
normattiva2md "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2022;53" legge.md --keep-xml
```

### Metodo 2: Da file XML locale

```bash
# Argomenti posizionali (più semplice)
normattiva2md input.xml output.md

# Argomenti nominati
normattiva2md -i input.xml -o output.md
normattiva2md --input input.xml --output output.md
```

### Metodo 2bis: Filtrare un singolo articolo con `--art`

Il flag `--art` consente di estrarre un singolo articolo senza modificare l'URL:

```bash
# Filtrare articolo da file XML locale
normattiva2md --art 4 input.xml output.md
normattiva2md --art 3bis input.xml articolo.md

# Filtrare articolo da URL (più semplice che costruire URL con ~artN)
normattiva2md --art 16bis "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2022;53" art16bis.md

# Il flag --art ha priorità su ~artN nell'URL
normattiva2md --art 3 "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2005-03-07;82~art5" art3.md
# → Mostra art. 3, ignora ~art5 nell'URL

# Combinare con --with-urls per link automatici
normattiva2md --art 4 --with-urls input.xml output.md

# Output su stdout
normattiva2md --art 3 input.xml > articolo.md
```

**Note:**
- Formato articoli: numero + estensione opzionale (es: `4`, `16bis`, `3ter`)
- Case-insensitive: `16BIS` = `16bis`
- Se articolo non trovato: output con solo metadata + warning su stderr
- `--art` ha priorità su `--completo` e `~artN` nell'URL

### Metodo 3: Esportazione provvedimenti attuativi

Esporta i provvedimenti attuativi previsti da una legge in formato CSV:

```bash
# Esporta provvedimenti in CSV (richiede URL normattiva.it)
normattiva2md --provvedimenti "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2024;207" legge.md

# Genera due file:
# - legge.md: conversione markdown della legge
# - 2024_207_provvedimenti.csv: provvedimenti attuativi in formato CSV

# Solo conversione markdown (nessun CSV se non ci sono provvedimenti)
normattiva2md "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:1973;295" legge.md
```

**Formato CSV generato:**
- 7 colonne: `dettagli`, `governo`, `fonte_provvedimento`, `oggetto`, `provvedimento_previsto`, `adozione`, `link_al_provvedimento`
- Encoding: UTF-8
- Nome file: `{anno}_{numero}_provvedimenti.csv`
- Posizione: stessa directory del file markdown

### Metodo 4: Ricerca in linguaggio naturale (con Exa AI)

**⚠️ Richiede API key Exa AI configurata**

Prima di utilizzare questa funzionalità, assicurati di aver configurato l'[API key di Exa AI](#configurazione-exa-ai-api-opzionale---per-ricerca-in-linguaggio-naturale).

**Importante**: Per la ricerca in linguaggio naturale devi **sempre usare il flag `-s` o `--search`**:

```bash
# Ricerca automatica (seleziona automaticamente il miglior risultato)
# Usa --auto-select per evitare i prompt interattivi e usare il primo risultato suggerito.
normattiva2md -s "legge stanca accessibilità" output.md
normattiva2md -s "codice amministrazione digitale" --auto-select > cad.md
normattiva2md --search "decreto dignità" --exa-api-key "your-key" > decreto.md

# Output su stdout
normattiva2md -s "codice della strada"
normattiva2md -s "legge stanca accessibilità" --exa-api-key "your-key" > legge_stanca.md

# Modalità debug interattiva (--debug-search)
# Ti permette di vedere tutti i risultati e scegliere manualmente
normattiva2md -s "legge stanca accessibilità" --debug-search
```

#### 🔍 Modalità Debug Interattiva

La modalità `--debug-search` ti mostra tutti i risultati trovati e ti permette di scegliere manualmente quello desiderato:

```bash
normattiva2md -s "legge stanca accessibilità" --debug-search
```

**Cosa succede:**
1. Mostra il JSON completo della risposta Exa API (per debugging)
2. Lista tutti i risultati con titolo, URL e punteggio di preferenza
3. Ti chiede di selezionare il numero del risultato desiderato
4. **Nuovo in v2.0.16**: Dopo la selezione, ti chiede se vuoi scaricare il documento
5. Suggerisce un nome file in formato snake_case basato sul titolo
6. Puoi accettare (premendo ENTER) o personalizzare il nome
7. Se il file esiste già, chiede conferma prima di sovrascriverlo

**Esempio di sessione interattiva:**

```bash
$ normattiva2md -s "legge stanca accessibilità" --debug-search

🔍 Risultati trovati per: legge stanca
Seleziona il numero del risultato desiderato (1-5), o 0 per annullare:
  [1] DECRETO-LEGGE 7 giugno 2024, n. 73...
      URL: https://www.normattiva.it/...
      Preferenza: -30

  [2] LEGGE 24 maggio 1970, n. 336...
      URL: https://www.normattiva.it/uri-res/N2Ls?...
      Preferenza: 24

  [3] LEGGE 9 gennaio 2004, n. 4...
      URL: https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2004-01-09;4!vig
      Preferenza: 24

Scelta: 3
✅ URL selezionato manualmente: https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2004-01-09;4!vig

📥 Vuoi scaricare questo documento? (s/N): s
📝 Nome file [legge_9_gennaio_2004_n_4.md]:
✅ URL selezionato: https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2004-01-09;4!vig
Rilevato URL normattiva.it: https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2004-01-09;4!vig
...
✅ Conversione completata: legge_9_gennaio_2004_n_4.md
```

**Opzioni nella modalità interattiva:**
- **Conferma download**: Rispondi `s`, `si`, `sì`, `y`, o `yes` per confermare
- **Nome file**: Premi ENTER per accettare il nome suggerito, oppure digita un nome personalizzato
- **Sovrascrittura**: Se il file esiste già, ti chiede conferma prima di sovrascriverlo
- **Annulla**: Rispondi `n` o `N` in qualsiasi momento, oppure premi Ctrl+C

### Esempi pratici

```bash
# Convertire un file XML locale
normattiva2md decreto_82_2005.xml codice_amministrazione_digitale.md

# Con percorsi assoluti
normattiva2md /percorso/documento.xml /percorso/output.md

# Ricerca in linguaggio naturale (richiede Exa AI API - usa SEMPRE -s)
normattiva2md -s "legge stanca accessibilità" legge_stanca.md
normattiva2md -s "decreto dignità" > decreto.md

# Visualizzare l'aiuto
normattiva2md --help

# Generare link markdown agli articoli citati su normattiva.it
normattiva2md --with-urls input.xml output.md
normattiva2md --with-urls "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2022;53" legge_con_link.md

# Esportare provvedimenti attuativi in CSV
normattiva2md --provvedimenti "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2024;207" legge.md
# Genera: legge.md + 2024_207_provvedimenti.csv
```

### Opzioni disponibili

```
utilizzo: normattiva2md [-h] [-v] [-i INPUT] [-o OUTPUT] [-s SEARCH]
                       [--keep-xml] [-q] [-c] [--with-references]
                       [--with-urls] [--debug-search] [--auto-select]
                       [--exa-api-key EXA_API_KEY]
                       [file_input] [file_output]

Converte un file XML Akoma Ntoso in formato Markdown

argomenti posizionali:
  file_input            File XML di input in formato Akoma Ntoso o URL normattiva.it
  file_output           File Markdown di output (default: stdout)

opzioni:
   -h, --help            Mostra questo messaggio di aiuto
   -v, --version         Mostra la versione del programma
   -i INPUT, --input INPUT
                         File XML di input in formato Akoma Ntoso o URL normattiva.it
   -o OUTPUT, --output OUTPUT
                         File Markdown di output (default: stdout)
   -s SEARCH, --search SEARCH
                         Cerca documento in linguaggio naturale (richiede Exa AI API)
  --keep-xml            Mantiene il file XML temporaneo dopo la conversione
  --opendata            Forza download Akoma Ntoso via API OpenData (ZIP AKN)
   -q, --quiet           Modalità silenziosa (nessun output su stderr)
   -c, --completo        Forza download completo anche con URL articolo-specifico
   --with-references     Scarica anche tutti i riferimenti legislativi citati
   --with-urls           Genera link markdown agli articoli citati su normattiva.it
   --provvedimenti       Esporta provvedimenti attuativi in CSV (richiede URL normattiva.it)
   --debug-search        Modalità debug interattiva per la ricerca (mostra tutti i risultati)
   --auto-select         Seleziona automaticamente il miglior risultato (default: True)
   --exa-api-key EXA_API_KEY
                         API key di Exa AI (alternativa a EXA_API_KEY env var)

nota: per ricerca in linguaggio naturale usare -s/--search
```

**Modalità ricerca:**
- **Automatica** (default): `-s "query"` seleziona automaticamente il miglior risultato
- **Interattiva**: `-s "query" --debug-search` mostra tutti i risultati e permette selezione manuale con download interattivo

## 📋 Formato di input supportato

Lo strumento supporta documenti XML in formato **Akoma Ntoso 3.0**, inclusi:

- 📜 **Decreti legislativi**
- 📜 **Leggi**
- 📜 **Decreti legge**
- 📜 **Costituzione**
- 📜 **Regolamenti**
- 📜 **Altri atti normativi**

📖 **Guida agli URL**: Consulta [URL_NORMATTIVA.md](docs/URL_NORMATTIVA.md) per la struttura completa degli URL e esempi pratici.

### Strutture supportate

- ✅ Preamboli e intestazioni
- ✅ Capitoli e sezioni
- ✅ Articoli e commi
- ✅ Liste e definizioni
- ✅ Modifiche legislative evidenziate
- ✅ Note e aggiornamenti

## 📄 Formato di output

Il Markdown generato include:

- **Front matter YAML** con metadati completi (URL, dataGU, codiceRedaz, dataVigenza)
- **Gerarchia heading book-style** ottimizzata per lettura e parsing LLM:
  - `#` (H1) per titolo documento
  - `##` (H2) per Capi (capitoli principali)
  - `###` (H3) per Sezioni
  - `####` (H4) per Articoli
- **Liste puntate** per le definizioni
- **Numerazione corretta** dei commi e articoli
- **Evidenziazione delle modifiche** con `((testo modificato))`
- **Struttura machine-to-machine** ready per LLM e parser automatici

### Esempio di output

```markdown
---
url: https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2005-03-07;82
url_xml: https://www.normattiva.it/do/atto/caricaAKN?dataGU=20050307&codiceRedaz=005G0104&dataVigenza=20251101
dataGU: 20050307
codiceRedaz: 005G0104
dataVigenza: 20251101
---

# Codice dell'amministrazione digitale.

## Capo I - PRINCIPI GENERALI

### Sezione I - Definizioni, finalita' e ambito di applicazione

#### Art. 1. - Definizioni

1. Ai fini del presente codice si intende per:

- a) documento informatico: il documento elettronico...
- b) firma digitale: un particolare tipo di firma...
- c) ((identità digitale)): la rappresentazione informatica...

#### Art. 2. - Finalita' e ambito di applicazione

1. Lo Stato, le Regioni e le autonomie locali...

### Sezione II - ((Carta della cittadinanza digitale))

#### Art. 3. - Diritto all'uso delle tecnologie

1. I cittadini e le imprese hanno il diritto...
```

## 🔧 Sviluppo

### Requisiti

- Python 3.7+
- requests>=2.25.0 (URL fetch)
- rich>=13.0.0,<14.0.0 (output terminalizzato)
- [Exa AI API](https://exa.ai) per funzionalità di ricerca in linguaggio naturale (opzionale)

### Configurazione dell'ambiente di sviluppo

```bash
git clone https://github.com/ondata/normattiva_2_md.git
cd normattiva_2_md
python3 -m venv .venv
source .venv/bin/activate  # Su Windows: .venv\Scripts\activate
pip3 install -e .
```

### Creazione di un eseguibile autonomo (opzionale)

Per creare un eseguibile autonomo per uso locale:

```bash
pip install pyinstaller
python3 -m PyInstaller --onefile --name normattiva2md __main__.py
# L'eseguibile sarà in dist/normattiva2md
```

### Binari precompilati su GitHub

Ogni tag `v*` scatena la GitHub Action [`Build Releases`](.github/workflows/release-binaries.yml) che genera gli eseguibili standalone PyInstaller per **Linux x86_64** e **Windows x86_64**. I pacchetti (`.tar.gz` per Linux, `.zip` per Windows) vengono caricati come asset della release corrispondente e sono disponibili anche come artifact quando il workflow viene avviato manualmente (`workflow_dispatch`). Per pubblicare una nuova release:

1. Aggiorna il numero di versione in `setup.py` (e negli altri file pertinenti, se necessario).
2. Esegui i test locali (`make test`) e documenta eventuali cambiamenti in `LOG.md` e `VERIFICATION.md`.
3. Crea un tag Git `vX.Y.Z` e pushalo su GitHub (`git tag vX.Y.Z && git push origin vX.Y.Z`), oppure avvia manualmente il workflow specificando lo stesso tag già pubblicato.
4. Verifica che la release su GitHub contenga gli asset `normattiva2md-X.Y.Z-linux-x86_64.tar.gz` e `normattiva2md-X.Y.Z-windows-x86_64.zip`.

### Test

```bash
# Test di base (con package installato)
normattiva2md sample.xml output.md

# Test dell'eseguibile
./dist/normattiva2md sample.xml output.md
```

## 📝 Licenza

Questo progetto è distribuito con licenza [MIT](LICENSE).

## 🤝 Contributi

I contributi sono benvenuti! Segui questi passaggi:

1. Esegui un fork del progetto
2. Crea un ramo per la nuova funzionalità (`git checkout -b funzione/descrizione`)
3. Registra le modifiche (`git commit -m 'Descrizione sintetica della modifica'`)
4. Pubblica il ramo (`git push origin funzione/descrizione`)
5. Invia una richiesta di integrazione

## 📞 Supporto

- 🐛 **Segnalazioni di bug**: [pagina delle segnalazioni](https://github.com/ondata/normattiva_2_md/issues)
- 💡 **Proposte di nuove funzionalità**: [pagina delle segnalazioni](https://github.com/ondata/normattiva_2_md/issues)

## 🏗️ Stato del progetto

- ✅ **Funzionalità principali**: implementate
- ✅ **Interfaccia a riga di comando**: completa
- ✅ **Gestione errori**: robusta
- 🔄 **Verifiche automatiche**: in evoluzione
- 📚 **Documentazione**: aggiornata

---

**Akoma2MD** - Trasforma i tuoi documenti legali XML in Markdown leggibile! 🚀
