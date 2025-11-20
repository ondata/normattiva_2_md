# Add entry-into-force date to front matter

## Summary
Extend the Markdown front matter to emit the date each law entered into force ("dataEntrataInVigore") whenever the information is present in the Akoma Ntoso XML, so downstream users can quickly filter documents by their effective date without re-parsing the body text.

## Motivation
- The current front matter only reports publication (`dataGU`) and consolidation (`dataVigenza`) dates; analysts still have to skim the annotations in the preface to know when the law actually became effective.
- Entry-into-force metadata already exists inside many Normattiva XML files (e.g., the `authorialNote` in the preface that states "Entrata in vigore del provvedimento: 1/1/2006"). Surfacing it in YAML keeps the front matter a complete summary for AI/RAG pipelines.
- Having the normalized date in metadata simplifies comparisons between laws and allows scripts to skip documents that were not yet active on a given date.

## Impact
- **CLI / Conversion**: parsing code must detect and normalize the entry-into-force date while keeping the field optional when the source XML lacks it.
- **Front matter schema**: YAML gains a new `dataEntrataInVigore` key alongside the existing metadata; documentation and samples need updates.
- **Testing**: add coverage that proves the date is extracted from real XML samples and gracefully skipped when absent.

## Open Questions / Risks
- Need to define the authoritative source: initial scope will rely on the preface `authorialNote` text that starts with "Entrata in vigore". Future iterations can expand to other structures if needed.
- Date strings in the note can be formatted as `d/m/yyyy` or `dd/mm/yyyy`; implementation must normalize them to `YYYYMMDD`, matching other metadata fields.
