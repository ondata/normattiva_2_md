# Tasks for add-entry-into-force-frontmatter

## Parsing & Data Extraction
- [ ] Identify authoritative XML nodes for the entry-into-force note (preface/authorialNote) and add a helper that searches for text starting with "Entrata in vigore".
- [ ] Implement date parsing that accepts `d/m/yyyy`, `dd/mm/yyyy`, or `yyyy-mm-dd` formats and normalizes them to `YYYYMMDD`.
- [ ] Extend the metadata collection pipeline so the normalized value is stored as `dataEntrataInVigore` when present.

## Front Matter & Docs
- [ ] Update `generate_front_matter` (and any sample outputs) to emit the new field, keeping ordering consistent with existing keys.
- [ ] Document the new metadata key in README/front matter sections so users know what to expect.

## Validation
- [ ] Add/extend conversion tests that assert front matter contains `dataEntrataInVigore` for XML samples with the note and omits it when not available.
