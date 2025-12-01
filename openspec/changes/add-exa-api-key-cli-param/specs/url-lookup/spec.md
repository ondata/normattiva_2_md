# url-lookup Specification

## Purpose
Enable flexible Exa API key configuration for natural language search functionality through both CLI parameters and environment variables.

## ADDED Requirements

### Requirement: Exa API Key Configuration Options
The system SHALL accept Exa API key through both CLI parameter and environment variable, with CLI parameter taking precedence.

#### Scenario: CLI Parameter Provided
- **WHEN** user provides --exa-api-key parameter with search query
- **THEN** the system SHALL use the provided API key for Exa API calls
- **AND** ignore any EXA_API_KEY environment variable

#### Scenario: Environment Variable Fallback
- **WHEN** user does not provide --exa-api-key parameter
- **AND** EXA_API_KEY environment variable is set
- **THEN** the system SHALL use the environment variable value for Exa API calls

#### Scenario: No API Key Configured
- **WHEN** neither --exa-api-key parameter nor EXA_API_KEY environment variable are provided
- **THEN** the system SHALL display error message mentioning both configuration options
- **AND** exit without attempting search

#### Scenario: Invalid API Key
- **WHEN** provided API key (CLI or environment) is invalid or rejected by Exa API
- **THEN** the system SHALL display appropriate authentication error
- **AND** suggest checking API key configuration

## MODIFIED Requirements

### Requirement: Natural Language URL Lookup
The system SHALL accept natural language strings describing legal documents and use Exa AI API to find corresponding normattiva.it URLs for conversion, supporting flexible API key configuration.

#### Scenario: Successful URL Resolution with CLI API Key
- **WHEN** user provides natural language string and --exa-api-key parameter
- **THEN** the system SHALL use CLI-provided API key to call Exa AI API
- **AND** extract the found normattiva.it URL
- **AND** proceed with conversion using the resolved URL