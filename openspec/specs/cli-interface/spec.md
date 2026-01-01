# cli-interface Specification

## Purpose
Define command-line interface behavior and entry points for the normattiva2md tool, providing both backward compatibility and clear naming for Italian legal document conversion.
## Requirements
### Requirement: Dual CLI Entry Points
The system SHALL provide both legacy and new command names to ensure backward compatibility while transitioning to more descriptive naming.

#### Scenario: Legacy Command Support
- **WHEN** user runs `akoma2md` command
- **THEN** system SHALL execute the same conversion functionality as `normattiva2md`
- **AND** maintain full feature parity
- **AND** provide identical help text and behavior

#### Scenario: New Preferred Command
- **WHEN** user runs `normattiva2md` command
- **THEN** system SHALL execute conversion functionality
- **AND** this SHALL be the recommended command name
- **AND** all documentation SHALL reference this name

#### Scenario: Package Installation
- **WHEN** user installs package via pip
- **THEN** both `akoma2md` and `normattiva2md` commands SHALL be available
- **AND** both SHALL point to the same main function
- **AND** installation SHALL not require additional configuration

#### Scenario: Help and Version Display
- **WHEN** user runs either command with `--help` or `--version`
- **THEN** system SHALL display appropriate information
- **AND** command name in help SHALL reflect the actual command used
- **AND** version information SHALL be identical for both commands

### Requirement: Command Name Detection
The system SHALL detect the actual command name used to invoke the tool for appropriate display in help and error messages.

#### Scenario: Script Execution
- **WHEN** user runs `python convert_akomantoso.py`
- **THEN** system SHALL display help using `normattiva2md` as command name
- **AND** error messages SHALL reference `normattiva2md`

#### Scenario: Installed Command Execution
- **WHEN** user runs `akoma2md` or `normattiva2md`
- **THEN** system SHALL use the actual command name in output
- **AND** help text SHALL reflect the specific command invoked

#### Scenario: PyInstaller Binary
- **WHEN** user runs standalone binary
- **THEN** system SHALL detect binary name appropriately
- **AND** display correct command name in help and error messages

### Requirement: CLI Help Display
The system SHALL display comprehensive help information when invoked without arguments or with `--help` flag.

#### Scenario: Display Rich-Formatted Help
- **WHEN** user runs `normattiva2md --help`
- **THEN** system SHALL display help formatted with Rich library
- **AND** output SHALL use colors, panels, tables for better readability
- **AND** help SHALL be organized into clear sections (Usage, Options, Examples)
- **AND** code examples SHALL use syntax highlighting

#### Scenario: Display Help on No Arguments
- **WHEN** user runs `normattiva2md` without arguments
- **THEN** system SHALL display Rich-formatted help
- **AND** exit with status code 1

#### Scenario: Terminal Without Color Support
- **WHEN** terminal does not support colors
- **THEN** system SHALL degrade gracefully to plain text
- **AND** help SHALL remain readable and structured
- **AND** no ANSI escape codes SHALL appear

#### Scenario: Help Content Preservation
- **WHEN** Rich formatting is applied
- **THEN** all existing help content SHALL be preserved
- **AND** all CLI options SHALL be documented
- **AND** all usage examples SHALL be included
- **AND** no information SHALL be lost in conversion

#### Scenario: Backward Compatibility
- **WHEN** user invokes any CLI command
- **THEN** command behavior SHALL remain unchanged
- **AND** only help display formatting changes
- **AND** all existing tests SHALL pass

### Requirement: Article Filter Parameter
The system SHALL provide a command-line flag to filter output to a specific article without modifying the input URL or requiring knowledge of URL syntax.

#### Scenario: Basic Article Filter
- **WHEN** user runs `normattiva2md --art 4 input.xml output.md`
- **THEN** system SHALL download/parse the full XML
- **AND** output markdown SHALL contain only article 4
- **AND** all other articles SHALL be excluded from output

#### Scenario: Article with Extension
- **WHEN** user runs `normattiva2md --art 16bis "URL" output.md`
- **THEN** system SHALL filter to article 16-bis
- **AND** extension SHALL be recognized without hyphen (bis, ter, quater, etc.)
- **AND** common extensions SHALL be supported (bis through decies, vices, tricies, quadragies)

#### Scenario: Article Filter with Local File
- **WHEN** user runs `normattiva2md --art 3 local.xml output.md`
- **THEN** system SHALL filter the local XML file
- **AND** work identically to URL-based filtering
- **AND** no network access SHALL be required

#### Scenario: Article Filter with Normattiva URL
- **WHEN** user provides normattiva.it URL without `~artN` and `--art 5` flag
- **THEN** system SHALL download full document
- **AND** filter output to article 5 only
- **AND** URL SHALL remain unmodified during download

### Requirement: Parameter Priority Handling
The system SHALL handle conflicts between URL-embedded article references and the `--art` flag, giving priority to the explicit flag.

#### Scenario: Override URL Article Reference
- **WHEN** user runs `normattiva2md --art 2 "https://...~art5" output.md`
- **THEN** `--art 2` flag SHALL take precedence
- **AND** output SHALL contain only article 2
- **AND** URL's `~art5` SHALL be ignored for filtering purposes
- **AND** system SHALL download the full document (not filtered by URL)

#### Scenario: Nonexistent Article
- **WHEN** user specifies `--art 999` for a document without article 999
- **THEN** system SHALL output empty body (no articles)
- **AND** print warning to stderr: "Warning: Article 999 not found in document"
- **AND** metadata/frontmatter SHALL still be included
- **AND** exit code SHALL be 0 (success)

### Requirement: Help Documentation
The system SHALL document the `--art` flag in help text with clear examples.

#### Scenario: Help Text Display
- **WHEN** user runs `normattiva2md --help`
- **THEN** help SHALL include `--art` parameter description
- **AND** examples SHALL show numeric articles (e.g., `--art 4`)
- **AND** examples SHALL show articles with extensions (e.g., `--art 16bis`)
- **AND** explain behavior with both URLs and local files

