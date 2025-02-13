import unittest
import os

from unittest.mock import patch, MagicMock
from query_ai.config.db_config import DBConfig

class TestDBConfig(unittest.TestCase):

    @patch('query_ai.util.properties.Properties')
    @patch('os.getenv')
    def test_initializes_with_default_values(self, mock_getenv, mock_properties):
        mock_properties_instance = MagicMock()
        mock_properties.return_value = mock_properties_instance
        mock_properties_instance.get.side_effect = lambda section, key, default: default
        mock_properties_instance.getint.side_effect = lambda section, key, default: int(default)
        mock_getenv.side_effect = lambda key, default: default

        module_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(module_dir, "doesnt_exists.properties")

        config = DBConfig(full_path)

        self.assertEqual(config.get_database(), "query-ai")
        self.assertEqual(config.get_host(), "localhost")
        self.assertEqual(config.get_port(), 5432)
        self.assertEqual(config.get_user(), "postgres")
        self.assertEqual(config.get_password(), "mypassword")

    @patch('query_ai.util.properties.Properties')
    @patch('os.getenv')
    def test_initializes_with_custom_values(self, mock_getenv, mock_properties):
        mock_properties_instance = MagicMock()
        mock_properties.return_value = mock_properties_instance
        mock_properties_instance.get.side_effect = lambda section, key, default: "custom_db"
        mock_properties_instance.getint.side_effect = lambda section, key, default: 1234
        mock_getenv.side_effect = lambda key, default: "custom_user" if key == "DB_USER" \
            else "custom_password" if key == "DB_PASSWORD" else default

        module_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(module_dir, "db_config_test.properties")

        config = DBConfig(filename)

        self.assertEqual("custom_db", config.get_database())
        self.assertEqual("localhost", config.get_host())
        self.assertEqual(1234, config.get_port())
        self.assertEqual("custom_user", config.get_user())
        self.assertEqual("custom_password", config.get_password())

    @patch('query_ai.util.properties.Properties')
    @patch('os.getenv')
    def test_initializes_with_missing_env_variables(self, mock_getenv, mock_properties):
        mock_properties_instance = MagicMock()
        mock_properties.return_value = mock_properties_instance
        mock_properties_instance.get.side_effect = lambda section, key, default: default
        mock_properties_instance.getint.side_effect = lambda section, key, default: int(default)
        mock_getenv.side_effect = lambda key, default: default

        module_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(module_dir, "db_config_test.properties")
        config = DBConfig(filename)

        self.assertEqual("postgres", config.get_user())
        self.assertEqual("mypassword", config.get_password())

if __name__ == '__main__':
    unittest.main()