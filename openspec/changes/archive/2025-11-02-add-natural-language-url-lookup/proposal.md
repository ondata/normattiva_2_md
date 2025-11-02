## Why
Users currently need to know exact normattiva.it URLs to convert legal documents. This creates a barrier for users who know the law by name (e.g., "legge stanca") but not its URL. Adding natural language search would make the tool more accessible and user-friendly.

## What Changes
- Add new CLI option to accept natural language strings instead of URLs
- Integrate Gemini CLI headless to interpret strings and search normattiva.it
- Automatically resolve found URLs and pass to existing conversion logic
- **BREAKING**: No breaking changes, this is an additive feature

## Impact
- Affected specs: New url-lookup capability
- Affected code: Main CLI entry point, new URL lookup module
- New dependency: Gemini CLI (external tool)
- User experience: Simplified input for legal document conversion