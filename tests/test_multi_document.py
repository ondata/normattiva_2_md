import os
import tempfile
import unittest
from unittest import mock

from normattiva2md import multi_document


class TestMultiDocument(unittest.TestCase):
    def test_build_cross_references_mapping_from_urls(self):
        mapping = {"https://a": "refs/a.md"}
        self.assertEqual(
            multi_document.build_cross_references_mapping_from_urls(mapping), mapping
        )

    def test_create_index_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            refs_path = os.path.join(tmpdir, "refs")
            os.makedirs(refs_path, exist_ok=True)
            with open(os.path.join(refs_path, "a.md"), "w", encoding="utf-8") as f:
                f.write("a")

            params = {"codiceRedaz": "X", "dataGU": "20200101"}
            multi_document.create_index_file(
                tmpdir, params, {"u1"}, successful=1, failed=0
            )

            index_path = os.path.join(tmpdir, "index.md")
            self.assertTrue(os.path.exists(index_path))
            with open(index_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn("Raccolta Legislativa", content)
            self.assertIn("main.md", content)
            self.assertIn("refs/a.md", content)

    def test_convert_with_references_success(self):
        def fake_convert(xml_path, md_path, metadata=None, cross_references=None):
            with open(md_path, "w", encoding="utf-8") as f:
                f.write("ok")
            return True

        params = {
            "dataGU": "20200101",
            "codiceRedaz": "X",
            "dataVigenza": "20200102",
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            with mock.patch.object(
                multi_document, "extract_params_from_normattiva_url", return_value=(params, object())
            ), mock.patch.object(
                multi_document, "download_akoma_ntoso", return_value=True
            ), mock.patch.object(
                multi_document, "extract_cited_laws", return_value={"https://a", "https://b"}
            ), mock.patch.object(
                multi_document,
                "convert_akomantoso_to_markdown_improved",
                side_effect=fake_convert,
            ), mock.patch.object(
                multi_document.time, "sleep"
            ):
                success = multi_document.convert_with_references(
                    "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2020;1",
                    output_dir=tmpdir,
                    quiet=True,
                )

            self.assertTrue(success)
            self.assertTrue(os.path.exists(os.path.join(tmpdir, "main.md")))
            self.assertTrue(os.path.exists(os.path.join(tmpdir, "index.md")))
            refs_dir = os.path.join(tmpdir, "refs")
            self.assertTrue(os.listdir(refs_dir))

    def test_convert_with_references_no_params(self):
        with mock.patch.object(
            multi_document, "extract_params_from_normattiva_url", return_value=(None, None)
        ):
            success = multi_document.convert_with_references(
                "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2020;1",
                output_dir="/tmp",
                quiet=True,
            )
        self.assertFalse(success)


if __name__ == "__main__":
    unittest.main()
