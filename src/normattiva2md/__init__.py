"""
normattiva2md - Convert Akoma Ntoso XML to Markdown

A CLI tool and Python library for converting Italian legal documents
from normattiva.it to LLM-friendly Markdown format.

CLI usage:
    normattiva2md input.xml output.md
    normattiva2md "https://www.normattiva.it/..." output.md

API usage:
    >>> from normattiva2md import convert_url
    >>> result = convert_url("https://www.normattiva.it/...")
    >>> print(result.markdown)
    >>> result.save("output.md")

    >>> from normattiva2md import Converter
    >>> conv = Converter(quiet=True)
    >>> result = conv.search_and_convert("legge stanca")
"""

from .api import Converter, convert_url, convert_xml, search_law
from .constants import VERSION
from .exceptions import (
    APIKeyError,
    ConversionError,
    InvalidURLError,
    Normattiva2MDError,
    XMLFileNotFoundError,
)
from .models import ConversionResult, SearchResult

__version__ = VERSION
__all__ = [
    # Core functions
    "convert_url",
    "convert_xml",
    "search_law",
    # Classes
    "Converter",
    "ConversionResult",
    "SearchResult",
    # Exceptions
    "Normattiva2MDError",
    "InvalidURLError",
    "XMLFileNotFoundError",
    "APIKeyError",
    "ConversionError",
    # Version
    "__version__",
]
