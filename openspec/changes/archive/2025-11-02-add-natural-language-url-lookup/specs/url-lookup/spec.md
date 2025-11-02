## ADDED Requirements

### Requirement: Natural Language URL Lookup
The system SHALL accept natural language strings describing legal documents and use Gemini CLI to find corresponding normattiva.it URLs for conversion.

#### Scenario: Successful URL Resolution
- **WHEN** user provides a natural language string like "legge stanca"
- **THEN** the system SHALL call Gemini CLI with appropriate prompt
- **AND** extract the found normattiva.it URL
- **AND** proceed with conversion using the resolved URL

#### Scenario: No URL Found
- **WHEN** Gemini CLI cannot find a matching URL
- **THEN** the system SHALL display an informative error message
- **AND** exit without attempting conversion

#### Scenario: Gemini CLI Unavailable
- **WHEN** Gemini CLI is not installed or accessible
- **THEN** the system SHALL display installation guidance
- **AND** exit with appropriate error code

#### Scenario: Multiple URL Matches
- **WHEN** Gemini returns multiple potential URLs
- **THEN** the system SHALL use the most relevant match
- **OR** prompt user to choose if interactive mode is available