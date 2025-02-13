import unittest
import os
from unittest.mock import patch, MagicMock
from query_ai.util.properties import Properties

class TestProperties(unittest.TestCase):

    def test_reads_properties_file(self):

        module_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(module_dir, "properties_test.properties")

        properties = Properties(full_path)

        result = properties.get('section', 'prop', 'default')

        self.assertEqual('test', result)

    @patch('query_ai.util.properties.os.path.join')
    @patch('query_ai.util.properties.configparser.ConfigParser.read')
    def test_get_existing_property(self, mock_read, mock_join):
        mock_join.return_value = '/fake/path/to/conf/test.properties'
        properties = Properties('test.properties')
        config = MagicMock()
        config.has_option.return_value = True
        config.get.return_value = 'value'
        properties.properties = config

        result = properties.get('section', 'prop', 'default')

        self.assertEqual(result, 'value')

    @patch('query_ai.util.properties.os.path.join')
    @patch('query_ai.util.properties.configparser.ConfigParser.read')
    def test_get_non_existing_property(self, mock_read, mock_join):
        mock_join.return_value = '/fake/path/to/conf/test.properties'
        properties = Properties('test.properties')
        config = MagicMock()
        config.has_option.return_value = False
        properties.properties = config

        result = properties.get('section', 'prop', 'default')

        self.assertEqual(result, 'default')

    @patch('query_ai.util.properties.os.path.join')
    @patch('query_ai.util.properties.configparser.ConfigParser.read')
    def test_getint_existing_property(self, mock_read, mock_join):
        mock_join.return_value = '/fake/path/to/conf/test.properties'
        properties = Properties('test.properties')
        config = MagicMock()
        config.has_option.return_value = True
        config.getint.return_value = 42
        properties.properties = config

        result = properties.getint('section', 'prop', 0)

        self.assertEqual(result, 42)

    @patch('query_ai.util.properties.os.path.join')
    @patch('query_ai.util.properties.configparser.ConfigParser.read')
    def test_getint_non_existing_property(self, mock_read, mock_join):
        mock_join.return_value = '/fake/path/to/conf/test.properties'
        properties = Properties('test.properties')
        config = MagicMock()
        config.has_option.return_value = False
        properties.properties = config

        result = properties.getint('section', 'prop', 0)

        self.assertEqual(result, 0)

if __name__ == '__main__':
    unittest.main()