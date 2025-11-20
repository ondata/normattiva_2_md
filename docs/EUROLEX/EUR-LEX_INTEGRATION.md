# EUR-Lex Integration

## Summary

EUR-Lex è il portale ufficiale della legislazione europea. Questo documento descrive come scaricare e convertire documenti EUR-Lex in Markdown.

## Formats Available

EUR-Lex provides documents in three main formats:

1. **Formex XML** (`.fmx.xml`) - Best for conversion to Markdown
   - Structured XML format used by EU Publications Office
   - Contains semantic markup for articles, paragraphs, lists, etc.
   - Downloaded as ZIP file containing XML

2. **XHTML** (`.xhtml`) - Web-ready format
   - HTML with semantic markup
   - Can be used for conversion but less structured than Formex

3. **PDF/A** (`.pdf`) - Official authentic version
   - Legally binding format
   - Not suitable for automated conversion

## Usage

### Download a Document

```bash
# Download Formex XML (default format)
python scripts/download_eurlex.py 32024L1385

# Download in Italian
python scripts/download_eurlex.py 32024L1385 --lang IT

# Download XHTML format
python scripts/download_eurlex.py 32024L1385 --format xhtml --output document.xhtml

# List available formats
python scripts/download_eurlex.py --list-formats
```

### Supported Languages

- EN - English (ENG)
- IT - Italian (ITA)
- FR - French (FRA)
- DE - German (DEU)
- ES - Spanish (SPA)
- And 19 other EU languages

See `scripts/download_eurlex.py` for the complete mapping.

## CELEX Numbers

EUR-Lex documents are identified by CELEX numbers:

- Format: `[sector][year][type][number]`
- Example: `32024L1385`
  - `3` = Legislation sector
  - `2024` = Year
  - `L` = Directive (L=Directive, R=Regulation, D=Decision)
  - `1385` = Sequential number

## Finding CELEX Numbers

1. Browse EUR-Lex: https://eur-lex.europa.eu
2. Search for a document
3. The CELEX number is shown in the document metadata
4. Or extract from URL: `/eli/dir/2024/1385/oj` → CELEX: `32024L1385`

## API Documentation

Full API documentation available in `docs/EURLEX_API.md`.

## Next Steps

To convert EUR-Lex Formex XML to Markdown, we need to create a converter similar to `convert_akomantoso.py`:

```bash
python scripts/convert_eurlex.py test_data/eurlex_sample.xml output.md
```

This converter will:
1. Parse Formex XML structure
2. Extract articles, paragraphs, and lists
3. Convert to clean Markdown format
4. Preserve document structure and metadata

## Example Documents

Test documents are available in `test_data/`:
- `eurlex_sample.xml` - English Formex XML
- `eurlex_sample_it.xhtml` - Italian XHTML

## References

- [EUR-Lex API Documentation](EURLEX_API.md)
- [EUR-Lex Homepage](https://eur-lex.europa.eu)
- [Formex Format Specification](https://op.europa.eu/en/web/eu-vocabularies/formex)
