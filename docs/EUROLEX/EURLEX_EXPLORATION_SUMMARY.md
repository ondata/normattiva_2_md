# EUR-Lex API Exploration Summary

## Overview

Ho esplorato il sito EUR-Lex (https://eur-lex.europa.eu) per capire come scaricare documenti legislativi europei in formato strutturato.

## Risultati

### 1. Formati Disponibili

EUR-Lex offre i documenti in tre formati principali:

- **Formex XML** (`fmx4`): Formato XML strutturato, ideale per la conversione
- **XHTML** (`xhtml`): Formato HTML semantico per il web  
- **PDF/A** (`pdfa2a`): Versione ufficiale autenticata

### 2. Sistema di Identificazione

I documenti usano tre sistemi:

- **CELEX**: Numero alfanumerico (es. `32024L1385`)
- **ELI**: URI semantico (es. `http://data.europa.eu/eli/dir/2024/1385/oj`)
- **Cellar ID**: UUID interno

### 3. API Scoperte

#### XML Notice API
Endpoint per ottenere i metadati del documento:
```
https://eur-lex.europa.eu/legal-content/{LANG}/TXT/XML/?uri=CELEX:{CELEX}
```

Restituisce un XML con:
- Tutti i formati disponibili
- Tutte le lingue disponibili
- URL di download per ogni combinazione
- Metadati del documento

#### Document Download

Gli URL di download seguono questo pattern:
```
http://publications.europa.eu/resource/oj/{OJ_CODE}.{LANG}.{FORMAT}[.filename.ext]
```

Esempi:
- Formex XML: `L_202401385.ENG.fmx4.OJABA_L_202401385_ENG.fmx4.zip`
- XHTML: `L_202401385.ITA.xhtml.L_202401385IT.html`
- PDF: `L_202401385.ENG.pdfa2a.L_202401385EN.pdfa2a.pdf`

### 4. Codici Lingua

EUR-Lex usa codici a 3 lettere (non ISO 639-1):
- EN → ENG (English)
- IT → ITA (Italian)
- FR → FRA (French)
- DE → DEU (German)
- ES → SPA (Spanish)
- Etc.

## File Creati

### Documentazione

1. **`docs/EURLEX_API.md`** - Documentazione completa dell'API EUR-Lex
   - Endpoint disponibili
   - Esempi di utilizzo
   - Struttura Formex XML
   - Codici lingua completi

2. **`docs/EUR-LEX_INTEGRATION.md`** - Guida all'integrazione
   - Come scaricare documenti
   - Formati disponibili
   - Esempi pratici

### Script

3. **`scripts/download_eurlex.py`** - Script Python per scaricare documenti
   - Supporta tutti i formati (fmx4, xhtml, pdfa2a)
   - Supporta tutte le 24 lingue EU
   - Estrae automaticamente Formex XML da ZIP
   - Mappatura automatica codici lingua

### Dati di Test

4. **`test_data/eurlex_sample.xml`** - Direttiva 2024/1385 in Formex XML (inglese)
5. **`test_data/eurlex_sample_it.xhtml`** - Stessa direttiva in XHTML (italiano)

## Utilizzo

```bash
# Download Formex XML (formato predefinito)
python scripts/download_eurlex.py 32024L1385

# Download in italiano  
python scripts/download_eurlex.py 32024L1385 --lang IT

# Download XHTML
python scripts/download_eurlex.py 32024L1385 --format xhtml --output doc.xhtml

# Mostra formati disponibili
python scripts/download_eurlex.py --list-formats
```

## Prossimi Passi

Per completare l'integrazione EUR-Lex, si potrebbe:

1. **Creare un convertitore Formex → Markdown**
   - Simile a `convert_akomantoso.py`
   - Parser per elementi Formex (ARTICLE, PARAG, ALINEA, LIST, etc.)
   - Generazione Markdown pulito

2. **Aggiungere supporto ELI**
   - Permettere download tramite URI ELI invece di CELEX
   - Parser ELI → CELEX

3. **Integrazione nel tool principale**
   - Estendere `normattiva2md` per supportare EUR-Lex
   - Riconoscimento automatico fonte (Normattiva vs EUR-Lex)

## Struttura Formex XML

Elementi principali trovati:

```xml
<ACT>
  <TITLE>           <-- Campione delle particelle TARES con superficie Titolo documento -->
  <PREAMBLE>        <-- Campione delle particelle TARES con superficie Preambolo -->
    <GR.CONSID>     <-- Campione delle particelle TARES con superficie Considerando -->
      <CONSID>      <-- Campione delle particelle TARES con superficie Singolo considerando -->
  <ENACTING.TERMS>  <-- Campione delle particelle TARES con superficie Parte dispositiva -->
    <ARTICLE>       <-- Campione delle particelle TARES con superficie Articolo -->
      <TI.ART>      <-- Campione delle particelle TARES con superficie Numero articolo -->
      <STI.ART>     <-- Campione delle particelle TARES con superficie Titolo articolo -->
      <PARAG>       <-- Campione delle particelle TARES con superficie Paragrafo numerato -->
        <NO.PARAG>  <-- Campione delle particelle TARES con superficie Numero paragrafo -->
        <ALINEA>    <-- Campione delle particelle TARES con superficie Testo paragrafo -->
      <LIST>        <-- Campione delle particelle TARES con superficie Lista -->
        <ITEM>      <-- Campione delle particelle TARES con superficie Elemento lista -->
```

## Test Effettuati

✅ Download XML Notice per CELEX 32024L1385  
✅ Parsing XML Notice per estrarre URL  
✅ Mappatura codici lingua (EN → ENG)  
✅ Download Formex XML (inglese)  
✅ Estrazione ZIP e parsing XML  
✅ Download XHTML (italiano)  
✅ Verifica struttura Formex

## Conclusioni

L'API EUR-Lex è ben strutturata e documentabile. Il formato Formex XML è molto simile ad Akoma Ntoso nella struttura gerarchica (articoli, paragrafi, liste), quindi la conversione a Markdown dovrebbe essere relativamente semplice riutilizzando l'approccio già implementato per Normattiva.

La differenza principale è nella nomenclatura degli elementi XML:
- Akoma Ntoso: `<article>`, `<paragraph>`, `<list>`
- Formex: `<ARTICLE>`, `<PARAG>`, `<LIST>`

Ma la logica di conversione rimane la stessa.
