import unittest
from unittest.mock import patch, Mock, ANY
from flask import Flask
from query_ai.api.query import Query

class TestQuery(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.query = Query(self.app)

    @patch('query_ai.model.model_manager.ModelMgr.generate_answer')
    def test_handles_question_with_context(self, mock_generate):
        mock_generate.return_value = [{'generated_text': 'test answer'}]

        with self.app.test_request_context(json={'question': 'test?', 'context': 'test context'}):
            response = self.query.query()

            self.assertEqual(200, response[1])
            self.assertEqual({'answer': 'test answer'}, response[0].get_json())
            mock_generate.assert_called_with('test?', provided_context='test context')

    @patch('query_ai.model.model_manager.ModelMgr.generate_answer')
    @patch('query_ai.database.db_manager.DBMgr')
    def test_handles_question_without_context(self, mock_db, mock_generate):
        mock_generate.return_value = [{'generated_text': 'test answer'}]

        with self.app.test_request_context(json={'question': 'test?'}):
            response = self.query.query()

            self.assertEqual(200, response[1])
            self.assertEqual({'answer': 'test answer'}, response[0].get_json())
            mock_generate.assert_called_with('test?', ANY)

    @patch('query_ai.model.model_manager.ModelMgr.generate_answer')
    def test_returns_error_when_model_fails(self, mock_generate):
        mock_generate.return_value = None

        with self.app.test_request_context(json={'question': 'test?'}):
            response = self.query.query()

            self.assertEqual(500, response[1])
            self.assertEqual({'error': 'Error generating response.'}, response[0].get_json())

    def test_rejects_non_json_payload(self):
        with self.app.test_request_context(data='invalid'):
            response = self.query.query()

            self.assertEqual(415, response[1])

    def test_rejects_missing_question_field(self):
        with self.app.test_request_context(json={}):
            response = self.query.query()

            self.assertEqual(400, response[1])

if __name__ == '__main__':
    unittest.main()