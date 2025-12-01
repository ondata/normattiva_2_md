# Scripts Utility

Questa directory contiene script di supporto per il progetto normattiva_2_md.

## build_distribution.sh

Script per creare distribuzioni complete del convertitore.

**Uso:**
```bash
./scripts/build_distribution.sh
```

**Funzionalità:**
- Pulizia file temporanei
- Verifica dipendenze (Python, PyInstaller)
- Build eseguibile standalone
- Test funzionalità
- Creazione pacchetti di distribuzione (wheel/sdist)
- Generazione istruzioni d'uso

**Output:**
- `dist/akoma2md` - Eseguibile standalone per Linux/WSL
- Pacchetti wheel/tar.gz se richiesto

## download_eurlex.py

Utility per scaricare documenti legali da EUR-Lex in vari formati.

**Uso:**
```bash
python3 scripts/download_eurlex.py <CELEX> [--lang LANG] [--format FORMAT] [--output FILE]
```

**Esempi:**
```bash
# Download formato Formex XML (default)
python3 scripts/download_eurlex.py 32024L1385

# Download in italiano formato XHTML
python3 scripts/download_eurlex.py 32024L1385 --lang IT --format xhtml

# Download con output specifico
python3 scripts/download_eurlex.py 32024L1385 --format fmx4 --output directive.xml
```

**Formati supportati:**
- `fmx4` - Formex XML (strutturato, ottimo per processing)
- `xhtml` - XHTML (formato web)
- `pdfa2a` - PDF/A (versione ufficiale autentica)

**Lingue supportate:**
Tutti i codici lingua EU (BG, ES, CS, DA, DE, ET, EL, EN, FR, GA, HR, IT, LV, LT, HU, MT, NL, PL, PT, RO, SK, SL, FI, SV)

## test_compatibility.sh

Script per testare la compatibilità del convertitore con diverse tipologie di documenti Normattiva.

**Uso:**
```bash
./scripts/test_compatibility.sh
```

**Documenti testati:**
- Decreto Legislativo (es. Codice Amministrazione Digitale)
- Costituzione Italiana
- Codici (Civile, Penale)
- Legge ordinaria
- Regolamento

**Output:**
- Report con percentuale di successo
- Classificazione compatibilità (ottima/buona/limitata)

## test_url_types.sh

Script per testare il fetch da URL Normattiva con diversi tipi di atti normativi.

**Uso:**
```bash
./scripts/test_url_types.sh
```

**Test inclusi:**
1. Legge ordinaria
2. Decreto Legislativo (versione vigente)
3. Decreto Legge
4. Salvataggio solo XML
5. Conversione mantenendo XML

**Output:**
- File convertiti in `test_output/`
- Statistiche: righe e articoli per documento

## Prerequisiti

- Python 3.7+
- Bash shell
- Per `build_distribution.sh`: PyInstaller
- Accesso internet per `download_eurlex.py` e test di URL

## Note

- Gli script sono progettati per essere eseguiti dalla root del progetto
- I test richiedono che l'eseguibile `dist/akoma2md` sia già stato compilato
- `download_eurlex.py` può essere usato indipendentemente dal resto del progetto