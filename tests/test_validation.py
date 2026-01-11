import unittest
import textwrap
from normattiva2md.validation import MarkdownValidator, ReportGenerator

class TestMarkdownValidator(unittest.TestCase):
    def setUp(self):
        self.validator = MarkdownValidator()

    def test_validate_valid_markdown(self):
        # H1 -> H2 -> H4 (skipping H3) should be valid
        markdown = textwrap.dedent("""
            ---
            url: https://example.com
            dataGU: 20050307
            codiceRedaz: '105G0104'
            dataVigenza: 20251101
            ---

            # Titolo

            ## Capo I

            #### Art. 1
            """)
        result = self.validator.validate(markdown)
        self.assertEqual(result["status"], "PASS", f"Should pass but got errors: {result.get('errors')}")

    def test_fail_missing_front_matter(self):
        markdown = "# Titolo\n## Capo I"
        result = self.validator.validate(markdown)
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(any("front matter" in e["message"].lower() for e in result["errors"]))

    def test_fail_invalid_header_level(self):
        # H5 is not allowed
        markdown = textwrap.dedent("""
            ---
            url: https://example.com
            dataGU: 20050307
            codiceRedaz: '105G0104'
            dataVigenza: 20251101
            ---

            # Titolo
            ##### Invalid Level
            """)
        result = self.validator.validate(markdown)
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(any("h5" in e["message"].lower() or "level" in e["message"].lower() for e in result["errors"]))

    def test_fail_multiple_h1(self):
        markdown = textwrap.dedent("""
            ---
            url: https://example.com
            dataGU: 20050307
            codiceRedaz: '105G0104'
            dataVigenza: 20251101
            ---

            # Titolo 1
            # Titolo 2
            """)
        result = self.validator.validate(markdown)
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(any("multiple document titles" in e["message"].lower() for e in result["errors"]))

    def test_fail_missing_required_metadata(self):
        markdown = textwrap.dedent("""
            ---
            url: https://example.com
            ---
            # Titolo
            """)
        result = self.validator.validate(markdown)
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(any("metadata" in e["message"].lower() or "dataGU" in e["message"] for e in result["errors"]))

class TestReportGenerator(unittest.TestCase):
    def test_generate_json_report(self):
        generator = ReportGenerator()
        v_report = {"status": "PASS", "checks": []}
        c_report = {"status": "PASS", "message": "OK"}
        report_json = generator.generate_json(v_report, c_report, "sample.xml")
        import json
        report = json.loads(report_json)
        self.assertEqual(report["overall_status"], "PASS")
        self.assertEqual(report["source"], "sample.xml")

if __name__ == "__main__":
    unittest.main()
