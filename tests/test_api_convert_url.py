import os
import tempfile
import unittest
from unittest import mock

from normattiva2md.api import convert_url


class TestApiConvertUrl(unittest.TestCase):
    def _write_minimal_xml(self, path):
        content = (
            '<akn:akomaNtoso xmlns:akn="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">'
            "<akn:meta/>"
            "<akn:body/>"
            "</akn:akomaNtoso>"
        )
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

    def test_convert_url_success(self):
        params = {
            "dataGU": "20200101",
            "codiceRedaz": "X",
            "dataVigenza": "20200102",
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            xml_path = os.path.join(tmpdir, "doc.xml")

            def fake_download(_params, output_path, _session, quiet=False):
                self._write_minimal_xml(output_path)
                return True

            with mock.patch(
                "normattiva2md.api.extract_params_from_normattiva_url",
                return_value=(params, object()),
            ), mock.patch(
                "normattiva2md.api.download_akoma_ntoso",
                side_effect=fake_download,
            ):
                result = convert_url(
                    "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2020;1",
                    quiet=True,
                )
        self.assertIsNotNone(result)
        self.assertEqual(result.metadata["codiceRedaz"], "X")
        self.assertTrue(result.url.startswith("https://www.normattiva.it/uri-res/N2Ls"))


if __name__ == "__main__":
    unittest.main()
