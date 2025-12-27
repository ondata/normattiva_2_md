# Piano di Refactoring: Modularizzazione di `convert_akomantoso.py`

## ✅ COMPLETATO - 3 Dicembre 2025

Il refactoring è stato completato con successo. Lo script monolitico `convert_akomantoso.py` (2300+ righe) è stato trasformato in un pacchetto Python modulare (`src/normattiva2md`), migliorando la manutenibilità, la testabilità e facilitando l'espansione futura.

## Obiettivo
Trasformare lo script monolitico `convert_akomantoso.py` (2300+ righe) in un pacchetto Python modulare (`src/normattiva2md`), per migliorare la manutenibilità, la testabilità e facilitare l'espansione futura (es. integrazione EurLex).

## Struttura Target (`src/normattiva2md/`)

*   `__init__.py`: Setup del package.
*   `constants.py`: Costanti globali (namespace, domini, versioni).
*   `utils.py`: Funzioni di utilità generiche (path, env, stringhe).
*   `normattiva_api.py`: Interazione con il sito Normattiva (validazione URL, scraping parametri, download).
*   `exa_api.py`: Integrazione con Exa AI per la ricerca.
*   `xml_parser.py`: Estrazione metadati e analisi XML.
*   `markdown_converter.py`: Logica di conversione Akoma Ntoso -> Markdown.
*   `akoma_utils.py`: Funzioni specifiche per URI e riferimenti Akoma Ntoso.
*   `multi_document.py`: Gestione download ricorsivo e riferimenti incrociati.
*   `cli.py`: Entry point e parsing argomenti.

## Roadmap dei Task

### Fase 1: Fondamenta (Setup e Base)
- [x] **Task 1.1**: Creare struttura directory `src/normattiva2md` e file `__init__.py` vuoti.
- [x] **Task 1.2**: Estrarre `constants.py`. Spostare:
    - `AKN_NAMESPACE`, `GU_NAMESPACE`, `ELI_NAMESPACE`
    - `ALLOWED_DOMAINS`, `MAX_FILE_SIZE_MB`, `MAX_FILE_SIZE_BYTES`
    - `DEFAULT_TIMEOUT`, `VERSION`
- [x] **Task 1.3**: Estrarre `utils.py`. Spostare:
    - `load_env_file()`
    - `sanitize_output_path()`
    - `generate_snake_case_filename()`

### Fase 2: Logica Core (Akoma Ntoso e Markdown)
- [x] **Task 2.1**: Estrarre `akoma_utils.py`. Spostare:
    - `akoma_uri_to_normattiva_url()`
    - `parse_article_reference()`
    - `extract_akoma_uris_from_xml()`
    - `extract_cited_laws()`
- [x] **Task 2.2**: Estrarre `xml_parser.py`. Spostare:
    - `extract_metadata_from_xml()`
    - `filter_xml_to_article()`
    - `build_permanent_url()`
- [x] **Task 2.3**: Estrarre `markdown_converter.py` (la parte più grossa). Spostare:
    - `convert_akomantoso_to_markdown_improved()`
    - `generate_markdown_fragments()`
    - `process_*` functions (chapter, article, table, etc.)
    - `clean_text_content()`
    - `parse_chapter_heading()`, `format_heading_with_separator()`
    - `generate_front_matter()`

### Fase 3: Networking e API
- [x] **Task 3.1**: Estrarre `normattiva_api.py`. Spostare:
    - `validate_normattiva_url()`
    - `is_normattiva_url()`, `is_normattiva_export_url()`
    - `extract_params_from_normattiva_url()`
    - `download_akoma_ntoso()`
- [x] **Task 3.2**: Estrarre `exa_api.py`. Spostare:
    - `lookup_normattiva_url()`

### Fase 4: Orchestration e CLI
- [x] **Task 4.1**: Estrarre `multi_document.py`. Spostare:
    - `convert_with_references()`
    - `create_index_file()`
    - `build_cross_references_mapping_from_urls()`
- [x] **Task 4.2**: Creare `cli.py`. Spostare:
    - `main()`
    - Aggiornare gli import per usare i nuovi moduli.
- [x] **Task 4.3**: Creare entry point script nella root (`normattiva2md`) che importa ed esegue `src.normattiva2md.cli.main()`.

### Fase 5: Cleanup e Verifica
- [x] **Task 5.1**: Aggiornare i test esistenti (`tests/test_convert.py`) per importare dai nuovi moduli.
- [x] **Task 5.2**: Eseguire i test per verificare che nulla sia rotto.
- [x] **Task 5.3**: Rimuovere il vecchio `convert_akomantoso.py`.
- [x] **Task 5.4**: Aggiornare `setup.py` o `pyproject.toml` per riflettere la nuova struttura del package.

## Risultati del Testing

### Test Automatici
- ✅ 29 unit test passati senza errori
- ✅ Conversione XML → Markdown verificata (1648+ righe)
- ✅ Flag `--version` e `--help` funzionanti

### Test Funzionali Manuali
- ✅ Conversione da file XML locale
- ✅ Ricerca in linguaggio naturale con auto-select
- ✅ Ricerca interattiva con selezione manuale
- ✅ Download da URL normattiva.it
- ✅ Generazione file output con nomi personalizzati
- ✅ Download ricorsivo con `--with-references` (11/12 leggi citate scaricate)

### Fix Applicati Durante il Testing
1. Stringa multilinea non chiusa nell'epilog di `cli.py` (riga 70)
2. Import mancante di `load_env_file` in `cli.py`

## Note
- Ogni spostamento di funzione ha incluso l'aggiornamento degli import necessari nel file di destinazione.
- Il vecchio `convert_akomantoso.py` è stato rimosso dopo aver verificato che tutti i moduli funzionassero correttamente.
