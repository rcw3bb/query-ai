from flask import Flask, request, make_response

from query_ai.database import is_existing_context, db_manager
from query_ai.model import model_manager
from query_ai.util.text_util import TextUtil

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

        response_code = 200

        paragraphs = TextUtil.split_by_paragraph(context)

        for paragraph in paragraphs:
            text_util = TextUtil()
            cleaned_text = text_util.clean_text(paragraph)

            embeddings = model_manager.get_embeddings(cleaned_text)

            for embedding_record in embeddings:
                chunk = embedding_record[3]

                if is_existing_context(db_manager, chunk):
                    continue

                chunk_id = embedding_record[0]
                start_word = embedding_record[1]
                end_word = embedding_record[2]
                embedding = embedding_record[4]

                db_manager.execute(stmt="""
                    INSERT INTO qa_embeddings (chunk_id, start_word, end_word, context, embedding)
                    VALUES (%s, %s, %s, %s, %s)
                    """, stmt_vars=(chunk_id, start_word, end_word, chunk, embedding))

                response_code = 201

        return make_response('', response_code)