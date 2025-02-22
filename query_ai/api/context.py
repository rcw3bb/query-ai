"""
This module defines the Context class to handle context-related API endpoints.

Author: Ron Webb
Since: 1.0.0
"""

from flask import Flask, request, make_response

from query_ai.database import is_existing_context, db_manager
from query_ai.model import model_manager
from query_ai.util import text_util

# pylint: disable=R0903
class Context:
    """
    A class to handle context-related API endpoints.

    Author: Ron Webb
    Since: 1.0.0
    """

    def __init__(self, app: Flask):
        """
        Initializes the Context class with the given Flask app and sets up the URL rule.

        Parameters:
        app (Flask): The Flask application instance.
        """
        self.app = app
        self.app.add_url_rule('/api/v1/context', view_func=self.save_context, methods=['PUT'])

    def __persist(self, embedding_record):
        chunk_id = embedding_record[0]
        start_word = embedding_record[1]
        end_word = embedding_record[2]
        chunk = embedding_record[3]
        embedding = embedding_record[4]

        db_manager.execute(stmt="""
                        INSERT INTO qa_embeddings (chunk_id, start_word, end_word, context, embedding)
                        VALUES (%s, %s, %s, %s, %s)
                        """, stmt_vars=(chunk_id, start_word, end_word, chunk, embedding))

    def save_context(self):
        """
        Handles the PUT request to save context data.

        This method:
        - Retrieves JSON data from the request.
        - Splits the context into paragraphs.
        - Cleans each paragraph.
        - Generates embeddings for each cleaned paragraph.
        - Checks if the context already exists in the database.
        - Inserts new context data into the database if it does not already exist.

        Returns:
        Response: A Flask response object with status code 201.
        """
        data = request.get_json()
        context = data.get('context')
        created_status = 201
        success_status = 200
        bad_request = 400
        response_code = success_status if context else bad_request
        paragraphs = text_util.split_by_paragraph(context)

        for paragraph in paragraphs:
            cleaned_text = text_util.clean_text(paragraph)
            embeddings = model_manager.get_embeddings(cleaned_text)

            for embedding_record in embeddings:
                chunk = embedding_record[3]

                if is_existing_context(db_manager, chunk):
                    continue

                self.__persist(embedding_record)

                response_code = created_status

        return make_response('', response_code)
# pylint: enable=R0903
