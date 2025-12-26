# Tasks

## Implementation Tasks

- [ ] Add `--data-vigenza` argument to CLI parser in `src/normattiva2md/cli.py`
  - Add argparse parameter with help text and format description
  - Add to epilog examples section

- [ ] Implement date format validation function
  - Create `validate_vigenza_date(date_str)` function
  - Accept only YYYYMMDD format (8 digits)
  - Return validated date or raise ValueError with clear message
  - Check basic date validity (month 1-12, day 1-31)

- [ ] Integrate validation in CLI argument processing
  - Call validation after argument parsing
  - Print error to stderr if validation fails
  - Exit with non-zero status on invalid date

- [ ] Modify `extract_params_from_normattiva_url()` function signature
  - Add optional `custom_vigenza=None` parameter
  - Override extracted/default date if `custom_vigenza` provided
  - Update function docstring

- [ ] Pass custom date from CLI to extraction function
  - Pass `args.data_vigenza` to `extract_params_from_normattiva_url()`
  - Ensure date flows through to params dict

- [ ] Handle local XML file case
  - Check if input is local file when `--data-vigenza` provided
  - Print warning to stderr: "⚠️ --data-vigenza ignored for local XML files"
  - Continue processing without error

- [ ] Update help text and examples
  - Add `--data-vigenza` to examples in epilog
  - Document YYYYMMDD format requirement
  - Show example: `normattiva2md "URL" --data-vigenza 20231215 -o output.md`

## Testing Tasks

- [ ] Test with valid date format
  - Run: `normattiva2md "URL" --data-vigenza 20231215 -o test.md`
  - Verify correct date used in download
  - Check metadata front matter includes custom date

- [ ] Test with invalid date formats
  - Run with `2023-12-15` (should fail)
  - Run with `231215` (should fail)
  - Run with `20231345` (should fail - invalid date)
  - Verify clear error messages

- [ ] Test without parameter (default behavior)
  - Run: `normattiva2md "URL" -o test.md`
  - Verify auto-detection still works
  - Verify fallback to current date works

- [ ] Test with local XML file
  - Run: `normattiva2md local.xml --data-vigenza 20231215 -o test.md`
  - Verify warning printed
  - Verify conversion completes successfully

- [ ] Test help text
  - Run: `normattiva2md --help`
  - Verify `--data-vigenza` documented
  - Verify examples include the parameter

## Documentation Tasks

- [ ] Update README.md with `--data-vigenza` usage
  - Add to examples section
  - Explain use case (historical document versions)

- [ ] Update LOG.md with change entry
  - Add dated entry describing new parameter
  - Note YYYYMMDD format requirement
