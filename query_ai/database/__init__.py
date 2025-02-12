from .db_manager import DBMgr, is_existing_context

# Initialize the DBManager instance
db_manager = DBMgr(
    dbname="query-ai",
    user="postgres",
    password="mypassword",
    host="localhost",
    port="5432"
)

db_manager.initialize()

# Export the db_manager and connection
__all__ = ['db_manager', 'is_existing_context']