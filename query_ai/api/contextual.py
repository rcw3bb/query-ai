from flask import Flask, request, jsonify
from query_ai.model import model_manager

class Contextual:
    """
    A class to handle contextual queries.

    Author: Ron Webb
    Since: 1.0.0
    """

    def __init__(self, app: Flask):
        """
        Initializes the Contextual class with a Flask app and sets up the URL rule.

        Parameters:
        app (Flask): The Flask application instance.
        """
        self.app = app
        self.app.add_url_rule('/api/v1/contextual', view_func=self.contextual, methods=['POST'])

    def contextual(self):
        """
        Handles POST requests to the /api/v1/contextual endpoint.

        Expects a JSON payload with 'context' and 'question' fields.
        Uses the model_manager to generate an answer based on the provided context and question.

        Returns:
        Response: A JSON response containing the generated answer with a status code of 200.
        """
        
        data = request.get_json()
        context = data.get('context')
        question = data.get('question')

        response = model_manager.generate_answer(question, provided_context=context)
        text = response[0]['generated_text']

        return jsonify({'answer': text}), 200