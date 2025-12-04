# Add Article Filter Flag

## Why
Users currently need to manually construct URLs with `~artN` syntax to filter a specific article from normattiva.it documents. This requires knowledge of the URL structure and makes it harder to work with local XML files. A dedicated `--art` flag simplifies article filtering and works consistently with both URLs and local files.

## What Changes
- Add `--art` CLI flag accepting article numbers (e.g., `4`, `16bis`, `3ter`)
- Filter XML content to show only the specified article in markdown output
- Override any existing `~artN` in URL when `--art` is provided
- Support article extensions (bis, ter, quater, quinquies, etc.)
- Work with both normattiva.it URLs and local XML files

## Impact
- Affected specs: `cli-interface`, `markdown-conversion`
- Affected code:
  - `src/normattiva2md/cli.py` - add `--art` argument
  - `src/normattiva2md/markdown_converter.py` - apply article filtering
  - `src/normattiva2md/xml_parser.py` - use existing `filter_xml_to_article()` function
- No breaking changes
- Backward compatible (optional parameter)
