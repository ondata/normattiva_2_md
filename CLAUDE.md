# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Akoma2MD** is a CLI tool that converts XML documents in Akoma Ntoso format (legal documents from normattiva.it) to readable Markdown. The tool is designed to produce LLM-friendly output for building legal AI bots.

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

### XML Processing

The converter handles Akoma Ntoso 3.0 namespace: `http://docs.oasis-open.org/legaldocml/ns/akn/3.0`

Document structure extraction:

- Title: `//akn:docTitle`
- Preamble: `//akn:preamble`
- Body: `//akn:body` → chapters → sections → articles → paragraphs → lists
- Articles: `//akn:article` with `akn:num` (number) and `akn:heading` (title)
- Legislative modifications: wrapped in `(( ))` from `<ins>` and `<del>` tags

## Common Development Tasks

### Running the converter (auto-detect URL/file)

```bash
# Output to file
python convert_akomantoso.py input.xml output.md
akoma2md input.xml output.md

# Output to stdout (default when -o omitted)
python convert_akomantoso.py input.xml
akoma2md input.xml > output.md
akoma2md -i input.xml

# From normattiva.it URL (auto-detected)
python convert_akomantoso.py "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2022;53" output.md
akoma2md "URL" > output.md
akoma2md -i "URL" -o output.md

# With named arguments
akoma2md -i input.xml -o output.md

# Keep temporary XML from URL
akoma2md "URL" output.md --keep-xml
akoma2md "URL" --keep-xml > output.md
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
pyinstaller --onefile --name akoma2md convert_akomantoso.py
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

## Project Constraints

- **Minimal dependencies**: only `requests` for URL fetching
- Python 3.7+ compatibility
- CLI must support both positional and named arguments
- Auto-detect URL vs file input
- Output defaults to stdout when not specified (file optional)
- Status messages always go to stderr to keep stdout clean for piping
- Output must be LLM-friendly Markdown
