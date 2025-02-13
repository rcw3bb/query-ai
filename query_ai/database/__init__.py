import os
from .db_manager import DBMgr, is_existing_context
from ..config.db_config import DBConfig

module_dir = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(module_dir, "..", "..", "conf", "application.properties")

db_config = DBConfig(filename)

db_manager = DBMgr(
    dbname=db_config.get_database(),
    user=db_config.get_user(),
    password=db_config.get_password(),
    host=db_config.get_host(),
    port=db_config.get_port()
)

db_manager.initialize()

__all__ = ['db_manager', 'is_existing_context']