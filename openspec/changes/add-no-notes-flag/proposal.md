# Proposal: add-no-notes-flag

## Summary

Aggiunge il flag `--no-notes` alla CLI e il parametro `no_notes` all'API pubblica per escludere dall'output Markdown i blocchi di note `AGGIORNAMENTO` presenti nei documenti Akoma Ntoso.

## Motivazione

Issue #24: chi usa normattiva2md con sistemi RAG (Retrieval-Augmented Generation) segnala che i blocchi `AGGIORNAMENTO (N)` — testo descrittivo delle modifiche storiche, non testo normativo vigente — creano rumore nel retrieval. Serve un modo per ottenere solo il testo della norma corrente.

## Scope

Due capability coinvolte:

| Capability | Tipo di modifica |
|---|---|
| `cli-interface` | MODIFIED — aggiunge `--no-notes` |
| `markdown-conversion` | MODIFIED — aggiunge `no_notes` nelle funzioni di conversione |

## Comportamento atteso

Con `--no-notes`:
- I blocchi `AGGIORNAMENTO (N)` e il testo che li segue all'interno dello stesso elemento `<content>` vengono omessi dall'output.
- I marcatori `(( testo modificato ))` da `<ins>/<del>` **rimangono**: fanno parte del testo vigente, non delle note storiche.

Senza `--no-notes` (default): comportamento invariato — nessuna regressione.

## Architettura della modifica

Il parametro `no_notes` percorre la catena di chiamate esistente:

```
CLI (--no-notes)
  → api.py: convert_url(no_notes=...) / convert_xml(no_notes=...)
    → _convert_xml_internal(no_notes=...)
      → generate_markdown_text(no_notes=...)
        → generate_markdown_fragments(no_notes=...)
          → extract_body_fragments(no_notes=...)
            → process_content_with_paragraphs(no_notes=...)
```

Punto di filtraggio: in `process_content_with_paragraphs()` (markdown_converter.py:222), quando `no_notes=True`, i paragrafi che iniziano con `"AGGIORNAMENTO"` vengono saltati.

## Fuori scope

- Rimozione dei marcatori `(( ))` (potrebbero essere una feature separata futura).
- `convert_akomantoso_to_markdown_improved()` nella CLI legacy — da aggiornare solo se ancora usata direttamente.

## Impatto stimato

- Basso: ~30 righe di codice, nessuna dipendenza esterna.
- Test: aggiungere uno scenario nel test suite esistente con un file XML che contiene blocchi AGGIORNAMENTO.
