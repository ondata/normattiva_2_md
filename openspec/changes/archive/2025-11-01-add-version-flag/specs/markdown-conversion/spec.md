## ADDED Requirements

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
