import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from convert_akomantoso import generate_markdown_text


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
            "# Art. 1. - Definizioni",
            self.markdown_output,
            "Il primo articolo dovrebbe contenere l'intestazione attesa",
        )

    def test_capitolo_heading_format(self):
        self.assertIn(
            "## Capo I - PRINCIPI GENERALI",
            self.markdown_output,
            "La formattazione del capitolo dovrebbe includere numero romano e titolo",
        )


if __name__ == "__main__":
    unittest.main()
