from query_ai.api import endpoints
from flask import Flask

if __name__ == '__main__':
    app = Flask(__name__)

    [endpoint(app) for endpoint in endpoints]

    app.run(debug=False, port=5000)