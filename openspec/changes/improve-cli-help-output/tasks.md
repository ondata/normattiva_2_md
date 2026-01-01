# Implementation Tasks for improve-cli-help-output

## 1. Dependency Management

- [x] 1.1 Add Rich to project dependencies
  - Update `setup.py` with `rich>=13.0.0,<14.0.0`
  - Update `pyproject.toml` with same version constraint
  - Test with `python -m pip install -e .`
  - Verify Rich works with Python 3.7+

## 2. Rich Help Integration

- [x] 2.1 Create Rich-based help formatter
  - Create new function `print_rich_help()` in `cli.py`
  - Use Rich's `Console`, `Panel`, `Rule` for sections
  - Use Rich's `Table` for organized option display
  - Use Rich syntax highlighting for code examples
  - Use Rich colors for visual hierarchy (titles, sections, examples)

- [x] 2.2 Design help layout
  - Main title with version in prominent panel
  - Brief description paragraph
  - Section: "Usage" with common patterns
  - Section: "Options" organized by category (Input/Output, Filtering, Search, etc.)
  - Section: "Examples" with color-coded code blocks
  - Footer with project URL and version info

- [x] 2.3 Integrate with argparse flow
  - Detect when help is requested (no args or `--help`)
  - Call `print_rich_help()` instead of default argparse help
  - Exit cleanly after displaying help

- [x] 2.4 Handle terminal limitations
  - Rich auto-detects terminal capabilities
  - Test with TERM=dumb (no colors)
  - Test with narrow terminal widths
  - Ensure graceful degradation

## 3. Content Migration

- [x] 3.1 Port existing help content to Rich
  - Migrate epilog examples to Rich code blocks
  - Convert argument descriptions to Rich tables
  - Add section headers with Rich rules
  - Preserve all existing information and examples

- [x] 3.2 Enhance help content
  - Add visual grouping for related options
  - Use emoji for sections (where appropriate in Rich)
  - Improve spacing and readability
  - Keep help concise but comprehensive

## 4. Testing

- [x] 4.1 Test Rich help display
  - Test `normattiva2md --help` shows Rich output
  - Test `normattiva2md` (no args) shows Rich output
  - Test with different terminal sizes
  - Test with color disabled (`--no-color` if Rich supports)

- [ ] 4.2 Test with PyInstaller builds
  - Ensure Rich is included in executable
  - Test help display from compiled binary
  - Verify no import errors on startup

- [ ] 4.3 Test Python 3.7+ compatibility
  - Verify Rich works on minimum Python version
  - Test on multiple Python versions (3.7, 3.8, 3.9, 3.10, 3.11)

## 5. Validation & Documentation

- [x] 5.1 Validate openspec proposal
  - Run `openspec validate improve-cli-help-output --strict`
  - Fix any validation errors

- [ ] 5.2 Update documentation
  - Update CLAUDE.md if needed (dependency policy)
  - Update README.md screenshots of help output
  - Document Rich usage in developer docs if needed

- [x] 5.3 Verify backward compatibility
  - All CLI arguments still work identically
  - Only help output changes, not behavior
  - Test all existing integration tests pass
