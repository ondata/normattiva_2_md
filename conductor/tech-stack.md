# Technology Stack - Normattiva2MD

## Core Language & Runtime
- **Python (3.7+):** The primary programming language, chosen for its strong support for text processing, XML handling, and wide adoption in the AI/Data Science community.

## Libraries & Frameworks
- **Requests:** Used for all network interactions, including downloading XML from Normattiva and querying the Exa AI API.
- **Standard Library (xml.etree.ElementTree):** Utilized for parsing Akoma Ntoso XML documents, maintaining a minimalist footprint.
- **Standard Library (json, re):** Used for structural validation and report generation.
- **Setuptools / Pyproject.toml:** Used for package management, dependency definition, and distribution to PyPI.

## External APIs & Integrations
- **Normattiva.it (Akoma Ntoso):** The primary data source for Italian legislation.
- **Exa AI API:** Integrated to provide natural language search capabilities, allowing users to find laws without knowing the exact URN or URL.

## Development & Distribution Tools
- **PyInstaller:** Used to generate standalone, cross-platform binaries for users who do not have a Python environment.
- **Makefile:** Provides a consistent interface for common tasks like testing, building, and cleaning the project.
