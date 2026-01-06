# Development Setup

## Environment

**Python version**: 3.7+

**Virtual environment**: `.venv` (standard)

## Quick Start

```bash
# Clone repo
git clone https://github.com/ondata/normattiva_2_md.git
cd normattiva_2_md

# Create venv
python3 -m venv .venv

# Activate (Linux/macOS)
source .venv/bin/activate

# Activate (Windows)
.venv\Scripts\activate

# Install editable
pip3 install -e .

# On WSL/Linux, if you get "Invalid cross-device link" error:
# (This happens when /tmp is on a different filesystem)
TMPDIR=$PWD/tmp pip3 install -e .

# Test
normattiva2md test_data/20050516_005G0104_VIGENZA_20250130.xml test.md
```

## Dependencies

**Core**: no external deps (standard library only)

**Optional**:
- `requests`: URL fetching
- `exa_py`: natural language search (requires API key)

## Project Structure

```
normattiva_2_md/
├── __main__.py             # Entrypoint (imports src.normattiva2md.cli)
├── src/normattiva2md/
│   ├── cli.py              # Main CLI (argparse)
│   ├── api.py              # Normattiva API client
│   ├── xml_parser.py       # XML to structured data
│   ├── markdown_converter.py # Converter logic
│   ├── models.py           # Data models
│   └── ...                 # Other modules
├── setup.py                # PyPI config
├── .venv/                  # Virtual environment (gitignored)
├── test_data/              # Sample XML files
└── tests/                  # Test suite
```

## Testing

### Run all tests (recommended)

```bash
# Activate venv FIRST (required for all test/build operations)
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate  # Windows

# Then run tests
make test
```

**Always activate venv before testing, building, or running any development command.**

**Note**: Tests may show warnings for missing `EXA_API_KEY` environment variable. To suppress:
```bash
export EXA_API_KEY=your_key_here
make test
```
(Or skip EXA tests entirely if you don't have API access.)

### Alternative: unittest (no extra deps)

```bash
source .venv/bin/activate
python3 -m unittest discover -s tests
```

### Alternative: pytest (requires install)

```bash
source .venv/bin/activate
pip3 install pytest
python3 -m pytest tests/ -v
```

### Manual testing

```bash
# Basic conversion
normattiva2md test_data/20050516_005G0104_VIGENZA_20250130.xml output.md

# URL test
normattiva2md "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2004-01-09;4" test.md

# Article filter
normattiva2md --art 3 test_data/*.xml test.md
```

## Building Binary

**CRITICAL**: Always use the activated virtual environment (.venv) - never build with system Python.

This prevents binary bloat from global packages:

```bash
# Activate venv first
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate  # Windows

# Then build
pip3 install pyinstaller
pyinstaller --onefile --name normattiva2md __main__.py
# Output: dist/normattiva2md
```

If you build outside venv, the binary will be 4-5x larger due to unnecessary system packages being bundled.

## Publishing to PyPI

```bash
# Activate venv first
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate  # Windows

# Build
python3 setup.py sdist bdist_wheel

# Upload (twine already installed)
twine upload dist/*
```

## Code Style

- Concise variable names
- Minimal comments (code should be self-explanatory)
- stderr for status messages when stdout is used for markdown
- No emoji in code/commits (only docs if requested)

## Git Workflow

```bash
# Always update LOG.md for significant changes
echo "## $(date +%Y-%m-%d)" >> LOG.md
echo "- your change" >> LOG.md

# Commit
git add .
git commit -m "fix: your message"
```

## Common Tasks

### Add new feature
1. Read relevant code first
2. Make minimal changes
3. Test with sample data
4. Update LOG.md
5. Commit

### Fix bug
1. Find root cause (never temporary fixes)
2. Fix as simply as possible
3. Test
4. Update LOG.md
5. Commit

### Release new version
See `CLAUDE.md`: use release-publisher agent or manual twine upload
