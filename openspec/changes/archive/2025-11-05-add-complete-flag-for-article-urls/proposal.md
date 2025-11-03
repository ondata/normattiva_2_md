# Change Proposal: Add --completo Flag for Article URLs

## Summary
Add a `--completo` (`-c`) command-line flag that forces downloading and converting the complete law even when the URL specifies a single article.

## Motivation
Users may want to download the full law document even when providing an article-specific URL, for example to get context around the specific article or to have the complete document for reference.

## Current Behavior
When an article-specific URL is provided (e.g., `~art3`), the system downloads the full XML but filters it to output only the specified article.

## Proposed Behavior
When the `--completo` flag is used with an article-specific URL, the system should:
1. Download the full XML document
2. Convert the entire document to Markdown (ignoring the article reference)
3. Include metadata indicating it was originally an article-specific request but converted completely

## Impact
- **Backward Compatibility**: No impact on existing behavior without the flag
- **User Experience**: Provides flexibility for users who want full documents
- **Implementation**: Minimal changes to existing filtering logic

## Alternatives Considered
- Automatic full download: Would break existing behavior expectations
- Separate command: Unnecessary complexity for a simple flag
- Configuration file: Overkill for this use case

## Implementation Notes
The flag should override article filtering when present, ensuring the full document is processed regardless of URL article references.