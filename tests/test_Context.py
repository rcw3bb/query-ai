import unittest
from unittest.mock import patch
from flask import Flask
from query_ai.api.context import Context

class TestContext(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        Context(self.app)
        self.client = self.app.test_client()

    @patch('query_ai.database.is_existing_context')
    @patch('query_ai.model.model_manager.ModelMgr.get_embeddings')
    @patch('query_ai.database.db_manager.DBMgr.execute')
    @patch('query_ai.util.text_util.TextUtil.split_by_paragraph')
    @patch('query_ai.util.text_util.TextUtil.clean_text')
    def test_saves_new_context_successfully(self, mock_clean, mock_split, mock_execute, mock_embed, mock_exists):
        mock_split.return_value = ["paragraph1"]
        mock_clean.return_value = "cleaned paragraph"
        mock_embed.return_value = [(1, 0, 10, "chunk", [0.1, 0.2])]
        mock_execute.return_value = False

        response = self.client.put('/api/v1/context', json={'context': 'test context'})

        self.assertEqual(201, response.status_code)

    @patch('query_ai.database.db_manager.is_existing_context')
    @patch('query_ai.model.model_manager.ModelMgr.get_embeddings')
    @patch('query_ai.database.db_manager.DBMgr.execute')
    @patch('query_ai.util.text_util.TextUtil.split_by_paragraph')
    @patch('query_ai.util.text_util.TextUtil.clean_text')
    def test_returns_200_for_existing_context(self, mock_clean, mock_split, mock_execute, mock_embed, mock_exists):
        mock_execute.return_value = True
        mock_split.return_value = ["paragraph1"]
        mock_clean.return_value = "cleaned paragraph"
        mock_embed.return_value = [(1, 0, 10, "chunk", [0.1, 0.2])]

        response = self.client.put('/api/v1/context', json={'context': 'test context'})

        self.assertEqual(200, response.status_code)

    @patch('query_ai.util.text_util.TextUtil.split_by_paragraph')
    def test_handles_empty_context(self, mock_split):
        mock_split.return_value = []

        response = self.client.put('/api/v1/context', json={'context': ''})

        self.assertEqual(400, response.status_code)

    def test_rejects_missing_context_field(self):
        response = self.client.put('/api/v1/context', json={})

        self.assertEqual(400, response.status_code)

    def test_rejects_non_json_payload(self):
        response = self.client.put('/api/v1/context', data='not json')

        self.assertEqual(415, response.status_code)

if __name__ == '__main__':
    unittest.main()