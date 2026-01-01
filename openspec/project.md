# Project Context

## Project Information
- **Name**: normattiva2md
- **Current Version**: 2.0.21
- **Author**: Andrea Borruso <aborruso@gmail.com>
- **Repository**: https://github.com/ondata/normattiva_2_md
- **License**: MIT

## Purpose
Normattiva2MD (formerly Akoma2MD) is a command-line tool that converts Akoma Ntoso XML documents (particularly Italian legal documents from normattiva.it) into readable Markdown format. The primary goal is to provide legal documents in a format optimized for Large Language Models (LLMs) and AI applications, enabling better legal analysis, Q&A systems, and automated processing.

## Tech Stack
- **Language**: Python 3.7+
- **Packaging**: pyproject.toml (modern Python packaging), setuptools>=45, wheel, setuptools_scm[toml]>=6.2
- **CLI Framework**: argparse (standard library)
- **Build Tools**: PyInstaller (standalone executables), setuptools, Makefile for automation
- **Testing**: unittest (standard library)
- **CI/CD**: GitHub Actions
- **Dependencies**: requests>=2.25.0, rich>=13.0.0,<14.0.0
- **External APIs**: Exa AI API for natural language document search
- **Package Distribution**: PyPI (https://pypi.org/project/normattiva2md/)

## Project Conventions

### Code Style
- **Formatting**: PEP 8 compliant, 4-space indentation, 88-character line length
- **Naming**: snake_case for functions/variables, UPPER_SNAKE_CASE for constants
- **Imports**: Standard library first, then third-party, alphabetical within groups
- **Types**: No type hints (maintains Python 3.7+ compatibility)
- **Docstrings**: Google-style format with Args/Returns for public functions
- **Error handling**: Use try/except, print errors to stderr, return None/False on failure
- **Dependencies**: Keep minimal; only add to setup.py/pyproject.toml if essential
- **Regex/XPath**: Comment non-obvious patterns inline
- **CLI args**: Use argparse, support both positional and named flags
- **Dual CLI support**: Maintain both `akoma2md` (legacy) and `normattiva2md` (preferred) commands

### Architecture Patterns
- **CLI-first design**: Native command-line interface with flexible argument parsing and article filtering (--art flag)
- **Modular conversion**: Separate functions for different XML element types
- **Streaming processing**: Handle large XML documents efficiently
- **Hierarchical structure preservation**: Maintain legal document organization (chapters, articles, paragraphs)
- **URL-aware processing**: Automatic detection and downloading of normattiva.it URLs
- **AI-powered search**: Natural language lookup using Exa AI API for document discovery
- **Cross-reference system**: Automatic download and linking of cited legal documents
- **Programmable API**: Modular Python API (api.py, models.py, exceptions.py) with standalone functions (convert_url, convert_xml, search_law) for integration in scripts and applications

### Testing Strategy
- **Unit tests**: unittest framework for core conversion functions
- **Integration tests**: Makefile-based testing of CLI functionality
- **Test data**: Real XML samples from normattiva.it in test_data/ directory
- **Cross-platform verification**: Test both Python script and PyInstaller executables
- **Coverage**: Test conversion of various legal document structures
- **Make commands**:
  - `make test` - Run all tests (unittest + integration tests)
  - `make build` - Build standalone executable with PyInstaller
  - `make install` - Install package locally for development
  - `make package` - Create distribution packages (sdist + wheel)
  - `make clean` - Remove temporary files and build artifacts

### Git Workflow
- **Change tracking**: LOG.md file with YYYY-MM-DD dated entries for significant changes
- **Release process**: Version tags trigger GitHub Actions for automated binary builds
- **Branching**: Feature branches for new functionality (`git checkout -b feature/description`)
- **Commits**: Concise, descriptive messages focusing on what changed
- **Releases**: Semantic versioning with automated PyPI publishing and binary distribution

## Domain Context
- **Akoma Ntoso**: XML standard for legal documents, used by many governments worldwide
- **Italian legal system**: Focus on documents from normattiva.it (official Italian legal database)
- **Document structures**: Laws, decrees, regulations with hierarchical organization (preamble, chapters, articles, paragraphs)
- **Legal amendments**: Special handling of text modifications with ((double parentheses)) notation
- **Markdown optimization**: Format designed for LLM consumption, maintaining readability for both humans and AI systems
- **Metadata extraction**: YAML front matter with document metadata (dates, URLs, references)
- **Entry-into-force tracking**: Automatic extraction of law effectiveness dates from XML notes

## Important Constraints
- **Python compatibility**: Must work on Python 3.7+ through 3.12+ (no modern features like type hints)
- **Minimal external dependencies**: Only requests>=2.25.0 library allowed beyond standard library
- **Cross-platform**: Linux and Windows executable distribution via PyInstaller
- **Legal accuracy**: Preserve exact legal text and structure during conversion
- **Performance**: Handle large legal documents efficiently
- **Dual CLI naming**: Maintain both `normattiva2md` (preferred) and `akoma2md` (legacy) commands
- **Version synchronization**: Keep version strings aligned across pyproject.toml, setup.py, and convert_akomantoso.py

## External Dependencies
- **normattiva.it**: Italian official legal document repository for URL-based document fetching
- **Exa AI**: Search API for natural language document discovery
- **PyPI**: Package distribution and installation
- **GitHub**: Repository hosting, issue tracking, and CI/CD pipelines
