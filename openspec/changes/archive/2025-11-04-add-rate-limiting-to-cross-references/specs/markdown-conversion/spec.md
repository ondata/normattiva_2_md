## MODIFIED Requirements
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
- **AND** the delay SHALL not affect the overall functionality or output quality</content>
</xai:function_call"> 

Assistant: Ora devo completare tasks.md. Per una modifica semplice come questa, i task dovrebbero essere:

1. Aggiungere import time se non già presente
2. Modificare la funzione convert_with_references per aggiungere time.sleep(1) nel loop di download
3. Testare che la funzionalità funzioni ancora correttamente
4. Verificare che il delay sia applicato (possibilmente con un test che misura il tempo)

Procedo con tasks.md. 

<xai:function_call name="write">
<parameter name="filePath">openspec/changes/add-rate-limiting-to-cross-references/tasks.md