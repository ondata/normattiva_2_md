## ADDED Requirements
### Requirement: Complete Flag Override for Article URLs
The system SHALL provide a `--completo` (`-c`) flag that forces conversion of the complete law document even when the URL specifies a single article.

#### Scenario: Complete Flag with Article URL
- **WHEN** user provides an article-specific URL like "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto-legge:2018-07-12;87~art3"
- **AND** uses the `--completo` flag
- **THEN** the system SHALL download the full XML document
- **AND** convert the entire document to Markdown (ignoring the article reference)
- **AND** include metadata indicating the original URL contained an article reference

#### Scenario: Complete Flag with Full Law URL
- **WHEN** user provides a full law URL like "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2022;53"
- **AND** uses the `--completo` flag
- **THEN** the system SHALL behave identically to processing without the flag
- **AND** convert the entire document as normal

#### Scenario: Article URL Without Complete Flag
- **WHEN** user provides an article-specific URL without the `--completo` flag
- **THEN** the system SHALL filter to the specific article as before
- **AND** maintain existing behavior for single article conversion

#### Scenario: Complete Flag Metadata
- **WHEN** using `--completo` with an article-specific URL
- **THEN** the front matter SHALL include the original article-specific URL
- **AND** MAY include additional metadata indicating complete conversion was requested