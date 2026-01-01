"""
Test suite for normattiva2md API.

Run with: python -m pytest tests/test_api.py -v
"""

import sys
sys.path.insert(0, 'src')

import pytest

from normattiva2md import (
    ConversionResult,
    SearchResult,
    InvalidURLError,
    XMLFileNotFoundError,
    APIKeyError,
    ConversionError,
    Normattiva2MDError,
)


class TestModels:
    """Test data models."""

    def test_conversion_result_creation(self):
        """Test ConversionResult creation."""
        result = ConversionResult(
            markdown="# Test\n\nContent",
            metadata={"dataGU": "20220101", "codiceRedaz": "TEST"},
            url="https://www.normattiva.it/...",
            url_xml="https://www.normattiva.it/do/atto/caricaAKN?...",
        )

        assert result.markdown == "# Test\n\nContent"
        assert result.metadata["dataGU"] == "20220101"
        assert result.url is not None

    def test_conversion_result_str(self):
        """Test ConversionResult string conversion."""
        result = ConversionResult(
            markdown="# Test",
            metadata={},
        )

        assert str(result) == "# Test"

    def test_conversion_result_title_property(self):
        """Test title extraction from markdown."""
        result = ConversionResult(
            markdown="# Legge 9 gennaio 2004, n. 4\n\nContenuto...",
            metadata={},
        )

        assert result.title == "Legge 9 gennaio 2004, n. 4"

    def test_conversion_result_title_not_found(self):
        """Test title when no H1 present."""
        result = ConversionResult(
            markdown="Contenuto senza titolo H1",
            metadata={},
        )

        assert result.title is None

    def test_conversion_result_metadata_shortcuts(self):
        """Test metadata property shortcuts."""
        result = ConversionResult(
            markdown="",
            metadata={
                "dataGU": "20220101",
                "codiceRedaz": "22G00001",
                "dataVigenza": "20250101",
            },
        )

        assert result.data_gu == "20220101"
        assert result.codice_redaz == "22G00001"
        assert result.data_vigenza == "20250101"

    def test_search_result_creation(self):
        """Test SearchResult creation."""
        result = SearchResult(
            url="https://www.normattiva.it/...",
            title="Legge 4/2004",
            score=0.95,
        )

        assert result.url.startswith("https://")
        assert result.title == "Legge 4/2004"
        assert result.score == 0.95

    def test_search_result_str(self):
        """Test SearchResult string representation."""
        result = SearchResult(
            url="https://...",
            title="Legge 4/2004",
            score=0.95,
        )

        assert str(result) == "[0.95] Legge 4/2004"


class TestExceptions:
    """Test exception hierarchy."""

    def test_exception_hierarchy(self):
        """Test that all exceptions derive from base."""
        assert issubclass(InvalidURLError, Normattiva2MDError)
        assert issubclass(XMLFileNotFoundError, Normattiva2MDError)
        assert issubclass(APIKeyError, Normattiva2MDError)
        assert issubclass(ConversionError, Normattiva2MDError)

    def test_catch_base_exception(self):
        """Test catching all errors with base class."""
        with pytest.raises(Normattiva2MDError):
            raise InvalidURLError("test")

        with pytest.raises(Normattiva2MDError):
            raise ConversionError("test")

    def test_exception_message(self):
        """Test exception messages."""
        exc = InvalidURLError("URL non valido: test.com")
        assert "URL non valido" in str(exc)


class TestImports:
    """Test that all public API is importable."""

    def test_import_functions(self):
        """Test importing standalone functions."""
        from normattiva2md import convert_url, convert_xml, search_law

        assert callable(convert_url)
        assert callable(convert_xml)
        assert callable(search_law)

    def test_import_class(self):
        """Test importing Converter class."""
        from normattiva2md import Converter

        assert Converter is not None

    def test_import_models(self):
        """Test importing data models."""
        from normattiva2md import ConversionResult, SearchResult

        assert ConversionResult is not None
        assert SearchResult is not None

    def test_import_exceptions(self):
        """Test importing exceptions."""
        from normattiva2md import (
            Normattiva2MDError,
            InvalidURLError,
            XMLFileNotFoundError,
            APIKeyError,
            ConversionError,
        )

        assert all([
            Normattiva2MDError,
            InvalidURLError,
            XMLFileNotFoundError,
            APIKeyError,
            ConversionError,
        ])

    def test_import_version(self):
        """Test importing version."""
        from normattiva2md import __version__

        assert __version__ is not None
        assert isinstance(__version__, str)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
