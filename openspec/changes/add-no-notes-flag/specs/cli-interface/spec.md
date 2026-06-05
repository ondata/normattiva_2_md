# cli-interface — Delta Spec

## MODIFIED Requirements

### Requirement: Notes Filter Parameter
The system SHALL provide a `--no-notes` flag to exclude AGGIORNAMENTO annotation blocks from the Markdown output.

#### Scenario: Basic usage with local XML file
- **WHEN** user runs `normattiva2md --no-notes input.xml output.md`
- **THEN** output SHALL not contain any paragraph starting with `AGGIORNAMENTO`
- **AND** all other article text SHALL be preserved unchanged
- **AND** inline modifications `(( ... ))` SHALL remain in the output

#### Scenario: Usage with normattiva.it URL
- **WHEN** user runs `normattiva2md --no-notes "https://www.normattiva.it/..." output.md`
- **THEN** conversion SHALL download the XML normally
- **AND** output SHALL exclude AGGIORNAMENTO blocks
- **AND** exit code SHALL be 0

#### Scenario: Default behavior unchanged
- **WHEN** user runs `normattiva2md input.xml output.md` without `--no-notes`
- **THEN** AGGIORNAMENTO blocks SHALL appear in the output as before
- **AND** no behavioral change from current version

#### Scenario: Combination with --art
- **WHEN** user runs `normattiva2md --no-notes --art 4 input.xml`
- **THEN** output SHALL contain only article 4
- **AND** AGGIORNAMENTO blocks within article 4 SHALL be excluded

#### Scenario: Help documentation
- **WHEN** user runs `normattiva2md --help`
- **THEN** `--no-notes` SHALL be listed in the options table
- **AND** description SHALL explain that it excludes AGGIORNAMENTO annotation blocks
