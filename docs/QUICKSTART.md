# 🚀 Guida Rapida - Normattiva2MD per Cittadini

Questa guida ti spiega come **leggere le leggi italiane in un formato facilmente comprensibile** usando Normattiva2MD.

## Cos'è e perché serve?

**Normattiva2MD** converte le leggi pubblicate su normattiva.it (in formato XML complesso) in **Markdown**, un formato pulito e leggibile. Perfetto per:

- 📖 Leggere leggi su qualunque dispositivo (computer, tablet, telefono)
- 🔍 Cercare facilmente parole all'interno della legge
- 📋 Copiare gli articoli in documenti (Word, Google Docs, etc.)
- 🤖 Usare le leggi con ChatGPT, Claude o altri assistenti AI
- 📤 Condividere leggi con amici in formato testuale pulito

## 📦 Installazione (super facile!)

### Opzione 1: Se hai Python sul computer

Se hai già Python installato (Windows, Mac, Linux), apri il terminale e scrivi:

```bash
pip install normattiva2md
```

**Non hai Python?** Vai all'[Opzione 2](#opzione-2-usare-leseguibile-stand-alone) più sotto.

### Opzione 2: Usare l'eseguibile stand-alone

Se preferisci evitare Python:

1. Vai a: https://github.com/ondata/normattiva_2_md/releases
2. Scarica il file **zipato** adatto al tuo sistema:
   - **Windows**: `normattiva2md-2.1.4-windows-x86_64.zip`
   - **Mac/Linux**: `normattiva2md-2.1.4-linux-x86_64.tar.gz`
3. Estrai il file e troverai un eseguibile (`.exe` su Windows, nessuna estensione su Mac/Linux)

## 🎯 Utilizzo Base

### Modo 1: Convertire una legge direttamente da URL

È il **modo più semplice**. Prendi l'URL di una legge da normattiva.it e scrivi:

```bash
normattiva2md "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2022;53" legge_moderna.md
```

**Cosa succede?** Scarica la legge n. 53/2022 (Legge per la parità di retribuzione) e la salva nel file `legge_moderna.md`.

### Modo 2: Convertire un file XML locale

Se hai già un file XML di una legge:

```bash
normattiva2md documento.xml documento.md
```

### Modo 3: Cercare una legge per nome

Vuoi cercare una legge ma non hai l'URL? Usa la ricerca AI:

```bash
normattiva2md -s "legge sulla privacy"
```

Il tool cercherà automaticamente e ti mostra i risultati. Puoi scegliere quale vuoi convertire.

---

## 📚 Esempi Pratici

### 1️⃣ Leggere la Costituzione

```bash
normattiva2md "https://www.normattiva.it/uri-res/N2Ls?urn:nir:costituzione:1947-12-22" costituzione.md
```

Ottieni la Costituzione in formato Markdown leggibile!

### 2️⃣ Estrarre solo un articolo specifico

Vuoi solo l'articolo 4 della legge? Aggiungi `--art 4`:

```bash
normattiva2md "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2022;53" --art 4 art4.md
```

### 3️⃣ Leggere su ChatGPT o Claude

Converti una legge, poi copia il contenuto Markdown negli assistenti AI per ottenere spiegazioni, analisi, risposte a domande legali:

```bash
normattiva2md "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2024;207" legge_governo.md
```

Apri `legge_governo.md`, copia il testo, e inalla in ChatGPT con domande tipo:
- "Riassumi questa legge in 3 punti chiave"
- "Quali sono gli articoli che riguardano il lavoro?"
- "Quali sono le sanzioni previste?"

---

## 🎨 Visualizzare i risultati

Dopo la conversione, puoi leggere il file `.md` con:

- **Notepad/Word** (su qualunque computer)
- **GitHub** (carica il file su un repository e lo visualizza formattato automaticamente)
- **Notion, Obsidian, Bear** (markdown editors moderni)
- **VS Code** (editor di codice, ha preview Markdown integrato)

---

## ❓ Domande Frequenti

**D: Come trovo l'URL di una legge su normattiva.it?**

R: Vai su normattiva.it, cerca la legge, e quando la trovi copia l'indirizzo dalla barra del browser. Deve contenere "N2Ls" o "uri-res".

**D: Posso usare una legge convertita in ChatGPT?**

R: Sì! È anzi uno dei principali usi. Basta copiare il Markdown in qualunque assistente AI.

**D: Quale versione della legge mi converte?**

R: La versione **vigente** (attualmente in vigore). Se vuoi una versione passata, aggiungi `!vig=YYYY-MM-DD` all'URL.

**D: Posso modificare il file Markdown dopo la conversione?**

R: Certo! Una volta convertito, è un file di testo normale. Puoi editarlo con qualunque editor.

**D: Serve internet dopo l'installazione?**

R: Sì, per scaricare le leggi da normattiva.it. L'elaborazione avviene locale sul tuo computer.

---

## 🔗 Link Utili

- **Normattiva.it** (fonte ufficiale leggi): https://www.normattiva.it/
- **Repository GitHub**: https://github.com/ondata/normattiva_2_md
- **Pagina PyPI**: https://pypi.org/project/normattiva2md/
- **Report problemi**: https://github.com/ondata/normattiva_2_md/issues

---

## 💡 Suggerimenti

1. **Inizia semplice**: Prova con una legge breve e conosciuta
2. **USA con AI**: La vera potenza emerge quando combini le leggi con ChatGPT/Claude
3. **Condividi**: Hai amici legali, giornalisti o attivisti? Mostra loro come usarlo!
4. **Commenta il tuo uso**: Se lo trovi utile, condividi la tua esperienza su GitHub

---

**Hai domande? Apri un [issue su GitHub](https://github.com/ondata/normattiva_2_md/issues)!**
