import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from normattiva2md.markdown_converter import generate_markdown_text, process_content_with_paragraphs

AKN_NS = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"
NS = {"akn": AKN_NS}

FIXTURE_PATH = (
    Path(__file__).resolve().parents[1]
    / "test_data"
    / "20050516_005G0104_VIGENZA_20250130.xml"
)


class NoNotesTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        tree = ET.parse(FIXTURE_PATH)
        cls.root = tree.getroot()

    def test_aggiornamento_present_by_default(self):
        md = generate_markdown_text(self.root, no_notes=False)
        self.assertIn("AGGIORNAMENTO", md)

    def test_aggiornamento_absent_with_no_notes(self):
        md = generate_markdown_text(self.root, no_notes=True)
        self.assertNotIn("AGGIORNAMENTO", md)

    def test_double_parens_preserved_with_no_notes(self):
        """Inline modifications (( )) must survive --no-notes."""
        md = generate_markdown_text(self.root, no_notes=True)
        self.assertIn("((", md)

    def test_process_content_skips_aggiornamento(self):
        xml_str = (
            f'<content xmlns="{AKN_NS}">'
            "<p>------------</p>"
            "<p>AGGIORNAMENTO (1)</p>"
            "<p>Testo della nota storica.</p>"
            "</content>"
        )
        elem = ET.fromstring(xml_str)
        result = process_content_with_paragraphs(elem, NS, no_notes=True)
        self.assertEqual(result, "")

    def test_process_content_keeps_regular_text(self):
        xml_str = (
            f'<content xmlns="{AKN_NS}">'
            "<p>Testo normativo vigente.</p>"
            "</content>"
        )
        elem = ET.fromstring(xml_str)
        result = process_content_with_paragraphs(elem, NS, no_notes=True)
        self.assertIn("Testo normativo vigente.", result)

    def test_process_content_default_includes_aggiornamento(self):
        xml_str = (
            f'<content xmlns="{AKN_NS}">'
            "<p>AGGIORNAMENTO (5)</p>"
            "<p>Nota.</p>"
            "</content>"
        )
        elem = ET.fromstring(xml_str)
        result = process_content_with_paragraphs(elem, NS, no_notes=False)
        self.assertIn("AGGIORNAMENTO", result)


if __name__ == "__main__":
    unittest.main()
