# Implementation Tasks

## 1. CLI Interface

- [ ] 1.1 Add `--art` argument to argparse in `cli.py`
  - Accept string input (e.g., "4", "16bis", "3ter")
  - Add to help text with examples
  - Document interaction with URL-based `~artN`

- [ ] 1.2 Update help examples in `cli.py`
  - Add example: `normattiva2md --art 4 input.xml output.md`
  - Add example: `normattiva2md --art 16bis "URL" output.md`
  - Add example: `normattiva2md --art 3 --with-urls "URL" output.md`

- [ ] 1.3 Add validation for `--art` parameter
  - Check format matches pattern: `^\d+[a-z]*$` (number + optional extension)
  - Warn if invalid format but continue processing
  - Handle case-insensitive extensions

## 2. Article Filtering Logic

- [ ] 2.1 Create article eId construction function
  - Convert user input "4" → "art_4"
  - Convert user input "16bis" → "art_16bis"
  - Handle common extensions (bis through quadragies)
  - Place in `xml_parser.py` or create new `article_utils.py`

- [ ] 2.2 Integrate filtering in conversion flow
  - In `cli.py`, pass `--art` value to conversion function
  - Call `filter_xml_to_article()` before markdown conversion
  - Handle None return (article not found)
  - Print warning to stderr when article not found

- [ ] 2.3 Update `convert_akomantoso_to_markdown_improved()`
  - Accept optional `article_filter` parameter
  - Apply filtering after XML parsing, before conversion
  - Preserve metadata extraction from full document
  - Adjust title in output when filtered

## 3. URL Handling

- [ ] 3.1 Handle URL with existing `~artN`
  - When `--art` is provided, it overrides URL's `~artN`
  - Download full document (ignore URL article reference)
  - Apply filtering using `--art` value instead

- [ ] 3.2 Ensure compatibility with `--completo` flag
  - If both `--completo` and `--art` provided, `--art` takes precedence
  - Document this behavior in help text

## 4. Integration with Existing Features

- [ ] 4.1 Test `--art` with `--with-urls`
  - Verify reference URLs are generated correctly
  - Ensure URLs point to proper articles in cited documents

- [ ] 4.2 Test `--art` with `--with-references`
  - Main document should be filtered
  - Referenced documents should NOT be filtered (download full)

- [ ] 4.3 Test `--art` with `--provvedimenti`
  - Both features should work independently
  - CSV export should work with filtered markdown

## 5. Testing

- [ ] 5.1 Unit tests for eId construction
  - Test numeric articles: "1", "4", "99"
  - Test extensions: "16bis", "3ter", "5quater"
  - Test edge cases: invalid formats

- [ ] 5.2 Integration tests via Makefile
  - Test with local XML file
  - Test with normattiva.it URL
  - Test with URL containing `~artN` (override scenario)
  - Test with nonexistent article number

- [ ] 5.3 Test article extension variations
  - Test all common extensions (bis through decies)
  - Test case insensitivity
  - Test less common extensions (vices, tricies, quadragies)

## 6. Documentation

- [ ] 6.1 Update README.md with `--art` examples
  - Add to CLI usage section
  - Show combination with other flags

- [ ] 6.2 Update CLAUDE.md project instructions
  - Document new `--art` parameter
  - Explain filtering behavior

- [ ] 6.3 Update URL_NORMATTIVA.md if needed
  - Cross-reference `--art` flag as alternative to `~artN`
  - Explain when to use each approach

## 7. Validation

- [ ] 7.1 Run `openspec validate add-article-filter-flag --strict`
  - Resolve any validation errors
  - Ensure all requirements have scenarios

- [ ] 7.2 Test with real normattiva.it documents
  - Test Decreto Legge with multiple articles
  - Test document with articles containing extensions
  - Verify output markdown quality
