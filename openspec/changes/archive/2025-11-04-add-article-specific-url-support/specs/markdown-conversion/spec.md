## ADDED Requirements
### Requirement: Article-Specific URL Support
The system SHALL accept normattiva.it URLs with article references (containing `~art` suffixes) and convert only the specified article to Markdown.

#### Scenario: Article Reference Parsing
- **WHEN** user provides a URL with article reference like "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto-legge:2018-07-12;87~art3"
- **THEN** the system SHALL parse the article identifier ("art3") from the URL
- **AND** download the full XML document
- **AND** filter the XML to extract only the specified article

#### Scenario: Single Article Conversion
- **WHEN** processing an article-specific URL
- **THEN** the system SHALL convert only the specified article to Markdown
- **AND** include appropriate metadata indicating it's a single article
- **AND** maintain proper heading hierarchy starting from H1

#### Scenario: Article Extensions Support
- **WHEN** article reference includes extensions like "~art16bis" or "~art5ter"
- **THEN** the system SHALL correctly identify and extract the article with extension
- **AND** handle all standard article extension formats (bis, ter, quater, etc.)

#### Scenario: Non-Existent Article
- **WHEN** specified article does not exist in the document
- **THEN** the system SHALL display an informative error message
- **AND** exit without attempting conversion

#### Scenario: Full Document Fallback
- **WHEN** URL does not contain article reference
- **THEN** the system SHALL process the entire document as before
- **AND** maintain backward compatibility