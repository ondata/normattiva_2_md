import os
import tempfile
import unittest
from unittest import mock

from normattiva2md import normattiva_api as api


class FakeResponse:
    def __init__(self, text="", content=b"", status_code=200, headers=None):
        self.text = text
        self.content = content
        self.status_code = status_code
        self.headers = headers or {}

    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception("http error")


class TestNormattivaApi(unittest.TestCase):
    def test_normalize_and_validate(self):
        url = "https:\\/\\/www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2020;1"
        normalized = api.normalize_normattiva_url(url)
        self.assertNotIn("\\", normalized)
        self.assertTrue(api.validate_normattiva_url(normalized))

        with self.assertRaises(ValueError):
            api.validate_normattiva_url("http://www.normattiva.it/")
        with self.assertRaises(ValueError):
            api.validate_normattiva_url("https://example.com/")

    def test_is_normattiva_url(self):
        self.assertTrue(
            api.is_normattiva_url(
                "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2020;1"
            )
        )
        self.assertFalse(api.is_normattiva_url("https://example.com/"))

    def test_is_normattiva_export_url(self):
        url = "https://www.normattiva.it/esporta/attoCompleto"
        self.assertTrue(api.is_normattiva_export_url(url))
        self.assertFalse(api.is_normattiva_export_url("https://www.normattiva.it/"))

    def test_extract_params_from_normattiva_url(self):
        html = """
        <input name="atto.dataPubblicazioneGazzetta" value="2020-01-02"/>
        <input name="atto.codiceRedazionale" value="ABC123"/>
        <input value="03/01/2020"/>
        """
        session = mock.Mock()
        session.get.return_value = FakeResponse(text=html)

        params, _ = api.extract_params_from_normattiva_url(
            "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2020;1",
            session=session,
            quiet=True,
        )
        self.assertEqual(params["dataGU"], "20200102")
        self.assertEqual(params["codiceRedaz"], "ABC123")
        self.assertEqual(params["dataVigenza"], "20200103")

    def test_extract_params_rejects_export_url(self):
        params, _ = api.extract_params_from_normattiva_url(
            "https://www.normattiva.it/esporta/attoCompleto",
            quiet=True,
        )
        self.assertIsNone(params)

    def test_download_akoma_ntoso_success_and_non_xml(self):
        params = {"dataGU": "20200101", "codiceRedaz": "X", "dataVigenza": "20200102"}
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "doc.xml")
            session = mock.Mock()
            session.get.return_value = FakeResponse(
                content=b"<?xml version='1.0'?><akomaNtoso></akomaNtoso>"
            )
            self.assertTrue(
                api.download_akoma_ntoso(
                    params, output_path, session=session, quiet=True
                )
            )
            self.assertTrue(os.path.exists(output_path))

            session.get.return_value = FakeResponse(content=b"<html></html>")
            self.assertFalse(
                api.download_akoma_ntoso(
                    params, output_path, session=session, quiet=True
                )
            )


if __name__ == "__main__":
    unittest.main()
