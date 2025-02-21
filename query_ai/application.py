"""
This module serves as the entry point for the Query AI application.
It initializes the logger, creates a Flask application instance,
registers all endpoints, and serves the application using Waitress.
"""

from flask import Flask
from waitress import serve

from query_ai.api import endpoints
from query_ai.logger import get_logger

def main():
    """
    This function serves as the entry point for the Query AI application.
    :return: None
    """

    logger = get_logger(__name__)

    logger.info("Query AI application")

    app = Flask(__name__)

    for endpoint in endpoints:
        endpoint(app)

    serve(app, host='0.0.0.0', port=5000)

if __name__ == '__main__':

    main()
