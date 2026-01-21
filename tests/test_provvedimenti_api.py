import os
import tempfile
import unittest
from unittest import mock

from normattiva2md import provvedimenti_api as api


class TestProvvedimentiApi(unittest.TestCase):
    def test_extract_law_params_from_url(self):
        url = "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2024-03-01;207"
        year, number = api.extract_law_params_from_url(url)
        self.assertEqual(year, "2024")
        self.assertEqual(number, "207")

        url_simple = "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2020;5"
        year, number = api.extract_law_params_from_url(url_simple)
        self.assertEqual(year, "2020")
        self.assertEqual(number, "5")

        year, number = api.extract_law_params_from_url("https://example.com")
        self.assertIsNone(year)
        self.assertIsNone(number)

    def test_build_search_url(self):
        url = api.build_search_url("10", "2020")
        self.assertIn("numero=10&anno=2020", url)
        self.assertTrue(url.startswith(api.BASE_URL))

        url_page = api.build_search_url("10", "2020", page=2)
        self.assertIn("page=2&numero=10&anno=2020", url_page)

    def test_parse_provvedimenti_html(self):
        html = """
        <table>
          <tr><th>Header</th></tr>
          <tr>
            <td><a href="/detail/123">Dettagli</a></td>
            <td>Governo &amp; co</td>
            <td>Fonte</td>
            <td>Oggetto &#xE0;</td>
            <td>Tipo</td>
            <td>Stato</td>
            <td><a href="/prov/456">Link</a></td>
          </tr>
        </table>
        """
        results = api.parse_provvedimenti_html(html)
        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(
            result["dettagli"], "https://www.programmagoverno.gov.it/detail/123"
        )
        self.assertEqual(result["governo"], "Governo & co")
        self.assertEqual(result["oggetto"], "Oggetto à")
        self.assertEqual(
            result["link_al_provvedimento"],
            "https://www.programmagoverno.gov.it/prov/456",
        )

    def test_parse_provvedimenti_html_no_results(self):
        results = api.parse_provvedimenti_html("Nessun risultato.")
        self.assertEqual(results, [])

    def test_has_next_page(self):
        html = '<a class="pagination-next" href="?page=2">Avanti</a>'
        self.assertTrue(api.has_next_page(html))

        html_disabled = '<a class="pagination-next disabled" href="?page=2">Avanti</a>'
        self.assertFalse(api.has_next_page(html_disabled))

    def test_fetch_all_provvedimenti(self):
        page_one = "<tr><td>1</td><td>G</td><td>F</td><td>O</td><td>P</td><td>A</td><td></td></tr>"
        page_two = "Nessun risultato."

        with mock.patch.object(api, "fetch_provvedimenti_page") as mock_fetch, mock.patch.object(
            api, "has_next_page", side_effect=[True, False]
        ):
            mock_fetch.side_effect = [page_one, page_two]
            results = api.fetch_all_provvedimenti("10", "2020", quiet=True)

        self.assertEqual(len(results), 1)

    def test_determine_csv_path(self):
        path = api.determine_csv_path(None, "2020", "10")
        self.assertEqual(path, "2020_10_provvedimenti.csv")

        path = api.determine_csv_path("out/report.md", "2020", "10")
        self.assertEqual(path, os.path.join("out", "2020_10_provvedimenti.csv"))

    def test_export_provvedimenti_csv(self):
        data = [
            {
                "dettagli": "d",
                "governo": "g",
                "fonte_provvedimento": "f",
                "oggetto": "o",
                "provvedimento_previsto": "p",
                "adozione": "a",
                "link_al_provvedimento": "l",
            }
        ]
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = os.path.join(tmpdir, "out.csv")
            success = api.export_provvedimenti_csv(data, csv_path)
            self.assertTrue(success)
            self.assertTrue(os.path.exists(csv_path))

    def test_write_provvedimenti_csv_overwrite(self):
        data = [
            {
                "dettagli": "d",
                "governo": "g",
                "fonte_provvedimento": "f",
                "oggetto": "o",
                "provvedimento_previsto": "p",
                "adozione": "a",
                "link_al_provvedimento": "l",
            }
        ]
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = os.path.join(tmpdir, "2020_10_provvedimenti.csv")
            with open(csv_path, "w", encoding="utf-8") as f:
                f.write("existing")

            with mock.patch.object(api, "prompt_overwrite", return_value=True):
                success = api.write_provvedimenti_csv(
                    data, "2020", "10", os.path.join(tmpdir, "out.md"), quiet=True
                )
        self.assertTrue(success)

    def test_write_provvedimenti_csv_abort(self):
        data = [
            {
                "dettagli": "d",
                "governo": "g",
                "fonte_provvedimento": "f",
                "oggetto": "o",
                "provvedimento_previsto": "p",
                "adozione": "a",
                "link_al_provvedimento": "l",
            }
        ]
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = os.path.join(tmpdir, "2020_10_provvedimenti.csv")
            with open(csv_path, "w", encoding="utf-8") as f:
                f.write("existing")

            with mock.patch.object(api, "prompt_overwrite", return_value=False):
                success = api.write_provvedimenti_csv(
                    data, "2020", "10", os.path.join(tmpdir, "out.md"), quiet=True
                )
        self.assertFalse(success)


if __name__ == "__main__":
    unittest.main()
