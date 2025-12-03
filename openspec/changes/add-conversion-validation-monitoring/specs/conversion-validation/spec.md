# conversion-validation Specification

## Purpose
Provide automated monitoring and validation of Akoma Ntoso to Markdown conversion rules through scheduled testing and issue reporting.

## ADDED Requirements

### Requirement: Weekly Schema Validation
The system SHALL run automated schema and extraction validation tests weekly to detect breaking changes in normattiva.it HTML structure or XML schema.

#### Scenario: Scheduled Weekly Execution
- **WHEN** the workflow is scheduled to run (every Monday at 09:00 UTC)
- **THEN** the system SHALL execute validation tests against a sample legal document URL
- **AND** report results to GitHub Actions logs
- **AND** create issues if validation fails

#### Scenario: Manual Workflow Trigger
- **WHEN** a maintainer manually triggers the workflow via GitHub Actions UI
- **THEN** the system SHALL execute the same validation tests on-demand
- **AND** report results immediately

### Requirement: HTML Parameter Extraction Validation
The system SHALL verify that parameter extraction from normattiva.it HTML pages continues to work correctly.

#### Scenario: HTML Form Parameter Extraction
- **WHEN** running validation against a normattiva.it page URL
- **THEN** the system SHALL download the HTML page
- **AND** verify that hidden input fields for dataGU, codiceRedaz, dataVigenza are found
- **AND** verify extracted values are non-empty and in expected format

#### Scenario: HTML Structure Change Detection
- **WHEN** HTML parsing fails to extract required parameters
- **THEN** the test SHALL fail with specific error indicating which parameter is missing
- **AND** report that normattiva.it HTML structure may have changed

### Requirement: XML Schema Stability Validation
The system SHALL verify that Akoma Ntoso XML schema remains stable and compatible with conversion logic.

#### Scenario: Namespace Validation
- **WHEN** running validation against downloaded XML document
- **THEN** the system SHALL verify Akoma Ntoso 3.0 namespace is present
- **AND** verify namespace URL is unchanged: `http://docs.oasis-open.org/legaldocml/ns/akn/3.0`

#### Scenario: Essential Elements Validation
- **WHEN** validating XML structure
- **THEN** the system SHALL verify presence of essential elements:
  - `<akomaNtoso>` root element
  - `<meta>` metadata section
  - `<body>` document body
  - At least one `<article>` element
- **AND** report which elements are missing if validation fails

### Requirement: Automated Issue Creation
The system SHALL automatically create GitHub issues when validation tests fail, assigned to the project maintainer.

#### Scenario: Test Failure Issue Creation
- **WHEN** one or more integration tests fail in the weekly workflow
- **THEN** the system SHALL create a GitHub issue with:
  - Title: "Conversion validation failed - [date]"
  - Body containing summary of all failures
  - Labels: "bug", "automated"
  - Assignee: @aborruso

#### Scenario: Issue Content Detail
- **WHEN** creating an automated issue
- **THEN** the issue body SHALL include:
  - List of failed document URLs/identifiers
  - Specific error messages or validation failures
  - Link to failed workflow run
  - Comparison diff if output structure changed

#### Scenario: Success Without Issue
- **WHEN** all validation tests pass
- **THEN** no GitHub issue SHALL be created
- **AND** workflow SHALL complete with success status

### Requirement: Download Stability Validation
The system SHALL verify that XML document download from normattiva.it continues to work correctly.

#### Scenario: XML Download Success
- **WHEN** testing document download from normattiva.it
- **THEN** the system SHALL verify HTTP response is successful (200)
- **AND** verify response content-type indicates XML
- **AND** verify response body is valid XML (parseable)
- **AND** report failure if download fails or returns HTML error page
