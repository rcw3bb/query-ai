from query_ai.api import endpoints
from flask import Flask
from waitress import serve

from query_ai.logger import get_logger

if __name__ == '__main__':

    logger = get_logger(__name__)

    logger.info("Query AI application")

    app = Flask(__name__)

    [endpoint(app) for endpoint in endpoints]

    serve(app, host='0.0.0.0', port=5000)