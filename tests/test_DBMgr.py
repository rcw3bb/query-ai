import unittest
import psycopg2

from unittest.mock import patch, MagicMock
from query_ai.commons import embedding_token_length
from query_ai.database.db_manager import DBMgr, is_existing_context

class TestDBMgr(unittest.TestCase):

    @patch('psycopg2.connect')
    def test_connects_to_database(self, mock_connect):
        db_mgr = DBMgr('test_db', 'user', 'password', 'localhost', 5432)
        connection = MagicMock()
        mock_connect.return_value = connection

        result = db_mgr.connect()

        self.assertEqual(result, connection)
        mock_connect.assert_called_once_with(database='test_db', user='user', password='password', host='localhost', port=5432)

    @patch('psycopg2.connect')
    def test_fails_to_connect_to_database(self, mock_connect):
        db_mgr = DBMgr('test_db', 'user', 'password', 'localhost', 5432)
        mock_connect.side_effect = psycopg2.Error("Connection error")

        result = db_mgr.connect()

        self.assertIsNone(result)

    @patch('psycopg2.connect')
    def test_executes_sql_statement(self, mock_connect):
        db_mgr = DBMgr('test_db', 'user', 'password', 'localhost', 5432)
        connection = MagicMock()
        cursor = MagicMock()
        connection.cursor.return_value = cursor
        mock_connect.return_value = connection

        stmt = "SELECT 1"
        output_logic = lambda conn, cur: cur.fetchone()
        cursor.fetchone.return_value = (1,)

        result = db_mgr.execute(stmt, output_logic)

        cursor.execute.assert_called_once_with(stmt, None)
        self.assertEqual(result, (1,))

    @unittest.skip("Skipping test_initializes_database")
    @patch('psycopg2.connect')
    def test_initializes_database(self, mock_connect):
        db_mgr = DBMgr('test_db', 'user', 'password', 'localhost', 5432)
        connection = MagicMock()
        cursor = MagicMock()
        connection.cursor.return_value = cursor
        mock_connect.return_value = connection

        db_mgr.initialize()

        cursor.execute.assert_any_call("CREATE EXTENSION IF NOT EXISTS vector", None)
        cursor.execute.assert_any_call("""
            CREATE TABLE IF NOT EXISTS qa_embeddings (id SERIAL PRIMARY KEY,
                chunk_id INTEGER NOT NULL,
                start_word INTEGER NOT NULL,
                end_word INTEGER NOT NULL,
                context TEXT,
                embedding vector(%s)
            )
            """, (embedding_token_length,))
        cursor.execute.assert_any_call("CREATE INDEX IF NOT EXISTS embedding_idx ON qa_embeddings USING ivfflat(embedding)", None)

    @patch('psycopg2.connect')
    def test_checks_existing_context(self, mock_connect):
        db_mgr = DBMgr('test_db', 'user', 'password', 'localhost', 5432)
        connection = MagicMock()
        cursor = MagicMock()
        connection.cursor.return_value = cursor
        mock_connect.return_value = connection

        context = "test context"
        cursor.fetchone.return_value = (True,)

        result = is_existing_context(db_mgr, context)

        cursor.execute.assert_called_once_with("SELECT EXISTS(SELECT 1 FROM qa_embeddings WHERE context = %s)", (context,))
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()