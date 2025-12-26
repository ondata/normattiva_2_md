# cli-interface Spec Delta

## ADDED Requirements

### Requirement: Custom Enforcement Date Parameter
The system SHALL provide a CLI parameter to specify a custom enforcement date (data di vigenza) for legal document retrieval.

#### Scenario: Specifying Custom Vigenza Date
- **WHEN** user runs `normattiva2md "URL" --data-vigenza 20231215 -o output.md`
- **THEN** system SHALL use `20231215` as the vigenza date
- **AND** override any date found in the HTML form
- **AND** download the document version in force on that date

#### Scenario: Date Format Validation
- **WHEN** user provides `--data-vigenza` with invalid format
- **THEN** system SHALL reject the input
- **AND** print clear error message to stderr
- **AND** exit with non-zero status code
- **AND** suggest correct format (YYYYMMDD)

#### Scenario: Valid Date Formats
- **WHEN** user provides `--data-vigenza 20231215`
- **THEN** system SHALL accept the date
- **WHEN** user provides `--data-vigenza 2023-12-15`
- **THEN** system SHALL reject it (only YYYYMMDD format allowed)

#### Scenario: Combining with URL Download
- **WHEN** user provides normattiva.it URL with `--data-vigenza`
- **THEN** system SHALL use the specified date in download request
- **AND** include the date in metadata front matter
- **AND** use it for the XML download URL

#### Scenario: Local XML File Handling
- **WHEN** user provides local XML file with `--data-vigenza`
- **THEN** system SHALL print warning to stderr
- **AND** ignore the parameter (local XML already has its own vigenza)
- **AND** proceed with conversion

#### Scenario: Default Behavior Unchanged
- **WHEN** user does not provide `--data-vigenza`
- **THEN** system SHALL extract date from HTML form (if available)
- **AND** fall back to current date if not found
- **AND** maintain existing behavior

#### Scenario: Help Text Documentation
- **WHEN** user runs `normattiva2md --help`
- **THEN** help text SHALL document `--data-vigenza` parameter
- **AND** explain YYYYMMDD format requirement
- **AND** provide example usage
