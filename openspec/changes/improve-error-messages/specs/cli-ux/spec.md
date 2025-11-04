## ADDED Requirements

### Requirement: Helpful Error Messages for Invalid Input

When the user provides input that is neither a valid file path nor a URL, the CLI SHALL display a helpful error message explaining the three valid usage modes: URL from normattiva.it, local XML file path, or search query with `-s`.

#### Scenario: Invalid input shows helpful guidance

- **WHEN** user runs `akoma2md "legge stanca"` or `akoma2md legge stanca`
- **AND** "legge stanca" is not a valid file path
- **AND** "legge stanca" is not a normattiva.it URL
- **THEN** display error message explaining:
  - Option 1: Provide a normattiva.it URL
  - Option 2: Provide a local XML file path
  - Option 3: Use `-s "query"` to search for a law

#### Scenario: Valid file path still works

- **WHEN** user provides a valid XML file path
- **THEN** conversion proceeds normally without showing the error message

#### Scenario: Valid URL still works

- **WHEN** user provides a valid normattiva.it URL
- **THEN** conversion proceeds normally without showing the error message

#### Scenario: Search flag still works

- **WHEN** user provides `-s "query"`
- **THEN** search proceeds normally without showing the error message
