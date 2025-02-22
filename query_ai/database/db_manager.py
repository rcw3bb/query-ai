"""
A module to manage database connections and operations for a PostgreSQL database.

Author: Ron Webb
Since: 1.0.0
"""
import threading

import psycopg2
from pgvector.psycopg2 import register_vector
from psycopg2 import ProgrammingError

from query_ai.config import embedding_config
from query_ai.logger import get_logger

class DBMgr:
    """
    A class to manage database connections and operations for a PostgreSQL database.

    Author: Ron Webb
    Since: 1.0.0
    """

    __is_db_initialized__ = False
    __lock = threading.Lock()

    @staticmethod
    def __set_db_initialized(is_db_initialized: bool):
        with DBMgr.__lock:
            DBMgr.__is_db_initialized__ = is_db_initialized

    @staticmethod
    def __is_db_initialized():
        return DBMgr.__is_db_initialized__

    # pylint: disable=too-many-arguments, too-many-positional-arguments
    def __init__(self, dbname: str, user: str, password: str, host: str, port: int):
        """
        Constructs all the necessary attributes for the DBMgr object.

        Parameters:
            dbname (str): The name of the database.
            user (str): The username used to authenticate.
            password (str): The password used to authenticate.
            host (str): The host address of the database.
            port (int): The port number to connect to.
        """
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.log = get_logger(__name__)
    # pylint: disable=too-many-arguments, too-many-positional-arguments

    def connect(self):
        """
        Establishes a connection to the PostgresSQL database.

        Returns:
            connection (psycopg2.extensions.connection): The database connection object if
            successful, None otherwise.
        """
        try:
            connection = psycopg2.connect(
                database=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )

            connection.autocommit = True

            if DBMgr.__is_db_initialized() is False:
                DBMgr.__set_db_initialized(True)
                self.initialize()

            return connection
        except psycopg2.Error as e:
            self.log.error("Error connecting to PostgreSQL database: %s", e)
            DBMgr.__set_db_initialized(False)
            return None

    def execute(self, stmt: str, output_logic = lambda connection, cursor: None,
                stmt_vars : tuple = None):
        """
        Executes a given SQL statement.

        Parameters:
            stmt (str): The SQL statement to execute.
            output_logic (function): A function to process the result of the query.
            stmt_vars (tuple): The variables to pass to the SQL statement.

        Returns:
            The result of the output_logic function.
        """
        try:
            connection = self.connect()
            try:
                cursor = connection.cursor()

                try:
                    cursor.execute(stmt, stmt_vars)
                except ProgrammingError as prog_error:
                    if "can't adapt type 'numpy.ndarray'" in str(prog_error):
                        self.log.debug("Registering vector extension.")
                        self.__register_vector()
                        cursor.execute(stmt, stmt_vars)
                    else:
                        raise prog_error

                return output_logic(connection, cursor)
            finally:
                connection.close()
        except Exception as exception:
            raise DBException("Database error occurred.") from exception

    def initialize(self):
        """
        Initializes the database by creating necessary extensions and tables.
        """

        self.__register_vector()

        self.execute("""
            CREATE TABLE IF NOT EXISTS qa_embeddings (id SERIAL PRIMARY KEY,
                chunk_id INTEGER NOT NULL,
                start_word INTEGER NOT NULL,
                end_word INTEGER NOT NULL,
                context TEXT,
                embedding vector(%s)
            )
            """, stmt_vars=(embedding_config.token_length,))

        self.execute("CREATE INDEX IF NOT EXISTS embedding_idx ON qa_embeddings "
                     "USING ivfflat(embedding)")

    def __register_vector(self):
        self.execute("CREATE EXTENSION IF NOT EXISTS vector",
                     output_logic=lambda ___connection, ___cursor: register_vector(___connection))

class DBException(Exception):
    """
    An exception class to handle database errors.
    """

def is_existing_context(db_manager : DBMgr, context: str):
    """
    Checks if a given context already exists in the qa_embeddings table.

    Parameters:
        db_manager (DBMgr): The database manager instance.
        context (str): The context to check for existence.

    Returns:
        bool: True if the context exists, False otherwise.
    """
    return db_manager.execute("SELECT EXISTS(SELECT 1 FROM qa_embeddings WHERE context = %s)",
                              lambda ___connection, ___cursor: ___cursor.fetchone()[0], (context,))
