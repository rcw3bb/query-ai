import unittest

from unittest.mock import patch
from query_ai.config.db_config import DBConfig

class TestDBConfig(unittest.TestCase):

    @patch('os.getenv')
    def test_initializes_with_default_values(self, mock_getenv):
        mock_getenv.side_effect = lambda key, default: default

        config = DBConfig()

        self.assertEqual(config.get_database(), "query-ai")
        self.assertEqual(config.get_host(), "localhost")
        self.assertEqual(config.get_port(), "5432")
        self.assertEqual(config.get_user(), "postgres")
        self.assertEqual(config.get_password(), "mypassword")

    @patch('os.getenv')
    def test_initializes_with_custom_values(self, mock_getenv):
        mock_getenv.side_effect = lambda key, default: "custom_user" if key == "QA_DB_USERNAME" \
            else "custom_password" if key == "QA_DB_PASSWORD" \
            else "1234" if key == "QA_DB_PORT" \
            else "custom_db" if key == "QA_DB_NAME" else default

        config = DBConfig()

        self.assertEqual("custom_db", config.get_database())
        self.assertEqual("localhost", config.get_host())
        self.assertEqual("1234", config.get_port())
        self.assertEqual("custom_user", config.get_user())
        self.assertEqual("custom_password", config.get_password())

if __name__ == '__main__':
    unittest.main()