import unittest
import xml.etree.ElementTree as ET

from normattiva2md.xml_parser import (
    build_permanent_url,
    construct_article_eid,
    extract_metadata_from_xml,
    filter_xml_to_article,
)
from normattiva2md.constants import AKN_NAMESPACE, ELI_NAMESPACE


class TestXmlParser(unittest.TestCase):
    def test_build_permanent_url(self):
        url = build_permanent_url("20200101", "123", "20200102")
        self.assertIn("urn:nir:stato:legge:2020-01-01;123!vig=2020-01-02", url)
        self.assertIn("legge:bad--", build_permanent_url("bad", "123", "20200102"))

    def test_construct_article_eid(self):
        self.assertEqual(construct_article_eid("4"), "art_4")
        self.assertEqual(construct_article_eid("16bis"), "art_16-bis")
        self.assertIsNone(construct_article_eid("bad-1"))
        self.assertIsNone(construct_article_eid(""))

    def test_extract_metadata_from_xml(self):
        xml = (
            f'<akn:akomaNtoso xmlns:akn="{AKN_NAMESPACE["akn"]}" '
            f'xmlns:eli="{ELI_NAMESPACE["eli"]}">'
            "<akn:meta>"
            "<akn:identification>"
            "<akn:FRBRWork>"
            '<akn:FRBRalias name="urn:nir" value="urn:nir:stato:legge:2020-01-01;123"/>'
            "</akn:FRBRWork>"
            '<akn:FRBRExpression><akn:FRBRdate date="2020-01-02"/></akn:FRBRExpression>'
            "<eli:id_local>123</eli:id_local>"
            "<eli:date_document>2020-01-01</eli:date_document>"
            "</akn:identification>"
            "</akn:meta>"
            "<akn:body/>"
            "</akn:akomaNtoso>"
        )
        root = ET.fromstring(xml)
        metadata = extract_metadata_from_xml(root)
        self.assertEqual(metadata["codiceRedaz"], "123")
        self.assertEqual(metadata["dataGU"], "20200101")
        self.assertEqual(metadata["dataVigenza"], "20200102")
        self.assertIn("url", metadata)
        self.assertIn("url_xml", metadata)
        self.assertIn("url_permanente", metadata)

    def test_filter_xml_to_article(self):
        xml = (
            f'<akn:akomaNtoso xmlns:akn="{AKN_NAMESPACE["akn"]}">'
            "<akn:meta/>"
            "<akn:body>"
            '<akn:article eId="art_1"><akn:content/></akn:article>'
            "</akn:body>"
            "</akn:akomaNtoso>"
        )
        root = ET.fromstring(xml)
        filtered = filter_xml_to_article(root, "art_1", AKN_NAMESPACE)
        self.assertIsNotNone(filtered)
        self.assertIsNotNone(filtered.find(".//akn:meta", AKN_NAMESPACE))
        self.assertIsNotNone(filtered.find('.//akn:article[@eId="art_1"]', AKN_NAMESPACE))


if __name__ == "__main__":
    unittest.main()
