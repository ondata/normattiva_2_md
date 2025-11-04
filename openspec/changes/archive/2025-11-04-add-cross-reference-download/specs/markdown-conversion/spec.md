## ADDED Requirements
### Requirement: Cross-Reference Download Mode
The system SHALL provide a `--with-references` parameter that downloads and converts all laws cited in the main document, organizing them in a structured folder hierarchy with cross-references.

#### Scenario: Basic Cross-Reference Download
- **WHEN** user runs `akoma2md --with-references "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2005-03-07;82" output.md`
- **THEN** the system SHALL create a folder named after the law ID (e.g., "legge_2005_82")
- **AND** download and convert the main law to "main.md" in that folder
- **AND** identify all cited laws from XML `<ref>` tags
- **AND** download and convert each cited law to separate markdown files
- **AND** create cross-references between the main law and cited laws

#### Scenario: Folder Structure Creation
- **WHEN** processing a law with cited references
- **THEN** the system SHALL create a folder structure like:
  ```
  legge_2005_82/
  ├── main.md (the requested law)
  ├── refs/
  │   ├── costituzione_1947.md
  │   ├── decreto-legislativo_1993_39.md
  │   └── ...
  └── index.md (summary of all laws)
  ```

#### Scenario: Reference Extraction and Deduplication
- **WHEN** parsing XML for references
- **THEN** the system SHALL extract URIs from all `<ref>` tags
- **AND** filter out non-normattiva.it URLs
- **AND** deduplicate identical law references
- **AND** handle different URI formats (URN, export URLs, article-specific URLs)

#### Scenario: Batch Download with Progress
- **WHEN** downloading multiple cited laws
- **THEN** the system SHALL show progress for each download
- **AND** continue processing even if individual downloads fail
- **AND** report summary of successful/failed downloads

#### Scenario: Cross-Reference Linking
- **WHEN** generating markdown files
- **THEN** cited law references SHALL be converted to relative links
- **AND** the main law SHALL include navigation to cited laws
- **AND** cited laws SHALL include back-references to the main law
