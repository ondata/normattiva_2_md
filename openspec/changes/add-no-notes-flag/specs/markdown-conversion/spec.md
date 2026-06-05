# markdown-conversion — Delta Spec

## MODIFIED Requirements

### Requirement: Notes Filter in Conversion Functions
The conversion API SHALL accept a `no_notes` parameter that, when `True`, omits AGGIORNAMENTO annotation blocks from the generated Markdown.

#### Scenario: convert_url with no_notes=True
- **WHEN** `convert_url(url, no_notes=True)` is called
- **THEN** returned `ConversionResult.markdown` SHALL not contain paragraphs starting with `AGGIORNAMENTO`
- **AND** inline `(( ... ))` modifications SHALL be preserved
- **AND** all metadata in `ConversionResult` SHALL be unchanged

#### Scenario: convert_xml with no_notes=True
- **WHEN** `convert_xml(xml_path, no_notes=True)` is called
- **THEN** returned `ConversionResult.markdown` SHALL not contain AGGIORNAMENTO blocks
- **AND** conversion SHALL complete without errors

#### Scenario: Default value preserves backward compatibility
- **WHEN** `convert_url(url)` or `convert_xml(xml_path)` is called without `no_notes`
- **THEN** behavior SHALL be identical to current version
- **AND** no AGGIORNAMENTO content SHALL be removed

#### Scenario: Parameter propagation through internal functions
- **WHEN** `no_notes=True` is passed to `convert_url` or `convert_xml`
- **THEN** `no_notes` SHALL be forwarded to `_convert_xml_internal`
- **AND** from there to `generate_markdown_text`
- **AND** from there to `generate_markdown_fragments` and `extract_body_fragments`
- **AND** ultimately to `process_content_with_paragraphs` where filtering occurs

#### Scenario: Filtering scope covers entire AGGIORNAMENTO block
- **WHEN** `no_notes=True` and an article contains both normal paragraphs and AGGIORNAMENTO blocks
- **THEN** the paragraph starting with `AGGIORNAMENTO` AND all subsequent paragraphs in the same `<content>` element SHALL be omitted
- **AND** all paragraphs before the AGGIORNAMENTO marker SHALL appear in the output unchanged
- **AND** `<ins>/<del>` wrapped text (rendered as `(( ... ))`) SHALL not be affected
