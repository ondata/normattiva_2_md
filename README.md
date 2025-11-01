# 🔄 Akoma2MD - Convertitore Akoma Ntoso in Markdown

[![Versione PyPI](https://img.shields.io/pypi/v/akoma2md.svg)](https://pypi.org/project/akoma2md/)
[![Versione Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://python.org)
[![Licenza](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Download](https://img.shields.io/pypi/dm/akoma2md.svg)](https://pypi.org/project/akoma2md/)

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
- ✅ **Gestione degli articoli** con numerazione corretta
- ✅ **Supporto per le modifiche legislative** con evidenziazione `((modifiche))`
- ✅ **Preservazione della struttura gerarchica** (capitoli, sezioni, articoli)
- ✅ **CLI flessibile** con argomenti posizionali e nominati
- ✅ **Gestione errori robusta** con messaggi informativi
- ✅ **Nessuna dipendenza esterna** (solo librerie standard Python)

## 📦 Installazione

### Installazione da PyPI (Raccomandato)

Il pacchetto è pubblicato su [PyPI](https://pypi.org/project/akoma2md/).

```bash
# Con uv
uv tool install akoma2md

# Con pip
pip install akoma2md

# Utilizzo
akoma2md input.xml output.md
```

### Installazione da sorgenti

```bash
git clone https://github.com/aborruso/normattiva_2_md.git
cd normattiva_2_md
pip install -e .
akoma2md input.xml output.md
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
akoma2md "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2022;53" legge.md

# Conversione diretta con output su stdout (utile per pipe)
akoma2md "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2005-03-07;82"

# Conservare l'XML scaricato
akoma2md "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2022;53" legge.md --keep-xml
```

### Metodo 2: Da file XML locale

```bash
# Argomenti posizionali (più semplice)
akoma2md input.xml output.md

# Argomenti nominati
akoma2md -i input.xml -o output.md
akoma2md --input input.xml --output output.md
```

### Esempi pratici

```bash
# Convertire un file XML locale
akoma2md decreto_82_2005.xml codice_amministrazione_digitale.md

# Con percorsi assoluti
akoma2md /percorso/documento.xml /percorso/output.md

# Visualizzare l'aiuto
akoma2md --help
```

### Opzioni disponibili

```
utilizzo: akoma2md [-h] [-i INPUT] [-o OUTPUT] [file_input] [file_output]

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
```

## 📋 Formato di input supportato

Lo strumento supporta documenti XML in formato **Akoma Ntoso 3.0**, inclusi:

- 📜 **Decreti legislativi**
- 📜 **Leggi**
- 📜 **Decreti legge**
- 📜 **Costituzione**
- 📜 **Regolamenti**
- 📜 **Altri atti normativi**

📖 **Guida agli URL**: Consulta [URL_NORMATTIVA.md](URL_NORMATTIVA.md) per la struttura completa degli URL e esempi pratici.

### Strutture supportate

- ✅ Preamboli e intestazioni
- ✅ Capitoli e sezioni
- ✅ Articoli e commi
- ✅ Liste e definizioni
- ✅ Modifiche legislative evidenziate
- ✅ Note e aggiornamenti

## 📄 Formato di output

Il Markdown generato include:

- **Intestazioni gerarchiche** (`#`, `##`, `###`)
- **Liste puntate** per le definizioni
- **Numerazione corretta** dei commi e articoli
- **Evidenziazione delle modifiche** con `((testo modificato))`
- **Struttura pulita e leggibile**

### Esempio di output

```markdown
# Art. 1 - Definizioni

1. Ai fini del presente codice si intende per:

- a) documento informatico: il documento elettronico...
- b) firma digitale: un particolare tipo di firma...
- c) ((identità digitale)): la rappresentazione informatica...

# Art. 2 - Finalità e ambito di applicazione

1. Lo Stato, le Regioni e le autonomie locali...
```

## 🔧 Sviluppo

### Requisiti

- Python 3.7+
- Nessuna dipendenza esterna

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
pyinstaller --onefile --name akoma2md convert_akomantoso.py
# L'eseguibile sarà in dist/akoma2md
```

### Binari precompilati su GitHub

Ogni tag `v*` scatena la GitHub Action [`Build Releases`](.github/workflows/release-binaries.yml) che genera gli eseguibili standalone PyInstaller per **Linux x86_64** e **Windows x86_64**. I pacchetti (`.tar.gz` per Linux, `.zip` per Windows) vengono caricati come asset della release corrispondente e sono disponibili anche come artifact quando il workflow viene avviato manualmente (`workflow_dispatch`). Per pubblicare una nuova release:

1. Aggiorna il numero di versione in `setup.py` (e negli altri file pertinenti, se necessario).
2. Esegui i test locali (`make test`) e documenta eventuali cambiamenti in `LOG.md` e `VERIFICATION.md`.
3. Crea un tag Git `vX.Y.Z` e pushalo su GitHub (`git tag vX.Y.Z && git push origin vX.Y.Z`), oppure avvia manualmente il workflow specificando lo stesso tag già pubblicato.
4. Verifica che la release su GitHub contenga gli asset `akoma2md-X.Y.Z-linux-x86_64.tar.gz` e `akoma2md-X.Y.Z-windows-x86_64.zip`.

### Test

```bash
# Test di base
python convert_akomantoso.py sample.xml output.md

# Test dell'eseguibile
./dist/akoma2md sample.xml output.md
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
