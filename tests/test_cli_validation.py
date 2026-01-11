import unittest
from unittest.mock import patch, MagicMock, mock_open
import argparse
import os

from normattiva2md.cli import main

class TestCLIValidation(unittest.TestCase):

    @patch('normattiva2md.cli.argparse.ArgumentParser.parse_args')
    @patch('normattiva2md.cli.convert_akomantoso_to_markdown_improved')
    @patch('normattiva2md.cli.MarkdownValidator')
    @patch('normattiva2md.cli.StructureComparer')
    @patch('normattiva2md.cli.download_akoma_ntoso')
    @patch('normattiva2md.cli.ET.parse')
    @patch('os.path.exists')
    @patch('normattiva2md.cli.open', new_callable=mock_open, read_data="# MD Content")
    def test_validate_flag_triggers_validation(self, mock_cli_open, mock_exists, mock_et_parse, mock_download, mock_comparer, mock_validator, mock_convert, mock_parse):
        # Setup mocks
        mock_args = argparse.Namespace(
            input="sample.xml",
            output="output.md",
            input_named=None,
            output_named=None,
            validate=True,
            search_query=None,
            keep_xml=False,
            quiet=True,
            completo=False,
            with_references=False,
            with_urls=False,
            provvedimenti=False,
            debug_search=False,
            auto_select=True,
            exa_api_key=None,
            version=False,
            article_filter=None
        )
        mock_parse.return_value = mock_args
        mock_exists.return_value = True
        
        # Mock convert return
        mock_convert.return_value = True
        
        # Mock validator
        v_instance = mock_validator.return_value
        v_instance.validate.return_value = {"status": "PASS", "checks": [], "errors": []}
        
        # Mock comparer
        c_instance = mock_comparer.return_value
        c_instance.compare.return_value = {"status": "PASS", "message": "OK"}
        
        # Run main
        with patch('sys.argv', ['normattiva2md', 'sample.xml', 'output.md', '--validate']):
             try:
                 main()
             except SystemExit:
                 pass
        
        # Verify validator was called
        v_instance.validate.assert_called_once()

if __name__ == "__main__":
    unittest.main()
