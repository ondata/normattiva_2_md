# markdown-conversion Specification

## Purpose
Convert XML Akoma Ntoso legal documents from normattiva.it to structured Markdown format optimized for LLM consumption and legal analysis.
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

### Requirement: Atto Intero Export URL Support
The system SHALL accept normattiva.it atto intero export URLs (containing parameters in query string) and extract XML download parameters directly from the URL.

#### Scenario: Export URL Parameter Extraction
- **WHEN** user provides an atto intero export URL like "https://www.normattiva.it/esporta/attoCompleto?atto.dataPubblicazioneGazzetta=2018-07-13&atto.codiceRedazionale=18G00112"
- **THEN** the system SHALL parse the query parameters to extract dataGU, codiceRedaz, and dataVigenza
- **AND** proceed with XML download and conversion

#### Scenario: Fallback to Page Scraping
- **WHEN** user provides a law page URL like "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto-legge:2018-07-12;87"
- **THEN** the system SHALL scrape the page HTML to extract parameters from hidden form inputs
- **AND** proceed with XML download and conversion

#### Scenario: Invalid Export URL
- **WHEN** export URL lacks required parameters
- **THEN** the system SHALL display an informative error message
- **AND** exit without attempting conversion

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

#### Scenario: Inline Cross-Reference Linking
- **WHEN** generating the main markdown file in --with-references mode
- **THEN** law references in the main document SHALL be converted to clickable markdown links
- **AND** each link SHALL point to the corresponding downloaded markdown file in refs/
- **AND** link format SHALL be [reference text](refs/filename.md)
- **AND** only successfully downloaded references SHALL be converted to links

#### Scenario: Rate Limiting for Respectful Usage
- **WHEN** downloading multiple cited laws in --with-references mode
- **THEN** the system SHALL wait at least 1 second between each HTTP request to normattiva.it
- **AND** this delay SHALL apply only to batch downloads, not to single document downloads
- **AND** the delay SHALL not affect the overall functionality or output quality

### Requirement: Entry-Into-Force Date in Front Matter
The system SHALL extract and include entry-into-force date (`dataEntrataInVigore`) in YAML front matter when available in the source XML.

#### Scenario: Entry-Into-Force Date Extraction
- **WHEN** processing XML with entry-into-force information in preface authorialNote
- **THEN** system SHALL parse text starting with "Entrata in vigore"
- **AND** extract date in formats d/m/yyyy, dd/mm/yyyy, or yyyy-mm-dd
- **AND** normalize to YYYYMMDD format
- **AND** include as `dataEntrataInVigore` field in front matter

#### Scenario: Missing Entry-Into-Force Date
- **WHEN** no entry-into-force information is found in XML
- **THEN** system SHALL omit `dataEntrataInVigore` field from front matter
- **AND** continue processing without error

#### Scenario: Date Format Normalization
- **WHEN** extracting entry-into-force dates
- **THEN** system SHALL accept multiple date formats (d/m/yyyy, dd/mm/yyyy, yyyy-mm-dd)
- **AND** normalize all to YYYYMMDD format consistent with other metadata fields

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

