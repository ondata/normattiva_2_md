# cli-interface Delta Specification

## ADDED Requirements

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
