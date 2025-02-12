from query_ai.api.context import Context
from query_ai.api.query import Query

endpoints = (
    lambda app: Context(app),
    lambda app: Query(app),
)

__all__ = ['endpoints']