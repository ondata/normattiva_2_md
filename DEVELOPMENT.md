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

**Core** (from setup.py):
- `requests>=2.25.0`: URL fetching
- `rich>=13.0.0,<14.0.0`: Terminal formatting

**Optional**:
- `exa_py`: natural language search (requires API key)

## Project Structure

```
normattiva_2_md/
├── __main__.py                    # Entrypoint
├── src/normattiva2md/
│   ├── cli.py                    # Main CLI
│   ├── api.py                    # Normattiva API
│   ├── xml_parser.py             # XML parser
│   ├── markdown_converter.py     # Converter
│   ├── models.py                 # Data models
│   ├── akoma_utils.py            # Akoma Ntoso utilities
│   ├── normattiva_api.py         # Legacy API
│   ├── provvedimenti_api.py      # Provvedimenti API
│   ├── exa_api.py                # Exa search API
│   └── ...                       # Altri moduli
├── setup.py                      # PyPI config
├── pyproject.toml                # Modern Python config
├── test_data/                    # Sample XML files
└── tests/                        # Test suite
```

## Testing

### Run all tests (recommended)

```bash
# Activate venv FIRST (required for all test/build operations)
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate  # Windows

# Install the package in editable mode so tests can import `normattiva2md`
pip3 install -e .

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
pip3 install -e .
python3 -m unittest discover -s tests
```

### Alternative: pytest (requires install)

```bash
source .venv/bin/activate
pip3 install -e .
pip3 install pytest
python3 -m pytest tests/ -v
```

### Note on network-dependent tests

- Some tests hit external services (Normattiva, Exa API, programmagoverno.gov.it).
- These can fail due to network or API availability; in that case, the failures are not necessarily regressions.
- For consistent results, ensure network access and configure `EXA_API_KEY` if running Exa tests.

### Coverage Testing

**Current coverage: 40%** (Target: 70%+)

Run tests with coverage reporting:

```bash
source .venv/bin/activate

# Install coverage tools (one-time)
pip3 install pytest pytest-cov

# Run tests with coverage
pytest --cov=src/normattiva2md --cov-report=term-missing --cov-report=html tests/

# View HTML report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

**Coverage reports:**
- Terminal: Shows line-by-line missing coverage
- HTML: `htmlcov/index.html` - Interactive browsable report

**Coverage config** is in `pyproject.toml`:
- Source: `src/normattiva2md/`
- Branch coverage enabled
- Excludes: tests, venv, __pycache__

**Quick commands:**
```bash
# Just show coverage percentage
pytest --cov=src/normattiva2md tests/ -q

# Only show files with <100% coverage
pytest --cov=src/normattiva2md --cov-report=term:skip-covered tests/

# Generate coverage badge data
pytest --cov=src/normattiva2md --cov-report=json tests/
```

**Improving coverage:**
1. Check `htmlcov/index.html` for red/yellow lines
2. Add tests for uncovered code paths
3. Focus on high-impact modules first (api.py, xml_parser.py, normattiva_api.py)
4. See `tmp/coverage_analysis.md` for detailed gap analysis

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
python3 -m PyInstaller --onefile --name normattiva2md __main__.py
# Output: dist/normattiva2md
```

If you build outside venv, the binary will be 4-5x larger due to unnecessary system packages being bundled.

## Publishing to PyPI

```bash
# Activate venv first
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate  # Windows

# Clean dist before building/uploading (avoid non-PyPI artifacts)
rm -f dist/*

# Build
python3 setup.py sdist bdist_wheel

# Upload (twine already installed)
twine upload dist/*.tar.gz dist/*.whl
```

## GitHub Release

```bash
# Push commit + tag

git push
git push --tags

# Create release

gh release create vX.Y.Z --title "vX.Y.Z" --notes "- summary"
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
