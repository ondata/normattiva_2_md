## ADDED Requirements
### Requirement: Browser Light Conversion Mode
The system SHALL provide a browser-based “light” conversion path that fetches Normattiva XML via a controlled proxy and converts it to Markdown in-page using Pyodide without relying on local filesystem access.

#### Scenario: Proxy-Mediated Fetch
- **WHEN** a user triggers conversion from a Normattiva permalink in the browser
- **THEN** the system SHALL obtain the XML through a proxy that only forwards whitelisted Normattiva endpoints
- **AND** the proxy SHALL set permissive CORS headers for the client response

#### Scenario: In-Browser Conversion
- **WHEN** XML is returned by the proxy
- **THEN** the client SHALL run the existing Akoma Ntoso → Markdown logic inside Pyodide
- **AND** generated headings and YAML front matter SHALL follow the same rules as the CLI conversion

#### Scenario: Respectful Usage Limits
- **WHEN** the proxy processes requests
- **THEN** it SHALL reject payloads larger than the configured safety limit
- **AND** it SHALL enforce at least a 1-second delay between upstream fetches to Normattiva
- **AND** it SHALL refuse URLs outside the Normattiva domain

#### Scenario: Browser-Friendly Output
- **WHEN** conversion completes
- **THEN** the client SHALL provide the Markdown as a downloadable blob or inline viewer
- **AND** no local disk write SHALL be required to obtain the output
