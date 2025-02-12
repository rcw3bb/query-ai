import psycopg2
from pgvector.psycopg2 import register_vector
from query_ai.commons import embedding_token_length

class DBMgr:
    """
    A class to manage database connections and operations for a PostgreSQL database.

    Attributes:
        dbname (str): The name of the database.
        user (str): The username used to authenticate.
        password (str): The password used to authenticate.
        host (str): The host address of the database.
        port (int): The port number to connect to.

    Author: Ron Webb
    Since: 1.0.0
    """

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

    def connect(self):
        """
        Establishes a connection to the PostgreSQL database.

        Returns:
            connection (psycopg2.extensions.connection): The database connection object if successful, None otherwise.
        """
        try:
            connection = psycopg2.connect(
                database=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )

            # Enable autocommit
            connection.autocommit = True
            return connection
        except psycopg2.Error as e:
            print("Error connecting to PostgreSQL database:", e)
            return None

    def execute(self, stmt: str, output_logic = lambda connection, cursor: None, stmt_vars : tuple = None):
        """
        Executes a given SQL statement.

        Parameters:
            stmt (str): The SQL statement to execute.
            output_logic (function): A function to process the result of the query.
            stmt_vars (tuple): The variables to pass to the SQL statement.

        Returns:
            The result of the output_logic function.
        """
        connection = self.connect()
        try:
            cursor = connection.cursor()
            cursor.execute(stmt, stmt_vars)
            return output_logic(connection, cursor)
        finally:
            connection.close()

    def initialize(self):
        """
        Initializes the database by creating necessary extensions and tables.
        """

        # Create the vector extension
        self.execute("CREATE EXTENSION IF NOT EXISTS vector",
                     output_logic=lambda ___connection, ___cursor: register_vector(___connection))

        # Create a table to store embeddings and context
        self.execute("""
            CREATE TABLE IF NOT EXISTS qa_embeddings (id SERIAL PRIMARY KEY,
                chunk_id INTEGER NOT NULL,
                start_word INTEGER NOT NULL,
                end_word INTEGER NOT NULL,
                context TEXT, 
                embedding vector(%s)
            )
            """, stmt_vars=(embedding_token_length,))

        # Create index for embedding column
        self.execute("CREATE INDEX IF NOT EXISTS embedding_idx ON qa_embeddings USING ivfflat(embedding)")

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