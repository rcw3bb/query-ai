from flask import Flask, request, jsonify

from query_ai.database import db_manager
from query_ai.model import model_manager

class Query:
    """
    A class to handle query requests to the Flask application.

    Author: Ron Webb
    Since: 1.0.0
    """

    def __init__(self, app: Flask):
        """
        Initializes the Query class with the given Flask application instance.

        Parameters:
        app (Flask): The Flask application instance.
        """
        self.app = app
        self.app.add_url_rule('/api/v1/query', view_func=self.query, methods=['POST'])

    def query(self):
        """
        Handles POST requests to the /api/v1/query endpoint.

        Expects a JSON payload with a 'question' field.
        Uses the model_manager to generate an answer based on the question.
        Returns a JSON response with the generated answer.

        Returns:
        Response: A Flask JSON response containing the answer and a status code 200.
        """
        data = request.get_json()
        question = data.get('question')
        context = data.get('context')

        if context:
            response = model_manager.generate_answer(question, provided_context=context)
        else:
            response = model_manager.generate_answer(question, db_manager)

        text = response[0]['generated_text']

        return jsonify({'answer': text}), 200