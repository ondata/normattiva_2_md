import unittest
import xml.etree.ElementTree as ET
from normattiva2md.validation import StructureComparer

class TestStructureComparer(unittest.TestCase):
    def setUp(self):
        self.comparer = StructureComparer()

    def test_compare_matching_articles(self):
        xml_content = """
        <nir>
            <legge>
                <art>
                    <num>Art. 1.</num>
                </art>
                <art>
                    <num>Art. 2.</num>
                </art>
            </legge>
        </nir>
        """
        root = ET.fromstring(xml_content)
        markdown = """
# Titolo

#### Art. 1.
Testo articolo 1.

#### Art. 2.
Testo articolo 2.
"""
        result = self.comparer.compare(root, markdown)
        self.assertEqual(result["status"], "PASS")

    def test_compare_mismatch_articles(self):
        xml_content = """
        <nir>
            <legge>
                <art>
                    <num>Art. 1.</num>
                </art>
                <art>
                    <num>Art. 2.</num>
                </art>
            </legge>
        </nir>
        """
        root = ET.fromstring(xml_content)
        # Markdown only has Art. 1
        markdown = """
# Titolo

#### Art. 1.
Testo articolo 1.
"""
        result = self.comparer.compare(root, markdown)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("Article count mismatch", result["message"])
        self.assertEqual(result["details"]["xml_count"], 2)
        self.assertEqual(result["details"]["md_count"], 1)

if __name__ == "__main__":
    unittest.main()
