import unittest
import psycopg2

from unittest.mock import patch, MagicMock

from psycopg2 import ProgrammingError

from query_ai.config import embedding_config
from query_ai.database.db_manager import DBMgr, is_existing_context, DBException


class TestDBMgr(unittest.TestCase):

    @patch('query_ai.database.db_manager.register_vector', new_callable=MagicMock)
    @patch('psycopg2.connect')
    def test_01_connects_to_database(self, mock_connect, mock_register_vector):
        db_mgr = DBMgr('test_db', 'user', 'password', 'localhost', 5432)
        connection = MagicMock()
        mock_connect.return_value = connection

        result = db_mgr.connect()

        self.assertEqual(result, connection)

        mock_register_vector.assert_called_once()

    @patch('psycopg2.connect')
    def test_fails_to_connect_to_database(self, mock_connect):
        db_mgr = DBMgr('test_db', 'user', 'password', 'localhost', 5432)
        mock_connect.side_effect = psycopg2.Error("Connection error")
        result = db_mgr.connect()

        self.assertIsNone(result)

    @patch('query_ai.database.db_manager.register_vector', new_callable=MagicMock)
    @patch('psycopg2.connect')
    def test_executes_sql_statement(self, mock_connect, mock_register_vector):
        db_mgr = DBMgr('test_db', 'user', 'password', 'localhost', 5432)
        connection = MagicMock()
        cursor = MagicMock()
        connection.cursor.return_value = cursor
        mock_connect.return_value = connection

        stmt = "SELECT 1"
        output_logic = lambda conn, cur: cur.fetchone()
        cursor.fetchone.return_value = (1,)

        result = db_mgr.execute(stmt, output_logic)

        self.assertEqual(cursor.execute.call_args[0][0], stmt)
        self.assertEqual(result, (1,))

    @patch('query_ai.database.db_manager.register_vector', new_callable=MagicMock)
    @patch('psycopg2.connect')
    def test_initializes_database(self, mock_connect, mock_register_vector):
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
            """, (embedding_config.token_length,))
        cursor.execute.assert_any_call("CREATE INDEX IF NOT EXISTS embedding_idx ON qa_embeddings USING ivfflat(embedding)", None)

    @patch('query_ai.database.db_manager.register_vector', new_callable=MagicMock)
    @patch('psycopg2.connect')
    def test_checks_existing_context(self, mock_connect, mock_register_vector):
        db_mgr = DBMgr('test_db', 'user', 'password', 'localhost', 5432)
        connection = MagicMock()
        cursor = MagicMock()
        connection.cursor.return_value = cursor
        mock_connect.return_value = connection

        context = "test context"
        cursor.fetchone.return_value = (True,)

        result = is_existing_context(db_mgr, context)

        self.assertEqual(cursor.execute.call_args[0][0], "SELECT EXISTS(SELECT 1 FROM qa_embeddings WHERE context = %s)")
        self.assertTrue(result)

    @patch('query_ai.database.db_manager.DBMgr.connect')
    @patch('query_ai.database.db_manager.register_vector', new_callable=MagicMock)
    def test_execute_handles_programming_error_with_numpy(self, mock_register_vector, mock_connect):
        db_mgr = DBMgr('test_db', 'user', 'password', 'localhost', 5432)

        call_count = 0
        def side_effect(*args, **kwargs):
            nonlocal call_count
            if call_count == 0:
                call_count += 1
                raise ProgrammingError("can't adapt type 'numpy.ndarray'")
            else:
                return MagicMock()

        mock_connection = MagicMock()
        mock_cursor = mock_connection.cursor.return_value
        mock_connect.return_value = mock_connection
        mock_cursor.execute.side_effect = side_effect

        db_mgr.execute("SELECT * FROM qa_embeddings", stmt_vars=(1,))

        mock_register_vector.assert_called_once()
        mock_cursor.execute.assert_called_with("SELECT * FROM qa_embeddings", (1,))

    @patch('query_ai.database.db_manager.DBMgr.connect')
    @patch('query_ai.database.db_manager.register_vector', new_callable=MagicMock)
    def test_execute_handles_programming_error(self, mock_register_vector, mock_connect):
        db_mgr = DBMgr('test_db', 'user', 'password', 'localhost', 5432)

        call_count = 0
        def side_effect(*args, **kwargs):
            nonlocal call_count
            if call_count == 0:
                call_count += 1
                raise ProgrammingError("Other error")
            else:
                return MagicMock()

        mock_connection = MagicMock()
        mock_cursor = mock_connection.cursor.return_value
        mock_connect.return_value = mock_connection
        mock_cursor.execute.side_effect = side_effect

        with self.assertRaises(DBException):
            db_mgr.execute("SELECT * FROM qa_embeddings", stmt_vars=(1,))

        mock_register_vector.assert_not_called()

if __name__ == '__main__':
    unittest.main()