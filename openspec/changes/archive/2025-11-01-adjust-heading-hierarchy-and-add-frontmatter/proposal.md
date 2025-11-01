## Why
The current Markdown output structure uses inconsistent heading levels that don't follow standard document hierarchy conventions. Users want a cleaner structure with the law title prominently displayed at the top and metadata information available in front matter format for better document processing and LLM consumption.

## What Changes
- Lower all existing headings by one level (H1 → H2, H2 → H3, etc.)
- Add the law title as H1 at the beginning of the document
- Add YAML front matter with metadata fields: URL, URL_XML, dataGU, codiceRedaz, dataVigenza
- Extract metadata from XML when available, fall back to URL parameters when processing from normattiva.it URLs

## Impact
- Affected specs: markdown-conversion (new capability)
- Affected code: convert_akomantoso.py (heading generation functions, main conversion flow)
- Breaking change: Output format changes, existing consumers may need to adjust heading level expectations