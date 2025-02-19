from query_ai.api import endpoints
from flask import Flask

from query_ai.logger import get_logger

if __name__ == '__main__':

    logger = get_logger(__name__)

    logger.info("Query AI application")

    app = Flask(__name__)

    [endpoint(app) for endpoint in endpoints]

    app.run(debug=False, port=5000)