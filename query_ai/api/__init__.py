"""
This module is used to import all the endpoints of the API.

Author: Ron Webb
Since: 1.0.0
"""

from query_ai.api.context import Context
from query_ai.api.query import Query

endpoints = (
    lambda app: Context(app), #pylint: disable=unnecessary-lambda
    lambda app: Query(app), #pylint: disable=unnecessary-lambda
)

__all__ = ['endpoints']
