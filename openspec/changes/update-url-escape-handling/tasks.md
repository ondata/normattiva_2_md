# Tasks for update-url-escape-handling

## URL Normalization

- [ ] Identify URL intake points (CLI, `convert_url`, `is_normattiva_url`) and add a normalization helper for escaped delimiters.
- [ ] Normalize backslash-escaped reserved characters before validation and download.

## Error Messaging

- [ ] Ensure logs and metadata use the normalized URL consistently.

## Validation

- [ ] Add a unit or CLI test for escaped URL input (use the example from the request).
- [ ] Run relevant tests (`python -m unittest ...` or `make test`).
