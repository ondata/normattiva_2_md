## ADDED Requirements
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