"""
This module is the database package. It contains the database manager and the
database configuration.

Author: Ron Webb
Since: 1.0.0
"""

from .db_manager import DBMgr, is_existing_context, DBException
from ..config.db_config import DBConfig
from ..logger import get_logger

logger = get_logger(__name__)

db_config = DBConfig()

db_manager = DBMgr(
    dbname=db_config.get_database(),
    user=db_config.get_user(),
    password=db_config.get_password(),
    host=db_config.get_host(),
    port=db_config.get_port()
)

__all__ = ['db_manager', 'is_existing_context', 'DBMgr']
