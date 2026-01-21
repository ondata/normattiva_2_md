import os
import tempfile
import unittest
from unittest import mock

from normattiva2md import cli


class TestCliMore(unittest.TestCase):
    def test_provvedimenti_requires_url(self):
        with mock.patch("sys.argv", ["normattiva2md", "input.xml", "--provvedimenti"]):
            with self.assertRaises(SystemExit):
                cli.main()

    def test_with_references_requires_url(self):
        with mock.patch("sys.argv", ["normattiva2md", "input.xml", "--with-references"]):
            with self.assertRaises(SystemExit):
                cli.main()

    def test_local_file_conversion_success(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "doc.xml")
            with open(input_path, "w", encoding="utf-8") as f:
                f.write("<root/>")

            with mock.patch(
                "normattiva2md.cli.convert_akomantoso_to_markdown_improved",
                return_value=True,
            ):
                with mock.patch(
                    "sys.argv", ["normattiva2md", input_path, os.path.join(tmpdir, "out.md")]
                ):
                    cli.main()

    def test_local_file_conversion_failure_exits(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "doc.xml")
            with open(input_path, "w", encoding="utf-8") as f:
                f.write("<root/>")

            with mock.patch(
                "normattiva2md.cli.convert_akomantoso_to_markdown_improved",
                return_value=False,
            ):
                with mock.patch(
                    "sys.argv", ["normattiva2md", input_path, os.path.join(tmpdir, "out.md")]
                ):
                    with self.assertRaises(SystemExit):
                        cli.main()

    def test_url_conversion_happy_path(self):
        params = {
            "dataGU": "20200101",
            "codiceRedaz": "X",
            "dataVigenza": "20200102",
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            fd, temp_file = tempfile.mkstemp(dir=tmpdir, suffix=".xml")

            with mock.patch("sys.argv", ["normattiva2md", "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2020;1", "-o", os.path.join(tmpdir, "out.md")]), mock.patch(
                "normattiva2md.cli.is_normattiva_url", return_value=True
            ), mock.patch(
                "normattiva2md.cli.validate_normattiva_url"
            ), mock.patch(
                "normattiva2md.cli.extract_params_from_normattiva_url",
                return_value=(params, object()),
            ), mock.patch(
                "normattiva2md.cli.download_akoma_ntoso", return_value=True
            ), mock.patch(
                "normattiva2md.cli.convert_akomantoso_to_markdown_improved",
                return_value=True,
            ), mock.patch(
                "tempfile.mkstemp", return_value=(fd, temp_file)
            ), mock.patch(
                "normattiva2md.cli.os.remove"
            ):
                cli.main()

    def test_invalid_article_format_exits(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "doc.xml")
            with open(input_path, "w", encoding="utf-8") as f:
                f.write("<root/>")
            with mock.patch(
                "sys.argv",
                ["normattiva2md", "--art", "bad-1", input_path, os.path.join(tmpdir, "out.md")],
            ):
                with self.assertRaises(SystemExit):
                    cli.main()

    def test_with_references_existing_file_exits(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            existing = os.path.join(tmpdir, "out.md")
            with open(existing, "w", encoding="utf-8") as f:
                f.write("x")

            with mock.patch(
                "sys.argv",
                [
                    "normattiva2md",
                    "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2020;1",
                    "--with-references",
                    existing,
                ],
            ), mock.patch(
                "normattiva2md.cli.is_normattiva_url", return_value=True
            ):
                with self.assertRaises(SystemExit):
                    cli.main()

    def test_with_references_success(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with mock.patch(
                "sys.argv",
                [
                    "normattiva2md",
                    "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2020;1",
                    "--with-references",
                    "-o",
                    tmpdir,
                ],
            ), mock.patch(
                "normattiva2md.cli.is_normattiva_url", return_value=True
            ), mock.patch(
                "normattiva2md.cli.convert_with_references", return_value=True
            ):
                cli.main()

    def test_validate_on_local_file_calls_validator(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "doc.xml")
            output_path = os.path.join(tmpdir, "out.md")
            with open(input_path, "w", encoding="utf-8") as f:
                f.write("<root/>")
            with open(output_path, "w", encoding="utf-8") as f:
                f.write("# Title")

            with mock.patch(
                "normattiva2md.cli.convert_akomantoso_to_markdown_improved",
                return_value=True,
            ), mock.patch(
                "normattiva2md.cli.perform_validation", return_value=True
            ) as mock_validate:
                with mock.patch(
                    "sys.argv", ["normattiva2md", "--validate", input_path, output_path]
                ):
                    cli.main()
            mock_validate.assert_called_once()

    def test_validate_with_stdout_skips(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "doc.xml")
            with open(input_path, "w", encoding="utf-8") as f:
                f.write("<root/>")

            with mock.patch(
                "normattiva2md.cli.convert_akomantoso_to_markdown_improved",
                return_value=True,
            ), mock.patch(
                "normattiva2md.cli.perform_validation"
            ) as mock_validate:
                with mock.patch(
                    "sys.argv", ["normattiva2md", "--validate", input_path]
                ):
                    cli.main()
            mock_validate.assert_not_called()

    def test_provvedimenti_no_results(self):
        with mock.patch(
            "sys.argv",
            [
                "normattiva2md",
                "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2020;1",
                "--provvedimenti",
            ],
        ), mock.patch(
            "normattiva2md.cli.is_normattiva_url", return_value=True
        ), mock.patch(
            "normattiva2md.cli.extract_law_params_from_url", return_value=("2020", "1")
        ), mock.patch(
            "normattiva2md.cli.fetch_all_provvedimenti", return_value=[]
        ):
            cli.main()

    def test_provvedimenti_fetch_error_exits(self):
        with mock.patch(
            "sys.argv",
            [
                "normattiva2md",
                "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2020;1",
                "--provvedimenti",
            ],
        ), mock.patch(
            "normattiva2md.cli.is_normattiva_url", return_value=True
        ), mock.patch(
            "normattiva2md.cli.extract_law_params_from_url", return_value=("2020", "1")
        ), mock.patch(
            "normattiva2md.cli.fetch_all_provvedimenti", return_value=None
        ):
            with self.assertRaises(SystemExit):
                cli.main()

    def test_provvedimenti_missing_params_exits(self):
        with mock.patch(
            "sys.argv",
            [
                "normattiva2md",
                "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2020;1",
                "--provvedimenti",
            ],
        ), mock.patch(
            "normattiva2md.cli.is_normattiva_url", return_value=True
        ), mock.patch(
            "normattiva2md.cli.extract_law_params_from_url", return_value=(None, None)
        ):
            with self.assertRaises(SystemExit):
                cli.main()

    def test_provvedimenti_write_failure_exits(self):
        with mock.patch(
            "sys.argv",
            [
                "normattiva2md",
                "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2020;1",
                "--provvedimenti",
            ],
        ), mock.patch(
            "normattiva2md.cli.is_normattiva_url", return_value=True
        ), mock.patch(
            "normattiva2md.cli.extract_law_params_from_url", return_value=("2020", "1")
        ), mock.patch(
            "normattiva2md.cli.fetch_all_provvedimenti", return_value=[{"x": "y"}]
        ), mock.patch(
            "normattiva2md.cli.write_provvedimenti_csv", return_value=False
        ):
            with self.assertRaises(SystemExit):
                cli.main()


if __name__ == "__main__":
    unittest.main()
