# 🔄 Normattiva2MD - Convertitore Akoma Ntoso in Markdown

[![Versione PyPI](https://img.shields.io/pypi/v/akoma2md.svg)](https://pypi.org/project/akoma2md/)
[![Versione Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://python.org)
[![Licenza](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**Akoma2MD** è uno strumento da riga di comando progettato per convertire documenti XML in formato **Akoma Ntoso** (in particolare le norme pubblicate su `normattiva.it`) in documenti **Markdown** leggibili e ben formattati. L'obiettivo principale è offrire un formato compatto e immediatamente riutilizzabile quando le norme devono essere fornite come contesto a un **Large Language Model (LLM)** o elaborate in pipeline di Intelligenza Artificiale.

## 🎯 Perché Markdown per le norme?

Convertire le norme legali da XML Akoma Ntoso a Markdown offre vantaggi significativi:

- **📝 Ottimizzato per LLM**: Il formato Markdown è ideale per modelli linguistici di grandi dimensioni (Claude, ChatGPT, ecc.), permettendo di fornire intere normative come contesto per analisi, interpretazione e risposta a domande legali
- **🤖 Applicazioni AI**: Facilita la creazione di chatbot legali, assistenti normativi e sistemi di Q&A automatizzati
- **👁️ Leggibilità**: Il testo è immediatamente comprensibile sia da persone che da sistemi automatici, senza tag XML complessi
- **🔍 Ricerca e analisi**: È un formato ottimale per indicizzazione, ricerca semantica e processamento del linguaggio naturale
- **📊 Documentazione**: Si integra con facilità in wiki, basi di conoscenza e piattaforme di documentazione

## 🚀 Caratteristiche

- ✅ **Conversione completa** da XML Akoma Ntoso a Markdown
- ✅ **Supporto URL articolo-specifico** (`~art3`, `~art16bis`, etc.) per estrarre singoli articoli
- ✅ **Gestione degli articoli** con numerazione corretta
- ✅ **Supporto per le modifiche legislative** con evidenziazione `((modifiche))`
- ✅ **Gerarchia book-style intelligente** con parsing strutturato (H1→H2→H3→H4)
- ✅ **Front matter YAML** con metadati completi (URL, dataGU, codiceRedaz, dataVigenza, article)
- ✅ **Machine-to-machine ready** per LLM, RAG e parsing automatico
- ✅ **CLI flessibile** con argomenti posizionali e nominati
- ✅ **Gestione errori robusta** con messaggi informativi
- ✅ **Nessuna dipendenza esterna** per conversione XML→Markdown (solo librerie standard Python)
- ✅ **Ricerca in linguaggio naturale** richiede [Exa AI API](https://exa.ai) per l'integrazione AI

## 📦 Installazione

### Installazione da PyPI (Raccomandato)

Il pacchetto è pubblicato su [PyPI](https://pypi.org/project/akoma2md/) come `akoma2md`.

```bash
# Con uv
uv tool install akoma2md

# Con pip
pip install akoma2md

# Utilizzo (entrambi i comandi funzionano)
normattiva2md input.xml output.md  # Nuovo comando raccomandato
akoma2md input.xml output.md       # Vecchio comando (compatibilità)
```

> **💡 Nota sulla compatibilità**: Entrambi i comandi `normattiva2md` e `akoma2md` funzionano identicamente. Il nuovo nome `normattiva2md` è raccomandato per chiarezza, ma il vecchio comando rimane disponibile per compatibilità durante la transizione.

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

#### Metodo 2: variabile d'ambiente

In alternativa, puoi esportare la variabile manualmente:

```bash
# Configura la variabile d'ambiente con la tua API key
export EXA_API_KEY='your-exa-api-key-here'

# Verifica che sia configurata
echo $EXA_API_KEY
```

### Installazione da sorgenti

```bash
git clone https://github.com/aborruso/normattiva_2_md.git
cd normattiva_2_md
pip install -e .
normattiva2md input.xml output.md  # Nuovo comando raccomandato
# Oppure: akoma2md input.xml output.md  # Vecchio comando (compatibilità)
```

### Esecuzione diretta (senza installazione)

```bash
git clone https://github.com/aborruso/normattiva_2_md.git
cd normattiva_2_md
python convert_akomantoso.py input.xml output.md
```

## 💻 Utilizzo

### Metodo 1: Da URL Normattiva (consigliato)

La CLI riconosce automaticamente gli URL di `normattiva.it` e scarica il documento Akoma Ntoso prima di convertirlo:

```bash
# Conversione diretta URL → Markdown (output su file)
normattiva2md "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2022;53" legge.md

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

### Metodo 3: Ricerca in linguaggio naturale (con Exa AI)

**⚠️ Richiede API key Exa AI configurata**

Prima di utilizzare questa funzionalità, assicurati di aver configurato l'[API key di Exa AI](#configurazione-exa-ai-api-opzionale---per-ricerca-in-linguaggio-naturale).

**Importante**: Per la ricerca in linguaggio naturale devi **sempre usare il flag `-s` o `--search`**:

```bash
# Ricerca in linguaggio naturale (usa SEMPRE -s/--search)
normattiva2md -s "legge stanca" output.md
normattiva2md --search "decreto dignità" > decreto.md

# Output su stdout
normattiva2md -s "codice della strada"
normattiva2md -s "legge stanca" > legge_stanca.md
```

### Esempi pratici

```bash
# Convertire un file XML locale
normattiva2md decreto_82_2005.xml codice_amministrazione_digitale.md

# Con percorsi assoluti
normattiva2md /percorso/documento.xml /percorso/output.md

# Ricerca in linguaggio naturale (richiede Exa AI API - usa SEMPRE -s)
normattiva2md -s "legge stanca" legge_stanca.md
normattiva2md -s "decreto dignità" > decreto.md

# Visualizzare l'aiuto
normattiva2md --help

# Generare link markdown agli articoli citati su normattiva.it
normattiva2md --with-urls input.xml output.md
normattiva2md --with-urls "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2022;53" legge_con_link.md
```

### Opzioni disponibili

```
utilizzo: normattiva2md [-h] [-i INPUT] [-o OUTPUT] [file_input] [file_output]

Converte un file XML Akoma Ntoso in formato Markdown

argomenti posizionali:
  file_input            File XML di input in formato Akoma Ntoso
  file_output           File Markdown di output

opzioni:
   -h, --help            Mostra questo messaggio di aiuto
   -i INPUT, --input INPUT
                         File XML di input in formato Akoma Ntoso
   -o OUTPUT, --output OUTPUT
                         File Markdown di output
   -s SEARCH, --search SEARCH
                         Cerca documento in linguaggio naturale (richiede Exa AI API)
   --with-urls           Genera link markdown agli articoli citati su normattiva.it (solo conversione, nessun download)


argomenti posizionali:
  input                 File XML locale o URL normattiva.it
  output                File Markdown di output (default: stdout)

nota: per ricerca in linguaggio naturale usare -s/--search
```

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
- Nessuna dipendenza esterna per conversione XML→Markdown (solo librerie standard Python)
- [Exa AI API](https://exa.ai) per funzionalità di ricerca in linguaggio naturale

### Configurazione dell'ambiente di sviluppo

```bash
git clone https://github.com/aborruso/normattiva_2_md.git
cd normattiva_2_md
python -m venv venv
source venv/bin/activate  # Su Windows: venv\Scripts\activate
pip install -e .
```

### Creazione di un eseguibile autonomo (opzionale)

Per creare un eseguibile autonomo per uso locale:

```bash
pip install pyinstaller
pyinstaller --onefile --name normattiva2md convert_akomantoso.py
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
# Test di base
python convert_akomantoso.py sample.xml output.md

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

- 🐛 **Segnalazioni di bug**: [pagina delle segnalazioni](https://github.com/aborruso/normattiva_2_md/issues)
- 💡 **Proposte di nuove funzionalità**: [pagina delle segnalazioni](https://github.com/aborruso/normattiva_2_md/issues)

## 🏗️ Stato del progetto

- ✅ **Funzionalità principali**: implementate
- ✅ **Interfaccia a riga di comando**: completa
- ✅ **Gestione errori**: robusta
- 🔄 **Verifiche automatiche**: in evoluzione
- 📚 **Documentazione**: aggiornata

---

**Akoma2MD** - Trasforma i tuoi documenti legali XML in Markdown leggibile! 🚀
