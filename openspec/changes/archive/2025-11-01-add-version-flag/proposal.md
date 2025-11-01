## Why

Users need to check which version of akoma2md is installed for debugging, compatibility verification, and reporting issues.

## What Changes

- Add `--version` and `-v` flags to CLI
- Display version from package metadata
- Exit after showing version (no conversion)

## Impact

- Affected specs: markdown-conversion
- Affected code: convert_akomantoso.py (argparse configuration)
