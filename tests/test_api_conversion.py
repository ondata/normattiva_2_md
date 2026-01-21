import tempfile
import unittest
from unittest import mock

from normattiva2md.api import convert_url, convert_xml
from normattiva2md.exceptions import ConversionError, InvalidURLError, XMLFileNotFoundError
from normattiva2md.constants import AKN_NAMESPACE


class TestApiConversion(unittest.TestCase):
    def _write_xml(self, content):
        tmp = tempfile.NamedTemporaryFile("w", suffix=".xml", delete=False)
        tmp.write(content)
        tmp.flush()
        return tmp.name

    def _minimal_xml(self):
        return (
            f"<akn:akomaNtoso xmlns:akn=\"{AKN_NAMESPACE['akn']}\" "
            "xmlns:eli=\"http://data.europa.eu/eli/ontology#\">"
            "<akn:meta>"
            "<akn:identification>"
            "<akn:FRBRWork>"
            "<akn:FRBRalias name=\"urn:nir\" value=\"urn:nir:stato:legge:2003-07-29;229\"/>"
            "</akn:FRBRWork>"
            "<akn:FRBRExpression><akn:FRBRdate date=\"2020-01-01\"/></akn:FRBRExpression>"
            "<eli:id_local>229</eli:id_local>"
            "<eli:date_document>2003-07-29</eli:date_document>"
            "</akn:identification>"
            "</akn:meta>"
            "<akn:body>"
            "<akn:article eId=\"art_1\"><akn:content><akn:p>Testo</akn:p></akn:content></akn:article>"
            "<akn:ref href=\"/akn/it/act/legge/stato/2004-01-01/10/!main#art_2\"/>"
            "<akn:ref href=\"https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2005-01-01;11\"/>"
            "</akn:body>"
            "</akn:akomaNtoso>"
        )

    def test_convert_xml_missing_file(self):
        with self.assertRaises(XMLFileNotFoundError):
            convert_xml("/tmp/does-not-exist.xml")

    def test_convert_xml_parse_error(self):
        path = self._write_xml("<akn:akomaNtoso")
        with self.assertRaises(ConversionError):
            convert_xml(path)

    def test_convert_url_invalid_domain(self):
        with self.assertRaises(InvalidURLError):
            convert_url("https://example.com/not-allowed")

    def test_convert_xml_with_urls_builds_cross_references(self):
        xml_path = self._write_xml(self._minimal_xml())

        with mock.patch("normattiva2md.api.generate_markdown_text", return_value="MD") as mock_generate:
            result = convert_xml(xml_path, with_urls=True, quiet=True)

        self.assertIsNotNone(result)
        cross_references = mock_generate.call_args.kwargs["cross_references"]
        self.assertIn(
            "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2004-01-01;10~art2",
            cross_references,
        )
        self.assertIn(
            "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2005-01-01;11",
            cross_references,
        )

    def test_convert_xml_merges_metadata(self):
        xml_path = self._write_xml(self._minimal_xml())

        with mock.patch(
            "normattiva2md.api.extract_metadata_from_xml",
            return_value={
                "dataGU": "20200101",
                "codiceRedaz": "XYZ",
                "dataVigenza": "20200102",
                "url": "xml-url",
            },
        ):
            with mock.patch(
                "normattiva2md.api.generate_markdown_text", return_value="MD"
            ) as mock_generate:
                convert_xml(
                    xml_path,
                    metadata={"dataGU": "20221212", "custom": "value"},
                    quiet=True,
                )

        merged_metadata = mock_generate.call_args.kwargs["metadata"]
        self.assertEqual(merged_metadata["dataGU"], "20221212")
        self.assertEqual(merged_metadata["custom"], "value")
        self.assertEqual(merged_metadata["codiceRedaz"], "XYZ")


if __name__ == "__main__":
    unittest.main()
