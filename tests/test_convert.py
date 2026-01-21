import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET
from pathlib import Path
import tempfile
import os

from normattiva2md.markdown_converter import (
    generate_markdown_text,
    clean_text_content,
    process_table,
    process_title,
    process_part,
    process_attachment,
    generate_front_matter,
)
from normattiva2md.xml_parser import extract_metadata_from_xml
from normattiva2md.normattiva_api import (
    validate_normattiva_url,
    is_normattiva_url,
    extract_params_from_normattiva_url,
    normalize_normattiva_url,
)
from normattiva2md.utils import sanitize_output_path
from normattiva2md.exa_api import lookup_normattiva_url
from normattiva2md.constants import MAX_FILE_SIZE_BYTES


FIXTURE_PATH = (
    Path(__file__).resolve().parents[1]
    / "test_data"
    / "20050516_005G0104_VIGENZA_20250130.xml"
)


class ConvertAkomaNtosoTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        tree = ET.parse(FIXTURE_PATH)
        root = tree.getroot()
        cls.markdown_output = generate_markdown_text(root)

    def test_document_title_is_rendered(self):
        self.assertTrue(
            self.markdown_output.startswith("# Codice dell'amministrazione digitale."),
            "Il titolo del documento dovrebbe essere renderizzato come intestazione H1",
        )

    def test_first_article_heading_is_present(self):
        self.assertIn(
            "## Art. 1. - Definizioni",
            self.markdown_output,
            "Il primo articolo dovrebbe contenere l'intestazione attesa",
        )

    def test_capitolo_heading_format(self):
        self.assertIn(
            "## Capo I - PRINCIPI GENERALI",
            self.markdown_output,
            "La formattazione del capitolo dovrebbe includere numero romano e titolo",
        )

    def test_footnote_element_handling(self):
        """Test that footnote elements are handled without errors"""
        # Create a simple XML element with footnote
        footnote_xml = """<akn:footnote xmlns:akn="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
            <akn:p>Test footnote content</akn:p>
        </akn:footnote>"""
        root = ET.fromstring(footnote_xml)
        result = clean_text_content(root)
        # Should not crash and should contain some reference
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)

    def test_quoted_structure_element_handling(self):
        """Test that quotedStructure elements are converted to blockquotes"""
        # Create a simple XML element with quotedStructure as block element
        quoted_xml = """<akn:quotedStructure xmlns:akn="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
            <akn:p>This is quoted text</akn:p>
        </akn:quotedStructure>"""
        root = ET.fromstring(quoted_xml)
        # Test the clean_text_content function directly on quotedStructure
        result = clean_text_content(root)
        # Should extract the text content
        self.assertIn("This is quoted text", result)

    def test_table_element_handling(self):
        """Test that table elements are converted to markdown tables"""
        # Create a simple XML table
        table_xml = """<akn:table xmlns:akn="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
            <akn:tr>
                <akn:th>Header 1</akn:th>
                <akn:th>Header 2</akn:th>
            </akn:tr>
            <akn:tr>
                <akn:td>Data 1</akn:td>
                <akn:td>Data 2</akn:td>
            </akn:tr>
        </akn:table>"""
        root = ET.fromstring(table_xml)
        ns = {"akn": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"}
        result = process_table(root, ns)
        # Should contain pipe characters for markdown table
        self.assertIn("|", result)
        self.assertIn("Header 1", result)
        self.assertIn("Data 1", result)

    def test_title_element_handling(self):
        """Test that title elements are converted to H2 headings"""
        # Create a simple XML title
        title_xml = """<akn:title xmlns:akn="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
            <akn:heading>TITOLO I</akn:heading>
            <akn:chapter>
                <akn:heading>Capo I DISPOSIZIONI GENERALI</akn:heading>
            </akn:chapter>
        </akn:title>"""
        root = ET.fromstring(title_xml)
        ns = {"akn": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"}
        result_fragments = process_title(root, ns)
        result = "".join(result_fragments)
        # Title should be H2
        self.assertIn("## TITOLO I", result)
        # Nested chapter (Capo) should be H2
        self.assertIn("## Capo I - DISPOSIZIONI GENERALI", result)

    def test_part_element_handling(self):
        """Test that part elements are converted to H2 headings"""
        # Create a simple XML part
        part_xml = """<akn:part xmlns:akn="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
            <akn:heading>Parte I - DISPOSIZIONI GENERALI</akn:heading>
        </akn:part>"""
        root = ET.fromstring(part_xml)
        ns = {"akn": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"}
        result_fragments = process_part(root, ns)
        result = "".join(result_fragments)
        # Should contain H1 heading (before global downgrade)
        self.assertIn("# Parte I - DISPOSIZIONI GENERALI", result)

    def test_attachment_element_handling(self):
        """Test that attachment elements are converted to separate sections"""
        # Create a simple XML attachment
        attachment_xml = """<akn:attachment xmlns:akn="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
            <akn:heading>Allegato A</akn:heading>
            <akn:article>
                <akn:num>Art. 1</akn:num>
                <akn:heading>Test Article</akn:heading>
            </akn:article>
        </akn:attachment>"""
        root = ET.fromstring(attachment_xml)
        ns = {"akn": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"}
        result_fragments = process_attachment(root, ns)
        result = "".join(result_fragments)
        # Should contain attachment section (H3 before global downgrade)
        self.assertIn("### Allegato A", result)
        # Should contain nested article
        self.assertIn("### Art. 1 - Test Article", result)

    def test_article_with_suffix_in_attachment(self):
        """Test articles with suffixes like -bis, -ter, -quater are on one line."""
        attachment_xml = """<akn:attachment xmlns:akn="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
            <akn:doc name="Test-art. 155 bis">
                <akn:mainBody>
                    <akn:paragraph>
                        <akn:content>
                            <akn:p>Art. 155-bis. (( ARTICOLO ABROGATO ))</akn:p>
                        </akn:content>
                    </akn:paragraph>
                </akn:mainBody>
            </akn:doc>
        </akn:attachment>"""
        root = ET.fromstring(attachment_xml)
        ns = {"akn": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"}
        result_fragments = process_attachment(root, ns)
        result = "".join(result_fragments)
        # Article number with suffix should be on one line
        self.assertIn("### Art. 155-bis.", result)
        # Should not be split across lines
        self.assertNotIn("### Art. 155\n\n-bis", result)

    def test_article_suffixes_variants(self):
        """Test various article suffix variants (ter, quater, quinquies, sexies)."""
        test_cases = [
            ("Art. 155-ter. Text", "### Art. 155-ter."),
            ("Art. 155-quater. Text", "### Art. 155-quater."),
            ("Art. 155-quinquies. Text", "### Art. 155-quinquies."),
            ("Art. 155-sexies. Text", "### Art. 155-sexies."),
        ]
        
        for article_text, expected in test_cases:
            with self.subTest(article=article_text):
                attachment_xml = f"""<akn:attachment xmlns:akn="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
                    <akn:doc>
                        <akn:mainBody>
                            <akn:paragraph>
                                <akn:content>
                                    <akn:p>{article_text}</akn:p>
                                </akn:content>
                            </akn:paragraph>
                        </akn:mainBody>
                    </akn:doc>
                </akn:attachment>"""
                root = ET.fromstring(attachment_xml)
                ns = {"akn": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"}
                result_fragments = process_attachment(root, ns)
                result = "".join(result_fragments)
                self.assertIn(expected, result)

    def test_generate_front_matter_complete(self):
        """Test front matter generation with complete metadata"""
        metadata = {
            "url": "https://example.com",
            "url_xml": "https://example.com/xml",
            "dataGU": "20231201",
            "codiceRedaz": "123ABC",
            "dataVigenza": "20231231",
        }
        result = generate_front_matter(metadata)
        expected = """---
legal_notice: I testi presenti nella banca dati "Normattiva" non hanno carattere di ufficialità. L'unico testo ufficiale è quello pubblicato sulla Gazzetta Ufficiale Italiana.
url: https://example.com
url_xml: https://example.com/xml
dataGU: 20231201
codiceRedaz: 123ABC
dataVigenza: 20231231
---

"""
        self.assertEqual(result, expected)

    def test_generate_front_matter_partial(self):
        """Test front matter generation with partial metadata"""
        metadata = {"url": "https://example.com", "dataGU": "20231201"}
        result = generate_front_matter(metadata)
        expected = """---
legal_notice: I testi presenti nella banca dati "Normattiva" non hanno carattere di ufficialità. L'unico testo ufficiale è quello pubblicato sulla Gazzetta Ufficiale Italiana.
url: https://example.com
dataGU: 20231201
---

"""
        self.assertEqual(result, expected)

    def test_generate_front_matter_empty(self):
        """Test front matter generation with no metadata"""
        metadata = {}
        result = generate_front_matter(metadata)
        self.assertEqual(result, "")

    def test_extract_metadata_from_xml(self):
        """Test metadata extraction from XML"""
        tree = ET.parse(FIXTURE_PATH)
        root = tree.getroot()
        metadata = extract_metadata_from_xml(root)

        # Check that expected fields are present
        self.assertIn("codiceRedaz", metadata)
        self.assertIn("dataGU", metadata)
        self.assertIn("dataVigenza", metadata)
        self.assertIn("url", metadata)
        self.assertIn("url_xml", metadata)

        # Check specific values
        self.assertEqual(metadata["codiceRedaz"], "005G0104")
        self.assertEqual(metadata["dataGU"], "20050307")
        self.assertEqual(metadata["dataVigenza"], "20250130")

    def test_output_includes_front_matter(self):
        """Test that the complete output includes front matter"""
        tree = ET.parse(FIXTURE_PATH)
        root = tree.getroot()
        metadata = extract_metadata_from_xml(root)
        markdown_with_frontmatter = generate_markdown_text(root, metadata=metadata)

        # Should start with front matter
        self.assertTrue(markdown_with_frontmatter.startswith("---"))
        self.assertIn("url:", markdown_with_frontmatter)
        self.assertIn("codiceRedaz: 005G0104", markdown_with_frontmatter)


class SecurityTests(unittest.TestCase):
    """Test security features: URL validation, path sanitization, file size limits"""

    def test_validate_normattiva_url_valid(self):
        """Test that valid normattiva.it HTTPS URLs are accepted"""
        valid_urls = [
            "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2022;53",
            "https://normattiva.it/do/atto/caricaAKN?test=123",
        ]
        for url in valid_urls:
            with self.subTest(url=url):
                # Should not raise exception
                self.assertTrue(validate_normattiva_url(url))

    def test_normalize_normattiva_url_removes_backslashes(self):
        """Test that escaped URLs are normalized"""
        escaped_url = "https://www.normattiva.it/uri-res/N2Ls\\?urn:nir:stato:legge:2005-03-10\\;33\\!vig\\=2026-01-12"
        expected_url = "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2005-03-10;33!vig=2026-01-12"
        self.assertEqual(normalize_normattiva_url(escaped_url), expected_url)
        self.assertTrue(validate_normattiva_url(escaped_url))
        self.assertTrue(is_normattiva_url(escaped_url))

    def test_validate_normattiva_url_rejects_http(self):
        """Test that HTTP (non-HTTPS) URLs are rejected"""
        with self.assertRaises(ValueError) as context:
            validate_normattiva_url("http://www.normattiva.it/test")
        self.assertIn("HTTPS", str(context.exception))

    def test_validate_normattiva_url_rejects_wrong_domain(self):
        """Test that URLs from other domains are rejected"""
        malicious_urls = [
            "https://evil.com/malware",
            "https://www.google.com/search",
            "https://normattiva.it.evil.com/fake",
        ]
        for url in malicious_urls:
            with self.subTest(url=url):
                with self.assertRaises(ValueError) as context:
                    validate_normattiva_url(url)
                self.assertIn("Dominio non consentito", str(context.exception))

    def test_is_normattiva_url_validates_security(self):
        """Test that is_normattiva_url rejects insecure URLs"""
        # HTTP should be rejected
        self.assertFalse(is_normattiva_url("http://www.normattiva.it/test"))
        # HTTPS should be accepted
        self.assertTrue(is_normattiva_url("https://www.normattiva.it/test"))
        # Wrong domain should be rejected
        self.assertFalse(is_normattiva_url("https://evil.com/test"))

    def test_sanitize_output_path_accepts_safe_paths(self):
        """Test that safe output paths are accepted"""
        safe_paths = [
            "output.md",
            "./output.md",
            "subdir/output.md",
            "/tmp/safe_output.md",
        ]
        for path in safe_paths:
            with self.subTest(path=path):
                # Should not raise exception
                result = sanitize_output_path(path)
                self.assertIsInstance(result, str)
                self.assertTrue(os.path.isabs(result))

    def test_sanitize_output_path_rejects_traversal(self):
        """Test that path traversal attempts are rejected"""
        malicious_paths = [
            "../../../etc/passwd",
            "/etc/passwd",
            "/sys/kernel/debug",
            "output/../../../etc/passwd",
        ]
        for path in malicious_paths:
            with self.subTest(path=path):
                with self.assertRaises(ValueError) as context:
                    sanitize_output_path(path)
                self.assertIn("Path non sicuro", str(context.exception))

    def test_sanitize_output_path_rejects_empty(self):
        """Test that empty paths are rejected"""
        with self.assertRaises(ValueError) as context:
            sanitize_output_path("")
        self.assertIn("vuoto", str(context.exception))

    def test_file_size_limit_constant_defined(self):
        """Test that file size limit constants are properly defined"""
        self.assertIsInstance(MAX_FILE_SIZE_BYTES, int)
        self.assertGreater(MAX_FILE_SIZE_BYTES, 0)
        # Should be reasonable (e.g., 50MB)
        self.assertGreater(MAX_FILE_SIZE_BYTES, 1024 * 1024)  # > 1MB
        self.assertLess(MAX_FILE_SIZE_BYTES, 1024 * 1024 * 1024)  # < 1GB


class URLLookupTest(unittest.TestCase):
    """Test cases for natural language URL lookup functionality"""

    def test_lookup_normattiva_url_with_mock_success(self):
        """Test successful URL lookup with mocked Exa API"""
        import unittest.mock as mock

        # Mock successful Exa API response
        mock_response = mock.MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [
                {
                    "url": "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2018-12-30;205",
                    "title": "Legge di Bilancio 2019",
                }
            ]
        }

        with mock.patch("os.getenv", return_value="fake-api-key"), mock.patch(
            "requests.post", return_value=mock_response
        ):
            result = lookup_normattiva_url("legge stanca")
            self.assertEqual(
                result,
                "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2018-12-30;205",
            )

    def test_lookup_normattiva_url_no_url_found(self):
        """Test when Exa API doesn't return valid results"""
        import unittest.mock as mock

        mock_response = mock.MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": []}

        with mock.patch("os.getenv", return_value="fake-api-key"), mock.patch(
            "requests.post", return_value=mock_response
        ):
            result = lookup_normattiva_url("legge inesistente")
            self.assertIsNone(result)

    def test_lookup_normattiva_url_exa_error(self):
        """Test when Exa API returns an error"""
        import unittest.mock as mock

        mock_response = mock.MagicMock()
        mock_response.status_code = 401
        mock_response.text = "Invalid API key"

        with mock.patch("os.getenv", return_value="fake-api-key"), mock.patch(
            "requests.post", return_value=mock_response
        ):
            result = lookup_normattiva_url("test query")
            self.assertIsNone(result)

    def test_lookup_normattiva_url_api_key_missing(self):
        """Test when Exa API key is not configured"""
        import unittest.mock as mock

        with mock.patch("os.getenv", return_value=None):
            result = lookup_normattiva_url("test query")
            self.assertIsNone(result)

    def test_lookup_normattiva_url_cli_api_key(self):
        """Test when Exa API key is provided via CLI parameter"""
        import unittest.mock as mock

        mock_response = mock.MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [
                {
                    "url": "https://normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2000-01-01;123"
                }
            ]
        }

        with mock.patch("os.getenv", return_value=None), mock.patch(
            "requests.post", return_value=mock_response
        ):
            result = lookup_normattiva_url("test query", exa_api_key="cli-api-key")
            self.assertEqual(
                result,
                "https://normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2000-01-01;123",
            )

    def test_lookup_normattiva_url_cli_precedence(self):
        """Test that CLI API key takes precedence over environment variable"""
        import unittest.mock as mock

        mock_response = mock.MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [
                {
                    "url": "https://normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2000-01-01;123"
                }
            ]
        }

        with mock.patch("os.getenv", return_value="env-api-key"), mock.patch(
            "requests.post", return_value=mock_response
        ) as mock_post:
            result = lookup_normattiva_url("test query", exa_api_key="cli-api-key")
            self.assertEqual(
                result,
                "https://normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2000-01-01;123",
            )
            # Verify CLI key was used in the request
            mock_post.assert_called_once()
            call_args = mock_post.call_args
            self.assertEqual(call_args[1]["headers"]["x-api-key"], "cli-api-key")

    def test_lookup_normattiva_url_invalid_results(self):
        """Test when Exa API returns results but no valid normattiva URLs"""
        import unittest.mock as mock

        mock_response = mock.MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [
                {"url": "https://example.com/page1"},
                {"url": "https://google.com/search"},
            ]
        }

        with mock.patch("os.getenv", return_value="fake-api-key"), mock.patch(
            "requests.post", return_value=mock_response
        ):
            result = lookup_normattiva_url("test query")
            self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
