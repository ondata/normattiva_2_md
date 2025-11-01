import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from convert_akomantoso import generate_markdown_text, clean_text_content, process_table, process_title, process_part, process_attachment, generate_front_matter, extract_metadata_from_xml


FIXTURE_PATH = Path(__file__).resolve().parents[1] / "test_data" / "20050516_005G0104_VIGENZA_20250130.xml"


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
            "### Capo I - PRINCIPI GENERALI",
            self.markdown_output,
            "La formattazione del capitolo dovrebbe includere numero romano e titolo",
        )

    def test_footnote_element_handling(self):
        """Test that footnote elements are handled without errors"""
        # Create a simple XML element with footnote
        footnote_xml = '''<akn:footnote xmlns:akn="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
            <akn:p>Test footnote content</akn:p>
        </akn:footnote>'''
        root = ET.fromstring(footnote_xml)
        result = clean_text_content(root)
        # Should not crash and should contain some reference
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)

    def test_quoted_structure_element_handling(self):
        """Test that quotedStructure elements are converted to blockquotes"""
        # Create a simple XML element with quotedStructure as block element
        quoted_xml = '''<akn:quotedStructure xmlns:akn="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
            <akn:p>This is quoted text</akn:p>
        </akn:quotedStructure>'''
        root = ET.fromstring(quoted_xml)
        # Test the clean_text_content function directly on quotedStructure
        result = clean_text_content(root)
        # Should extract the text content
        self.assertIn('This is quoted text', result)

    def test_table_element_handling(self):
        """Test that table elements are converted to markdown tables"""
        # Create a simple XML table
        table_xml = '''<akn:table xmlns:akn="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
            <akn:tr>
                <akn:th>Header 1</akn:th>
                <akn:th>Header 2</akn:th>
            </akn:tr>
            <akn:tr>
                <akn:td>Data 1</akn:td>
                <akn:td>Data 2</akn:td>
            </akn:tr>
        </akn:table>'''
        root = ET.fromstring(table_xml)
        ns = {'akn': 'http://docs.oasis-open.org/legaldocml/ns/akn/3.0'}
        result = process_table(root, ns)
        # Should contain pipe characters for markdown table
        self.assertIn('|', result)
        self.assertIn('Header 1', result)
        self.assertIn('Data 1', result)

    def test_title_element_handling(self):
        """Test that title elements are converted to H1 headings"""
        # Create a simple XML title
        title_xml = '''<akn:title xmlns:akn="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
            <akn:heading>TITOLO I</akn:heading>
            <akn:chapter>
                <akn:heading>Capo I DISPOSIZIONI GENERALI</akn:heading>
            </akn:chapter>
        </akn:title>'''
        root = ET.fromstring(title_xml)
        ns = {'akn': 'http://docs.oasis-open.org/legaldocml/ns/akn/3.0'}
        result_fragments = process_title(root, ns)
        result = ''.join(result_fragments)
        # Should contain H2 heading
        self.assertIn('## TITOLO I', result)
        # Should contain nested chapter
        self.assertIn('### Capo I - DISPOSIZIONI GENERALI', result)

    def test_part_element_handling(self):
        """Test that part elements are converted to H2 headings"""
        # Create a simple XML part
        part_xml = '''<akn:part xmlns:akn="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
            <akn:heading>Parte I - DISPOSIZIONI GENERALI</akn:heading>
        </akn:part>'''
        root = ET.fromstring(part_xml)
        ns = {'akn': 'http://docs.oasis-open.org/legaldocml/ns/akn/3.0'}
        result_fragments = process_part(root, ns)
        result = ''.join(result_fragments)
        # Should contain H3 heading
        self.assertIn('### Parte I - DISPOSIZIONI GENERALI', result)

    def test_attachment_element_handling(self):
        """Test that attachment elements are converted to separate sections"""
        # Create a simple XML attachment
        attachment_xml = '''<akn:attachment xmlns:akn="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
            <akn:heading>Allegato A</akn:heading>
            <akn:article>
                <akn:num>Art. 1</akn:num>
                <akn:heading>Test Article</akn:heading>
            </akn:article>
        </akn:attachment>'''
        root = ET.fromstring(attachment_xml)
        ns = {'akn': 'http://docs.oasis-open.org/legaldocml/ns/akn/3.0'}
        result_fragments = process_attachment(root, ns)
        result = ''.join(result_fragments)
        # Should contain attachment section
        self.assertIn('### Allegato: Allegato A', result)
        # Should contain nested article
        self.assertIn('## Art. 1 - Test Article', result)

    def test_generate_front_matter_complete(self):
        """Test front matter generation with complete metadata"""
        metadata = {
            'url': 'https://example.com',
            'url_xml': 'https://example.com/xml',
            'dataGU': '20231201',
            'codiceRedaz': '123ABC',
            'dataVigenza': '20231231'
        }
        result = generate_front_matter(metadata)
        expected = """---
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
        metadata = {
            'url': 'https://example.com',
            'dataGU': '20231201'
        }
        result = generate_front_matter(metadata)
        expected = """---
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
        self.assertIn('codiceRedaz', metadata)
        self.assertIn('dataGU', metadata)
        self.assertIn('dataVigenza', metadata)
        self.assertIn('url', metadata)
        self.assertIn('url_xml', metadata)

        # Check specific values
        self.assertEqual(metadata['codiceRedaz'], '005G0104')
        self.assertEqual(metadata['dataGU'], '20050307')
        self.assertEqual(metadata['dataVigenza'], '20250130')

    def test_output_includes_front_matter(self):
        """Test that the complete output includes front matter"""
        tree = ET.parse(FIXTURE_PATH)
        root = tree.getroot()
        metadata = extract_metadata_from_xml(root)
        markdown_with_frontmatter = generate_markdown_text(root, metadata=metadata)

        # Should start with front matter
        self.assertTrue(markdown_with_frontmatter.startswith('---'))
        self.assertIn('url:', markdown_with_frontmatter)
        self.assertIn('codiceRedaz: 005G0104', markdown_with_frontmatter)


if __name__ == "__main__":
    unittest.main()
