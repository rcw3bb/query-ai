"""
This module defines the Query class to handle query-related API endpoints.

Author: Ron Webb
Since: 1.0.0
"""

from flask import Flask, request, jsonify
from werkzeug.exceptions import UnsupportedMediaType

from query_ai.database import db_manager
from query_ai.model import model_manager

# pylint: disable=R0903
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

        try:
            success_status = 200
            bad_request = 400
            server_error = 500
            data = request.get_json()
            question = data.get('question')
            context = data.get('context')

            if context:
                response = model_manager.generate_answer(question, provided_context=context)
            elif question:
                response = model_manager.generate_answer(question, db_manager)
            else:
                return jsonify(''), bad_request

            if not response:
                return jsonify({'error': 'Error generating response.'}), server_error

            text = response[0]['generated_text']

            return jsonify({'answer': text}), success_status
        except UnsupportedMediaType:
            unsupported_media_type = 415
            return jsonify({'error': 'Unsupported Media Type'}), unsupported_media_type
# pylint: enable=R0903
