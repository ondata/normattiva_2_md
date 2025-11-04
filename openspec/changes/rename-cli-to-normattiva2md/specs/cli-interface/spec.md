# cli-interface Specification

## Purpose
Define the command-line interface naming and behavior for the normattiva2md tool.

## ADDED Requirements

### Requirement: CLI Command Name
The system SHALL be installed as `normattiva2md` command for better discoverability and clarity about its purpose with Italian legal documents.

#### Scenario: Command Installation
- **WHEN** user installs the package via pip
- **THEN** the `normattiva2md` command SHALL be available in PATH
- **AND** running `normattiva2md --help` SHALL display usage information

#### Scenario: Backward Compatibility
- **WHEN** existing users run the old `akoma2md` command
- **THEN** the system MAY provide a deprecation warning directing users to use `normattiva2md`
- **OR** the old command MAY be removed entirely as a breaking change

#### Scenario: Consistent Branding
- **WHEN** users interact with the tool
- **THEN** all references SHALL use `normattiva2md` in documentation, examples, and help text
- **AND** the tool SHALL be clearly identified as focused on normattiva.it legal documents