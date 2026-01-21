import unittest
from unittest import mock

from normattiva2md import cli


class TestCliSearch(unittest.TestCase):
    def test_search_no_results_exits(self):
        with mock.patch(
            "sys.argv", ["normattiva2md", "--search", "query"]
        ), mock.patch(
            "normattiva2md.cli.lookup_normattiva_url", return_value=None
        ):
            with self.assertRaises(SystemExit):
                cli.main()

    def test_search_debug_manual_decline(self):
        lookup_result = {"url": "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2020;1", "title": "Titolo"}
        with mock.patch(
            "sys.argv", ["normattiva2md", "--search", "query", "--debug-search"]
        ), mock.patch(
            "normattiva2md.cli.lookup_normattiva_url", return_value=lookup_result
        ), mock.patch(
            "builtins.input", return_value="n"
        ), mock.patch(
            "normattiva2md.cli.is_normattiva_url", return_value=True
        ), mock.patch(
            "normattiva2md.cli.extract_params_from_normattiva_url", return_value=(None, None)
        ):
            with self.assertRaises(SystemExit):
                cli.main()

    def test_search_debug_manual_accept_overwrite_no(self):
        lookup_result = {
            "url": "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2020;1",
            "title": "Titolo",
        }
        with mock.patch(
            "sys.argv", ["normattiva2md", "--search", "query", "--debug-search"]
        ), mock.patch(
            "normattiva2md.cli.lookup_normattiva_url", return_value=lookup_result
        ), mock.patch(
            "builtins.input", side_effect=["s", "", "n"]
        ), mock.patch(
            "normattiva2md.cli.generate_snake_case_filename", return_value="titolo.md"
        ), mock.patch(
            "os.path.exists", return_value=True
        ):
            with self.assertRaises(SystemExit):
                cli.main()


if __name__ == "__main__":
    unittest.main()
