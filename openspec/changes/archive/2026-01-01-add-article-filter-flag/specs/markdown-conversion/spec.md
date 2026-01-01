# markdown-conversion Delta Specification

## ADDED Requirements

### Requirement: Article Filtering During Conversion
The conversion process SHALL support filtering XML content to a specific article before generating markdown output.

#### Scenario: Filter Article Before Conversion
- **WHEN** article filter is requested via `--art` parameter
- **THEN** system SHALL use `filter_xml_to_article()` to extract target article
- **AND** conversion SHALL process only the filtered article
- **AND** metadata/frontmatter SHALL reflect the full document
- **AND** title SHALL indicate filtered view (e.g., "Art. 4 - [article title]")

#### Scenario: Preserve Document Structure
- **WHEN** converting a filtered article
- **THEN** article numbering SHALL be preserved as-is
- **AND** article SHALL maintain proper markdown heading level (# Art. N)
- **AND** paragraphs and lists SHALL retain correct formatting
- **AND** legislative modifications `(( ))` SHALL be preserved

#### Scenario: Handle Article Extensions in eId
- **WHEN** filtering article with extension (e.g., `--art 16bis`)
- **THEN** system SHALL construct eId as `art_16bis` (no hyphen)
- **AND** search XML using constructed eId format
- **AND** support common extensions: bis, ter, quater, quinquies, sexies, septies, octies, novies, decies, vices, tricies, quadragies
- **AND** case-insensitive matching for extensions

#### Scenario: Empty Result for Missing Article
- **WHEN** requested article is not found in XML
- **THEN** markdown body SHALL be empty (only metadata/frontmatter)
- **AND** warning SHALL be printed to stderr
- **AND** conversion SHALL complete successfully
- **AND** output file SHALL be created with metadata only

#### Scenario: Integration with Existing Features
- **WHEN** article filter is combined with `--with-urls`
- **THEN** reference URLs SHALL still be generated
- **AND** URLs SHALL point to correct articles in cited documents
- **WHEN** article filter is combined with `--with-references`
- **THEN** cited documents SHALL NOT be filtered (download full documents)
- **AND** only main document SHALL be filtered to specified article
