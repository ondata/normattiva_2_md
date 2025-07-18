# 🔄 Akoma2MD - Convertitore Akoma Ntoso to Markdown

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![CLI Tool](https://img.shields.io/badge/type-CLI%20Tool-orange.svg)](https://github.com/yourusername/akoma2md)

**Akoma2MD** è uno strumento da riga di comando progettato per convertire documenti XML in formato **Akoma Ntoso** (in particolare le norme pubblicate su `normattiva.it`) in documenti **Markdown** leggibili e ben formattati. L'output Markdown è ottimizzato per essere utilizzato come input per Large Language Models (LLM) e sistemi di Intelligenza Artificiale, facilitando la creazione di bot specializzati basati su normative legali.

## 🚀 Caratteristiche

- ✅ **Conversione completa** da XML Akoma Ntoso a Markdown
- ✅ **Gestione degli articoli** con numerazione corretta
- ✅ **Supporto per le modifiche legislative** con evidenziazione `((modifiche))`
- ✅ **Preservazione della struttura gerarchica** (capitoli, sezioni, articoli)
- ✅ **CLI flessibile** con argomenti posizionali e nominati
- ✅ **Gestione errori robusta** con messaggi informativi
- ✅ **Nessuna dipendenza esterna** (solo librerie standard Python)

## 📦 Installazione

### Metodo 1: Eseguibile Standalone (Raccomandato)
Scarica l'eseguibile precompilato dalla sezione [Releases](https://github.com/yourusername/akoma2md/releases):

```bash
# Su Linux/macOS
chmod +x akoma2md
./akoma2md input.xml output.md

# Su Windows
akoma2md.exe input.xml output.md
```

### Metodo 2: Installazione via pip
```bash
pip install akoma2md
akoma2md input.xml output.md
```

### Metodo 3: Installazione da sorgenti
```bash
git clone https://github.com/yourusername/akoma2md.git
cd akoma2md
pip install -e .
akoma2md input.xml output.md
```

### Metodo 4: Esecuzione diretta
```bash
python convert_akomantoso.py input.xml output.md
```

## 💻 Utilizzo

### Sintassi di base
```bash
# Argomenti posizionali (più semplice)
akoma2md input.xml output.md

# Argomenti nominati
akoma2md -i input.xml -o output.md
akoma2md --input input.xml --output output.md
```

### Esempi pratici
```bash
# Convertire un decreto legislativo
akoma2md decreto_82_2005.xml codice_amministrazione_digitale.md

# Con percorsi assoluti
akoma2md /path/to/document.xml /path/to/output.md

# Visualizzare l'help
akoma2md --help
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
- 📜 **Regolamenti**
- 📜 **Altri atti normativi**

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
git clone https://github.com/yourusername/akoma2md.git
cd akoma2md
python -m venv venv
source venv/bin/activate  # Su Windows: venv\Scripts\activate
pip install -e .
```

### Build dell'eseguibile
```bash
pip install pyinstaller
pyinstaller --onefile --name akoma2md convert_akomantoso.py
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

- 🐛 **Bug Reports**: [Issues](https://github.com/yourusername/akoma2md/issues)
- 💡 **Feature Requests**: [Issues](https://github.com/yourusername/akoma2md/issues)
- 📖 **Documentazione**: [Wiki](https://github.com/yourusername/akoma2md/wiki)

## 🏗️ Stato del progetto

- ✅ **Core features**: Implementate
- ✅ **CLI interface**: Completa
- ✅ **Error handling**: Robusta
- 🔄 **Testing**: In corso
- 📚 **Documentation**: Completa

---

**Akoma2MD** - Trasforma i tuoi documenti legali XML in Markdown leggibile! 🚀
