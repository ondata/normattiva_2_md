## Context
The current tool requires users to provide exact normattiva.it URLs. This proposal adds natural language input capability using Gemini CLI to interpret user strings and find corresponding URLs.

## Goals / Non-Goals
- Goals: Enable natural language search for legal documents, maintain existing URL/XML input methods
- Non-Goals: Replace existing input methods, add general web search (only normattiva.it), store search history

## Decisions
- Use Gemini CLI headless with -p flag for AI-powered interpretation
- Add new CLI flag for natural language input
- Integrate URL lookup as preprocessing step before existing conversion
- Fallback to existing behavior if URL lookup fails

## Risks / Trade-offs
- External dependency on Gemini CLI (user must install separately)
- Potential API rate limits or costs for Gemini usage
- Accuracy of AI interpretation may vary
- Increased complexity in CLI argument handling

## Migration Plan
- Additive feature, no migration needed
- Existing scripts continue to work unchanged
- New functionality available via new flag

## Open Questions
- How to handle multiple URL matches from Gemini?
- What error messages for failed lookups?
- Should we cache successful lookups?