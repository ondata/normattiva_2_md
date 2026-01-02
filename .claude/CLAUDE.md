# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**normattiva2md** is a CLI tool that converts XML documents in Akoma Ntoso format (legal documents from normattiva.it) to readable Markdown. The tool is designed to produce LLM-friendly output for building legal AI bots.

## Core Architecture

### Main Components

- `convert_akomantoso.py`: Unified CLI tool (requires `requests`)
  - Entry point: `main()` function with auto-detect URL/file
  - URL support: `is_normattiva_url()`, `extract_params_from_normattiva_url()`, `download_akoma_ntoso()`
  - Core conversion: `convert_akomantoso_to_markdown_improved(xml_path, md_path=None)` - outputs to stdout if md_path is None
  - Text extraction: `clean_text_content(element)` handles inline formatting, refs, and modifications
  - Article processing: `process_article(article_element, markdown_list, ns)` handles paragraphs and lists
  - Status messages: routed to stderr when outputting markdown to stdout

- `fetch_normattiva.py`: Alternative fetcher (requires `tulit` library)
  - Downloads documents from normattiva.it API
  - Requires specific parameters (not URL-based)
  - Converts to Markdown or JSON
  - Entry point: `main()` with argparse CLI

- `setup.py`: Package configuration for PyPI distribution

- `provvedimenti_api.py`: Provvedimenti attuativi export module
  - Entry point: `write_provvedimenti_csv(url, output_md_path)` orchestrates the full workflow
  - URL parsing: `extract_law_params_from_url(url)` extracts anno/numero from normattiva.it URLs
  - Data fetching: `fetch_all_provvedimenti(numero, anno)` handles pagination from programmagoverno.gov.it
  - HTML parsing: `parse_provvedimenti_html(html_content)` extracts structured data with regex
  - CSV export: `export_provvedimenti_csv(data, csv_path)` writes UTF-8 CSV with 7 columns
  - User interaction: `prompt_overwrite(file_path)` asks confirmation before overwriting

### XML Processing

The converter handles Akoma Ntoso 3.0 namespace: `http://docs.oasis-open.org/legaldocml/ns/akn/3.0`

Document structure extraction:

- Title: `//akn:docTitle`
- Preamble: `//akn:preamble`
- Body: `//akn:body` → chapters → sections → articles → paragraphs → lists
- Articles: `//akn:article` with `akn:num` (number) and `akn:heading` (title)
- Legislative modifications: wrapped in `(( ))` from `<ins>` and `<del>` tags

Article filtering:

- `construct_article_eid(user_input)`: Converts user-friendly input (e.g., "4", "16bis") to Akoma eId format (e.g., "art_4", "art_16-bis")
- `filter_xml_to_article(root, article_eid, ns)`: Extracts single article from XML document
- Supports article extensions: bis, ter, quater, quinquies, etc. with hyphen in eId

## Common Development Tasks

### Running the converter (auto-detect URL/file)

```bash
# Output to file
python convert_akomantoso.py input.xml output.md
normattiva2md input.xml output.md

# Output to stdout (default when -o omitted)
python convert_akomantoso.py input.xml
normattiva2md input.xml > output.md
normattiva2md -i input.xml

# From normattiva.it URL (auto-detected)
python convert_akomantoso.py "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2022;53" output.md
normattiva2md "URL" > output.md
normattiva2md -i "URL" -o output.md

# With named arguments
normattiva2md -i input.xml -o output.md

# Keep temporary XML from URL
normattiva2md "URL" output.md --keep-xml
normattiva2md "URL" --keep-xml > output.md

# Filter single article with --art flag
normattiva2md --art 4 input.xml output.md
normattiva2md --art 16bis "URL" output.md
normattiva2md --art 3 --with-urls input.xml > output.md
# --art overrides URL ~artN: --art 2 "URL~art5" → extracts art. 2

# Export provvedimenti attuativi to CSV
normattiva2md --provvedimenti "URL" output.md
normattiva2md --provvedimenti "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2024;207" legge.md
# Generates: legge.md + 2024_207_provvedimenti.csv
```

### Alternative: Fetching with specific parameters

```bash
# Requires: pip install tulit
python fetch_normattiva.py --dataGU YYYYMMDD --codiceRedaz CODE --dataVigenza YYYYMMDD --output file.md --format markdown
```

### Testing

```bash
# Basic test with sample data
python convert_akomantoso.py test_data/20050516_005G0104_VIGENZA_20250130.xml test_output.md
```

### Building executable

```bash
pip install pyinstaller
pyinstaller --onefile --name normattiva2md convert_akomantoso.py
```

### Package installation

```bash
# CLI tool installation (recommended)
uv tool install .

# Development mode (requires venv)
pip install -e .

# From source (requires venv)
pip install .
```

## Key Design Decisions

### Markdown Output Format

- Articles: `# Art. X - Title`
- Chapters: `## Chapter Title`
- Sections: `### Section Title`
- Numbered paragraphs: `1. Text content`
- Lists: Markdown bullet lists with `- a) item text`
- Legislative changes: Wrapped in `((modified text))`

### Text Cleaning

- Removes excessive whitespace and indentation
- Preserves inline formatting (bold, emphasis)
- Extracts text from `<ref>` tags
- Prevents double-wrapping of `(( ))` in modifications
- Filters out horizontal separator lines (`----`)

## Development Environment

**IMPORTANT**: Always follow procedures in `@/DEVELOPMENT.md` for:
- Creating and activating virtual environment (`.venv`)
- Running tests
- Building executables
- Packaging and releases

**Why**: The virtual environment isolates dependencies and prevents binary bloat from global packages.

## Project Constraints

- **Minimal dependencies**: only `requests` for URL fetching
- Python 3.7+ compatibility
- CLI must support both positional and named arguments
- Auto-detect URL vs file input
- Output defaults to stdout when not specified (file optional)
- Status messages always go to stderr to keep stdout clean for piping
- Output must be LLM-friendly Markdown
