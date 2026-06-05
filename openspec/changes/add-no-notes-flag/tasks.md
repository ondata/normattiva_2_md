# Tasks: add-no-notes-flag

## Implementation

- [ ] **1. markdown_converter.py** — aggiunge `no_notes=False` a `process_content_with_paragraphs()`: quando `no_notes=True`, salta il paragrafo che inizia con `"AGGIORNAMENTO"` e tutti quelli che lo seguono nello stesso `<content>` (l'intero blocco nota)
- [ ] **2. markdown_converter.py** — propaga `no_notes` attraverso la catena: `generate_markdown_text` → `generate_markdown_fragments` → `extract_body_fragments` → `process_body_element` → `process_article` → `process_content_with_paragraphs`
- [ ] **3. api.py** — aggiunge `no_notes=False` a `convert_url()`, `convert_xml()`, `_convert_xml_internal()`; passa il parametro a `generate_markdown_text()`
- [ ] **4. cli.py** — aggiunge `--no-notes` ad argparse; passa `no_notes` alla funzione di conversione; aggiorna la tabella help Rich

## Validation

- [ ] **5. Test** — aggiunge test in `tests/` con file XML contenente blocchi AGGIORNAMENTO: verifica che con `no_notes=True` siano assenti nell'output e con `no_notes=False` siano presenti
- [ ] **6. Smoke test CLI** — `normattiva2md --no-notes test_data/20050516_005G0104_VIGENZA_20250130.xml` non deve contenere "AGGIORNAMENTO" nell'output

## Notes

- Task 1 e 2 sono dipendenti (fare in sequenza).
- Task 3 dipende da 1+2.
- Task 4 dipende da 3.
- Task 5 e 6 parallelizzabili dopo task 4.
