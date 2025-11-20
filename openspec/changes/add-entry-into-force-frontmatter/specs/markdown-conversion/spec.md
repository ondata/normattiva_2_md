# markdown-conversion Specification Delta

## MODIFIED Requirements

### Requirement: YAML Front Matter Metadata
The system SHALL include YAML front matter at the beginning of generated Markdown containing document metadata.

#### Scenario: Complete Metadata from URL
- **WHEN** converting from a normattiva.it URL
- **THEN** front matter SHALL include URL, URL_XML, dataGU, codiceRedaz, and dataVigenza fields

#### Scenario: Metadata from XML
- **WHEN** converting local XML files with meta section
- **THEN** metadata SHALL be extracted from the XML meta section
- **AND** URL fields SHALL be constructed when possible

#### Scenario: Missing Metadata
- **WHEN** metadata is not available
- **THEN** front matter SHALL be omitted or contain only available fields

#### Scenario: Entry-into-force Date Field
- **WHEN** the parsed metadata contains a normalized entry-into-force date (`dataEntrataInVigore`)
- **THEN** the generated front matter SHALL include a `dataEntrataInVigore` key alongside the other metadata
- **AND** its value SHALL be formatted as `YYYYMMDD`
- **AND** the field SHALL be omitted if the date cannot be determined

### Requirement: Metadata Extraction
The system SHALL extract document metadata from Akoma Ntoso XML meta sections and normattiva.it URL parameters.

#### Scenario: XML Meta Section Parsing
- **WHEN** processing XML with meta section
- **THEN** dataGU, codiceRedaz, and dataVigenza SHALL be extracted from appropriate XML elements

#### Scenario: URL Parameter Fallback
- **WHEN** processing normattiva.it URLs
- **THEN** metadata SHALL be extracted from URL parameters as fallback

#### Scenario: Entry-into-force Note Parsing
- **WHEN** the preface or metadata section contains an `<authorialNote>` (or equivalent) whose text begins with "Entrata in vigore"
- **THEN** the system SHALL parse the first date mentioned in that text
- **AND** normalize it to `YYYYMMDD`
- **AND** store it as `dataEntrataInVigore` for downstream use (e.g., front matter emission)
