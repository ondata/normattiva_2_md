# Add Data Vigenza CLI Parameter

## Why
Users currently cannot specify a custom enforcement date (data di vigenza) when downloading legal documents from normattiva.it. The tool either:
1. Extracts the date from the HTML form on the normattiva.it page (if present)
2. Defaults to today's date if not found

This prevents users from retrieving historical versions of laws as they were in force on specific past dates without manually navigating the normattiva.it website to select the date first.

## What Changes
- Add `--data-vigenza` CLI flag accepting dates in YYYYMMDD format
- Override automatic date extraction when the flag is provided
- Apply the custom date to the XML download request
- Validate the date format before processing
- Work with normattiva.it URLs (local XML files already contain their own vigenza date)

## Impact
- Affected specs: `cli-interface`
- Affected code:
  - `src/normattiva2md/cli.py` - add `--data-vigenza` argument and pass to download function
  - `src/normattiva2md/normattiva_api.py` - accept optional `data_vigenza` parameter in `extract_params_from_normattiva_url()` and `download_akoma_ntoso()`
- No breaking changes
- Backward compatible (optional parameter)
- Default behavior unchanged (auto-detection or current date)
