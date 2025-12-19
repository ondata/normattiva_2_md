import unittest
from src.normattiva2md.validation import MarkdownValidator

class TestMarkdownValidator(unittest.TestCase):
    def setUp(self):
        self.validator = MarkdownValidator()

    def test_validate_valid_markdown(self):
        # H1 -> H2 -> H4 (skipping H3) should be valid
        markdown = """---\nurl: https://example.com\ndataGU: 20050307\ncodiceRedaz: '105G0104'\ndataVigenza: 20251101\n---\n\n# Titolo\n\n## Capo I\n\n#### Art. 1\n"""
        result = self.validator.validate(markdown)
        self.assertEqual(result["status"], "PASS", f"Should pass but got errors: {result.get('errors')}")

    def test_fail_missing_front_matter(self):
        markdown = "# Titolo\n## Capo I"
        result = self.validator.validate(markdown)
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(any("front matter" in e["message"].lower() for e in result["errors"]))

    def test_fail_invalid_header_level(self):
        # H5 is not allowed
        markdown = """--- \nurl: https://example.com\ndataGU: 20050307\ncodiceRedaz: '105G0104'\ndataVigenza: 20251101\n--- \n\n# Titolo\n##### Invalid Level\n"""
        result = self.validator.validate(markdown)
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(any("h5" in e["message"].lower() or "level" in e["message"].lower() for e in result["errors"]))

    def test_fail_multiple_h1(self):
        markdown = """--- \nurl: https://example.com\ndataGU: 20050307\ncodiceRedaz: '105G0104'\ndataVigenza: 20251101\n--- \n\n# Titolo 1\n# Titolo 2\n"""
        result = self.validator.validate(markdown)
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(any("multiple document titles" in e["message"].lower() for e in result["errors"]))

    def test_fail_missing_required_metadata(self):
        markdown = """--- \nurl: https://example.com\n--- \n# Titolo\n"""
        result = self.validator.validate(markdown)
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(any("metadata" in e["message"].lower() or "dataGU" in e["message"] for e in result["errors"]))

if __name__ == "__main__":
    unittest.main()
