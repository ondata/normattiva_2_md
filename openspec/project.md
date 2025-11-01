# Project Context

## Purpose
Akoma2MD is a command-line tool that converts Akoma Ntoso XML documents (particularly Italian legal documents from normattiva.it) into readable Markdown format. The primary goal is to provide legal documents in a format optimized for Large Language Models (LLMs) and AI applications, enabling better legal analysis, Q&A systems, and automated processing.

## Tech Stack
- **Language**: Python 3.7+
- **Packaging**: pyproject.toml (modern Python packaging)
- **CLI Framework**: argparse (standard library)
- **Build Tools**: PyInstaller (standalone executables), setuptools
- **Testing**: unittest (standard library)
- **CI/CD**: GitHub Actions
- **Dependencies**: requests>=2.25.0 (only external dependency)

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

### Architecture Patterns
- **CLI-first design**: Native command-line interface with flexible argument parsing
- **Modular conversion**: Separate functions for different XML element types
- **Streaming processing**: Handle large XML documents efficiently
- **Hierarchical structure preservation**: Maintain legal document organization (chapters, articles, paragraphs)
- **URL-aware processing**: Automatic detection and downloading of normattiva.it URLs

### Testing Strategy
- **Unit tests**: unittest framework for core conversion functions
- **Integration tests**: Makefile-based testing of CLI functionality
- **Test data**: Real XML samples from normattiva.it in test_data/ directory
- **Cross-platform verification**: Test both Python script and PyInstaller executables
- **Coverage**: Test conversion of various legal document structures

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

## Important Constraints
- **Python compatibility**: Must work on Python 3.7+ (no modern features like type hints)
- **Zero external dependencies**: Only requests library allowed beyond standard library
- **Cross-platform**: Linux and Windows executable distribution
- **Legal accuracy**: Preserve exact legal text and structure during conversion
- **Performance**: Handle large legal documents efficiently

## External Dependencies
- **normattiva.it**: Italian official legal document repository for URL-based document fetching
- **PyPI**: Package distribution and installation
- **GitHub**: Repository hosting, issue tracking, and CI/CD pipelines
