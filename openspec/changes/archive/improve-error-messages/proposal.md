## Why

When users provide invalid input like `akoma2md "legge stanca"` or `akoma2md legge stanca`, the tool shows an unhelpful error message "Errore: Il file XML 'legge' non trovato." This doesn't explain the three valid usage modes: URL input, file path, or search with `-s`.

## What Changes

- Replace generic "file not found" error with helpful message explaining three input modes
- Guide users to correct usage: URL from normattiva.it, local XML file, or search with `-s "query"`
- Improve user experience when invalid input is provided

## Impact

- Affected specs: cli-ux (new capability)
- Affected code: convert_akomantoso.py (error handling in FileNotFoundError exception)
