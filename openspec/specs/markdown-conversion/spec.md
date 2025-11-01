# markdown-conversion Specification

## Purpose
TBD - created by archiving change adjust-heading-hierarchy-and-add-frontmatter. Update Purpose after archive.
## Requirements
### Requirement: Structured Heading Hierarchy
The system SHALL generate Markdown with a consistent heading hierarchy where the law title uses H1, and all other structural elements (chapters, sections, articles) use progressively lower heading levels.

#### Scenario: Law Title as H1
- **WHEN** converting an Akoma Ntoso document
- **THEN** the law title SHALL be output as H1 at the document start
- **AND** all subsequent headings SHALL be lowered by one level

#### Scenario: Article Heading Levels
- **WHEN** processing articles in the document body
- **THEN** articles SHALL use H2 instead of H1
- **AND** article subsections SHALL use appropriate lower levels

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

### Requirement: Metadata Extraction
The system SHALL extract document metadata from Akoma Ntoso XML meta sections and normattiva.it URL parameters.

#### Scenario: XML Meta Section Parsing
- **WHEN** processing XML with meta section
- **THEN** dataGU, codiceRedaz, and dataVigenza SHALL be extracted from appropriate XML elements

#### Scenario: URL Parameter Fallback
- **WHEN** processing normattiva.it URLs
- **THEN** metadata SHALL be extracted from URL parameters as fallback

### Requirement: Version Flag

The system SHALL provide `--version` and `-v` flags to display the installed package version.

#### Scenario: Display version with long flag

- **WHEN** user runs `akoma2md --version`
- **THEN** the tool SHALL print the version number from package metadata
- **AND** exit without performing conversion

#### Scenario: Display version with short flag

- **WHEN** user runs `akoma2md -v`
- **THEN** the tool SHALL print the version number from package metadata
- **AND** exit without performing conversion

#### Scenario: Version flag takes precedence

- **WHEN** user runs `akoma2md --version input.xml`
- **THEN** the tool SHALL display version and exit
- **AND** no conversion SHALL be attempted

