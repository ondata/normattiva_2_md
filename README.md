# 🔄 Akoma2MD - Convertitore Akoma Ntoso to Markdown

[![PyPI version](https://img.shields.io/pypi/v/akoma2md.svg)](https://pypi.org/project/akoma2md/)
[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Downloads](https://img.shields.io/pypi/dm/akoma2md.svg)](https://pypi.org/project/akoma2md/)

**Akoma2MD** è uno strumento da riga di comando progettato per convertire documenti XML in formato **Akoma Ntoso** (in particolare le norme pubblicate su `normattiva.it`) in documenti **Markdown** leggibili e ben formattati.

## 🎯 Perché Markdown per le norme?

Convertire le norme legali da XML Akoma Ntoso a Markdown offre vantaggi significativi:

- **📝 LLM-friendly**: Il formato Markdown è ideale per Large Language Models (Claude, ChatGPT, ecc.), permettendo di passare intere normative come contesto per analisi, interpretazione e risposta a domande legali
- **🤖 AI Applications**: Facilita la creazione di chatbot legali, assistenti normativi e sistemi di Q&A automatizzati
- **👁️ Leggibilità**: Il testo è immediatamente leggibile sia da umani che da macchine, senza tag XML complessi
- **🔍 Ricerca e analisi**: Formato ottimale per indicizzazione, ricerca semantica e processamento del linguaggio naturale
- **📊 Documentazione**: Facile integrazione in wiki, knowledge base e sistemi di documentazione

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

Converti direttamente da un URL di normattiva.it:

```bash
# Conversione diretta URL → Markdown
python fetch_from_url.py "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2022;53" -o legge.md

# Salva solo il file XML Akoma Ntoso
python fetch_from_url.py "URL_NORMATTIVA" --xml-only -o documento.xml

# Mantieni il file XML dopo la conversione
python fetch_from_url.py "URL_NORMATTIVA" -o legge.md --keep-xml
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
# Convertire da URL normattiva
python fetch_from_url.py "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2005-03-07;82" -o cad.md

# Convertire un file XML locale
akoma2md decreto_82_2005.xml codice_amministrazione_digitale.md

# Con percorsi assoluti
akoma2md /path/to/document.xml /path/to/output.md

# Visualizzare l'help
akoma2md --help
python fetch_from_url.py --help
```

### Opzioni disponibili

```
usage: akoma2md [-h] [-i INPUT] [-o OUTPUT] [input_file] [output_file]

Converte un file XML Akoma Ntoso in formato Markdown

positional arguments:
  input_file            File XML di input in formato Akoma Ntoso
  output_file           File Markdown di output

options:
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

### Setup ambiente di sviluppo

```bash
git clone https://github.com/aborruso/normattiva_2_md.git
cd normattiva_2_md
python -m venv venv
source venv/bin/activate  # Su Windows: venv\Scripts\activate
pip install -e .
```

### Build eseguibile standalone (opzionale)

Per creare un eseguibile standalone per uso locale:

```bash
pip install pyinstaller
pyinstaller --onefile --name akoma2md convert_akomantoso.py
# L'eseguibile sarà in dist/akoma2md
```

### Test

```bash
# Test di base
python convert_akomantoso.py sample.xml output.md

# Test dell'eseguibile
./dist/akoma2md sample.xml output.md
```

## 📝 Licenza

Questo progetto è rilasciato sotto licenza [MIT](LICENSE).

## 🤝 Contributi

I contributi sono benvenuti! Per favore:

1. Fai un fork del progetto
2. Crea un branch per la tua feature (`git checkout -b feature/AmazingFeature`)
3. Committa le tue modifiche (`git commit -m 'Add some AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Apri una Pull Request

## 📞 Supporto

- 🐛 **Bug Reports**: [Issues](https://github.com/aborruso/normattiva_2_md/issues)
- 💡 **Feature Requests**: [Issues](https://github.com/aborruso/normattiva_2_md/issues)
- 📖 **Documentazione**: [Wiki](https://github.com/aborruso/normattiva_2_md/wiki)

## 🏗️ Stato del progetto

- ✅ **Core features**: Implementate
- ✅ **CLI interface**: Completa
- ✅ **Error handling**: Robusta
- 🔄 **Testing**: In corso
- 📚 **Documentation**: Completa

---

**Akoma2MD** - Trasforma i tuoi documenti legali XML in Markdown leggibile! 🚀