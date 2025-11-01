## Context
The current conversion produces Markdown with inconsistent heading levels where articles and titles both use H1, making it difficult for document processors and LLMs to understand the hierarchy. Users want a more structured output with clear metadata available in front matter format.

## Goals / Non-Goals
- Goals: Implement consistent heading hierarchy, add law title as top-level H1, provide metadata in YAML front matter
- Non-Goals: Change the core conversion logic, modify XML parsing, add new output formats

## Decisions
- Decision: Extract metadata from XML meta section when available, fall back to URL parameters for normattiva.it URLs
- Alternatives considered: Always require URL input vs extract from XML (chose XML extraction for broader compatibility)
- Decision: Use YAML front matter format for metadata (standard for Markdown documents)
- Decision: Lower all headings by one level to create proper hierarchy under the law title H1

## Risks / Trade-offs
- Risk: Breaking change for existing users expecting current heading levels → Mitigation: Document the change clearly
- Risk: Metadata not available in all XML files → Mitigation: Make front matter optional when metadata missing
- Trade-off: Additional processing time for metadata extraction vs better document structure

## Migration Plan
1. Implement changes with backward compatibility flag (if needed)
2. Update documentation and examples
3. Release as new version with clear changelog
4. Provide migration guide for users affected by heading level changes

## Open Questions
- How to handle XML files without complete metadata in meta section?
- Should front matter be optional or always included when metadata available?