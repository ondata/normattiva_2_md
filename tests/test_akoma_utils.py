import sys
import tempfile
import unittest

sys.path.insert(0, "src")

from normattiva2md.akoma_utils import (
    akoma_uri_to_normattiva_url,
    extract_akoma_uris_from_xml,
    extract_cited_laws,
    parse_article_reference,
)
from normattiva2md.constants import AKN_NAMESPACE


class TestAkomaUtils(unittest.TestCase):
    def test_parse_article_reference(self):
        url = "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2020-01-01;1~art16bis"
        self.assertEqual(parse_article_reference(url), "art_16bis")
        self.assertIsNone(parse_article_reference(123))
        self.assertIsNone(parse_article_reference("https://www.normattiva.it/"))

    def test_akoma_uri_to_normattiva_url_with_article(self):
        uri = "/akn/it/act/legge/stato/2003-07-29/229/!main#art_1"
        url = akoma_uri_to_normattiva_url(uri)
        self.assertTrue(url.endswith("~art1"))
        self.assertTrue(url.startswith("https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2003-07-29;229"))

    def test_akoma_uri_to_normattiva_url_ignores_article_for_costituzione(self):
        uri = "/akn/it/act/costituzione/stato/1948-01-01/1/!main#art_1"
        url = akoma_uri_to_normattiva_url(uri)
        self.assertTrue(url.startswith("https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:costituzione:1948-01-01"))
        self.assertNotIn("~art", url)

    def test_akoma_uri_to_normattiva_url_unknown_type(self):
        uri = "/akn/it/act/unknown/stato/2003-07-29/229/!main"
        self.assertIsNone(akoma_uri_to_normattiva_url(uri))

    def test_extract_akoma_uris_from_xml(self):
        xml = (
            f"<akn:akomaNtoso xmlns:akn=\"{AKN_NAMESPACE['akn']}\">"
            "<akn:doc>"
            "<akn:ref href=\"/akn/it/act/legge/stato/2003-07-29/229/!main#art_1\"/>"
            "<akn:ref href=\"/akn/it/act/legge/stato/2004-01-01/10/!main\"/>"
            "<akn:ref href=\"https://example.com\"/>"
            "</akn:doc>"
            "</akn:akomaNtoso>"
        )
        with tempfile.NamedTemporaryFile("w", suffix=".xml", delete=False) as tmp:
            tmp.write(xml)
            tmp_path = tmp.name

        uris = extract_akoma_uris_from_xml(tmp_path)
        self.assertEqual(len(uris), 2)
        self.assertTrue(any(uri.startswith("/akn/") for uri in uris))

    def test_extract_cited_laws(self):
        xml = (
            f"<akn:akomaNtoso xmlns:akn=\"{AKN_NAMESPACE['akn']}\">"
            "<akn:doc>"
            "<akn:ref href=\"/akn/it/act/legge/stato/2003-07-29/229/!main#art_1\"/>"
            "<akn:ref href=\"/akn/it/act/legge/stato/2003-07-29/229/!main#art_2\"/>"
            "</akn:doc>"
            "</akn:akomaNtoso>"
        )
        with tempfile.NamedTemporaryFile("w", suffix=".xml", delete=False) as tmp:
            tmp.write(xml)
            tmp_path = tmp.name

        cited = extract_cited_laws(tmp_path)
        self.assertEqual(len(cited), 1)
        only = next(iter(cited))
        self.assertTrue(only.startswith("https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2003-07-29;229"))


if __name__ == "__main__":
    unittest.main()
