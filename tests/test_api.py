"""
Test suite for normattiva2md API.

Run with: python -m unittest tests/test_api.py -v
"""

import sys
sys.path.insert(0, 'src')

import unittest

from normattiva2md import (
    ConversionResult,
    SearchResult,
    InvalidURLError,
    XMLFileNotFoundError,
    APIKeyError,
    ConversionError,
    Normattiva2MDError,
)


class TestModels(unittest.TestCase):
    """Test data models."""

    def test_conversion_result_creation(self):
        """Test ConversionResult creation."""
        result = ConversionResult(
            markdown="# Test\n\nContent",
            metadata={"dataGU": "20220101", "codiceRedaz": "TEST"},
            url="https://www.normattiva.it/...",
            url_xml="https://www.normattiva.it/do/atto/caricaAKN?...",
        )

        self.assertEqual(result.markdown, "# Test\n\nContent")
        self.assertEqual(result.metadata["dataGU"], "20220101")
        self.assertIsNotNone(result.url)

    def test_conversion_result_str(self):
        """Test ConversionResult string conversion."""
        result = ConversionResult(
            markdown="# Test",
            metadata={},
        )

        self.assertEqual(str(result), "# Test")

    def test_conversion_result_title_property(self):
        """Test title extraction from markdown."""
        result = ConversionResult(
            markdown="# Legge 9 gennaio 2004, n. 4\n\nContenuto...",
            metadata={},
        )

        self.assertEqual(result.title, "Legge 9 gennaio 2004, n. 4")

    def test_conversion_result_title_not_found(self):
        """Test title when no H1 present."""
        result = ConversionResult(
            markdown="Contenuto senza titolo H1",
            metadata={},
        )

        self.assertIsNone(result.title)

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

        self.assertEqual(result.data_gu, "20220101")
        self.assertEqual(result.codice_redaz, "22G00001")
        self.assertEqual(result.data_vigenza, "20250101")

    def test_search_result_creation(self):
        """Test SearchResult creation."""
        result = SearchResult(
            url="https://www.normattiva.it/...",
            title="Legge 4/2004",
            score=0.95,
        )

        self.assertTrue(result.url.startswith("https://"))
        self.assertEqual(result.title, "Legge 4/2004")
        self.assertEqual(result.score, 0.95)

    def test_search_result_str(self):
        """Test SearchResult string representation."""
        result = SearchResult(
            url="https://...",
            title="Legge 4/2004",
            score=0.95,
        )

        self.assertEqual(str(result), "[0.95] Legge 4/2004")


class TestExceptions(unittest.TestCase):
    """Test exception hierarchy."""

    def test_exception_hierarchy(self):
        """Test that all exceptions derive from base."""
        self.assertTrue(issubclass(InvalidURLError, Normattiva2MDError))
        self.assertTrue(issubclass(XMLFileNotFoundError, Normattiva2MDError))
        self.assertTrue(issubclass(APIKeyError, Normattiva2MDError))
        self.assertTrue(issubclass(ConversionError, Normattiva2MDError))

    def test_catch_base_exception(self):
        """Test catching all errors with base class."""
        with self.assertRaises(Normattiva2MDError):
            raise InvalidURLError("test")

        with self.assertRaises(Normattiva2MDError):
            raise ConversionError("test")

    def test_exception_message(self):
        """Test exception messages."""
        exc = InvalidURLError("URL non valido: test.com")
        self.assertIn("URL non valido", str(exc))


class TestImports(unittest.TestCase):
    """Test that all public API is importable."""

    def test_import_functions(self):
        """Test importing standalone functions."""
        from normattiva2md import convert_url, convert_xml, search_law

        self.assertTrue(callable(convert_url))
        self.assertTrue(callable(convert_xml))
        self.assertTrue(callable(search_law))

    def test_import_class(self):
        """Test importing Converter class."""
        from normattiva2md import Converter

        self.assertIsNotNone(Converter)

    def test_import_models(self):
        """Test importing data models."""
        from normattiva2md import ConversionResult, SearchResult

        self.assertIsNotNone(ConversionResult)
        self.assertIsNotNone(SearchResult)

    def test_import_exceptions(self):
        """Test importing exceptions."""
        from normattiva2md import (
            Normattiva2MDError,
            InvalidURLError,
            XMLFileNotFoundError,
            APIKeyError,
            ConversionError,
        )

        self.assertTrue(all([
            Normattiva2MDError,
            InvalidURLError,
            XMLFileNotFoundError,
            APIKeyError,
            ConversionError,
        ]))

    def test_import_version(self):
        """Test importing version."""
        from normattiva2md import __version__

        self.assertIsNotNone(__version__)
        self.assertIsInstance(__version__, str)


if __name__ == "__main__":
    unittest.main()
