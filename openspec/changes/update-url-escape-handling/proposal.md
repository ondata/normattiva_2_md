# Update escaped URL handling

## Summary
Allow conversion when normattiva URLs include backslash-escaped delimiters by normalizing them before validation and download.

## Motivation

- Some terminals or copy sources escape `?`, `;`, `!`, `=` with backslashes, causing URL validation or download failures.
- Normalize input to reduce user friction and make pasted links work reliably.

## Impact

- CLI/API input handling: normalize escaped URLs before `validate_normattiva_url` and `extract_params_from_normattiva_url`.
- Tests: add coverage for escaped URL input.

## Open Questions / Risks

- Should normalization remove only backslashes before reserved delimiters or strip all backslashes in URLs?
- Should the normalized URL be echoed in logs/metadata instead of the raw input?
