# markdown-conversion Specification Delta

## ADDED Requirements

### Requirement: Escaped Normattiva URL Normalization
The system SHALL normalize normattiva.it URLs containing escape characters from user input before validation and download.

#### Scenario: Backslash-escaped URL from clipboard
- **WHEN** user provides a normattiva.it URL containing backslash-escaped reserved characters (for example `\?`, `\;`, `\!`, `\=`)
- **THEN** the system SHALL remove the escape backslashes to produce a valid URL
- **AND** proceed with validation and download using the normalized URL
