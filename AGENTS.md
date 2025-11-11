<!-- OPENSPEC:START -->
# OpenSpec Instructions

These instructions are for AI assistants working in this project.

Always open `@/openspec/AGENTS.md` when the request:
- Mentions planning or proposals (words like proposal, spec, change, plan)
- Introduces new capabilities, breaking changes, architecture shifts, or big performance/security work
- Sounds ambiguous and you need the authoritative spec before coding

Use `@/openspec/AGENTS.md` to learn:
- How to create and apply change proposals
- Spec format and conventions
- Project structure and guidelines

Keep this managed block so 'openspec update' can refresh the instructions.

<!-- OPENSPEC:END -->

# Agent Guidelines for akoma2md

## Build/Test Commands
- **All tests**: `make test` or `python -m unittest discover -s tests`
- **Single test**: `python -m unittest tests.test_convert.ConvertAkomaNtosoTest.test_document_title_is_rendered`
- **Quick conversion test**: `python convert_akomantoso.py test_data/20050516_005G0104_VIGENZA_20250130.xml output.md`
- **Build executable**: `make build`
- **Install package**: `make install`

## Code Style Guidelines
- **Formatting**: PEP 8, 4-space indentation, 88-char line length
- **Naming**: snake_case for functions/variables, UPPER_SNAKE_CASE for constants
- **Imports**: Standard library first, then third-party, alphabetical within groups
- **Types**: No type hints (maintains Python 3.7+ compatibility)
- **Docstrings**: Google-style with Args/Returns for public functions
- **Error handling**: Use try/except, print errors to stderr, return None/False on failure
- **Dependencies**: Keep minimal; only add to setup.py if essential
- **Regex/XPath**: Comment non-obvious patterns inline
- **CLI args**: Use argparse, support both positional and named flags

## Version Bump Checklist
- Update the declared version string in `pyproject.toml` and `setup.py` so packaging metadata stays aligned.
- Mirror the same version in `convert_akomantoso.py` (the CLI reads it for `--version` and User-Agent). If the `build/lib/convert_akomantoso.py` artifact is committed, keep it in sync during the same change.
- After editing, run `normattiva2md --version` (from the local install) or `python convert_akomantoso.py --version` to verify the new number appears, then commit all touched files together.
