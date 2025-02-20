import torch

from transformers import (AutoTokenizer, AutoModel, AutoModelForQuestionAnswering, pipeline,
                          AutoModelForSeq2SeqLM)

from query_ai.config import embedding_config, generator_config
from query_ai.database import DBMgr

from query_ai.logger import get_logger
from query_ai.model import model_manager


class ModelMgr:
    """
    A class to manage models.

    Author: Ron Webb
    Since: 1.0.0
    """

    def __init__(self):
        """
        Initializes the ModelMgr with specified model names.

        Args:
        embedding_model_name (str): The name of the embedding model.
        qa_model_name (str): The name of the question answering model.
        """
        self.log = get_logger(__name__)
        self.embedding_tokenizer = AutoTokenizer.from_pretrained(embedding_config.model_name)
        self.embedding_model = AutoModel.from_pretrained(embedding_config.model_name)
        self.generator_tokenizer = AutoTokenizer.from_pretrained(generator_config.model_name)
        self.generator_model = AutoModelForSeq2SeqLM.from_pretrained(generator_config.model_name)
        self.generator_pipeline = pipeline("text2text-generation",
                                           model=self.generator_model,
                                           tokenizer=self.generator_tokenizer)

    def get_embedding(self, text: str):
        """
        Get the embedding of the text.

        Args:
        text (str): The text to embed.

        Returns:
        numpy.ndarray: The embedding of the text.
        """

        self.log.debug(f"Getting embedding for text:\n{text}")

        inputs = self.embedding_tokenizer(text, return_tensors="pt", padding=True, truncation=True,
                                          max_length=embedding_config.token_length)
        with torch.no_grad():
            outputs = self.embedding_model(**inputs)

        return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

    def get_embeddings(self, text: str, chunk_size=embedding_config.token_length, overlap=50):
        """
        Splits the text into overlapping chunks and gets the embedding for each chunk.

        Args:
        text (str): The text to embed.
        chunk_size (int, optional): The size of each chunk. Defaults to embedding_token_length.
        overlap (int, optional): The number of words to overlap between chunks. Defaults to 50.

        Returns:
        list: A list of tuples containing the chunk index, start index, end index, chunk text, and its embedding.
        """

        words = text.split()
        output = []
        i = 0
        while i * (chunk_size - overlap) < len(words):
            start = i * (chunk_size - overlap)
            end = min(start + chunk_size, len(words))
            chunk = " ".join(words[start:end])
            embedding = self.get_embedding(chunk)
            output.append((i, start, end, chunk, embedding))
            i += 1

        return output

    def format_conversation(self, conversation, suffix):
        """
        Formats a conversation into a string suitable for prompting the model.

        Args:
        conversation (list): A list of dictionaries representing the conversation. Each dictionary should have 'role' and 'content' keys.

        Returns:
        str: The formatted conversation as a string.
        """

        formatted_conversation = ""
        for message in conversation:
            formatted_conversation += f"{message['role']}: {message['content']}\n"
        formatted_conversation += suffix  # Important for prompting the model

        self.log.debug(f"Formatted conversation:\n{formatted_conversation}")

        return formatted_conversation

    def __generate(self, chat, suffix):
        formatted_chat = self.format_conversation(chat, suffix)

        result = self.generator_pipeline(formatted_chat,
                                         #truncation=True,
                                         max_length=generator_config.token_length,
                                         )[0]

        return result

    def generate_answer(self, question: str, db_manager: DBMgr = None, provided_context: str = None):
        """
        Answer a question using the generator model and database manager.

        Args:
        db_manager (DBMgr): The database manager to retrieve relevant contexts.
        question (str): The question to answer.

        Returns:
        list: A list of dictionaries containing the answers and their contexts.
        """

        question_embedding = self.get_embedding(question)

        results = []
        relevant_contexts = []

        if provided_context:
            distance = 0
            relevant_contexts = [(provided_context, distance)]
        elif db_manager:
            relevant_contexts = db_manager.execute(
                stmt="SELECT context, embedding <=> %s AS distance FROM qa_embeddings ORDER BY distance LIMIT 1",
                stmt_vars=(question_embedding,),
                output_logic=lambda ___connection, ___cursor: ___cursor.fetchall()
            )

        for context in relevant_contexts:

            retrieved_context = context[0]
            message = f"""You are a chatbot that can answer questions based on the given context.
Context: 

{retrieved_context}
"""
            chat = [
                {'role': 'system', 'content' : message},
                {'role': 'assistant', 'content' : "Must answer politely and informatively."},
                {'role': 'assistant', 'content' : "Respond 'I don't know' if out of context."},
                {'role': 'user', 'content' : question},
            ]

            result = self.__generate(chat, "assistant:")
            response = result['generated_text']

            self.log.debug(f"Original response:\n{response}")

            is_valid_response = self.validate_answer(retrieved_context, response)

            if not is_valid_response:
                result['generated_text'] = "I don't know"

            result["question"] = question
            result["context"] = retrieved_context

            self.log.debug(f"Final response:\n{result['generated_text']}")

            results.append(result)

        return results

    def validate_answer(self, context, response):
        """
        Validates the response based on the given context.

        Args:
        context (str): The context in which the response should be validated.
        response (str): The response to validate.

        Returns:
        int: 1 if the response is valid within the context, 0 otherwise.
        """

        message = f"""You are a quality analyst that validates the response if it in with context.
            
Context: 

{context}

Response:

{response}
        """
        chat = [
            {'role': 'system', 'content' : message},
            {'role': 'analyst', 'content' : "Must answer 1 if correct, 0 if incorrect."},
        ]
        result = self.__generate(chat, "analyst:")
        is_valid_response = result['generated_text'].strip()

        self.log.debug(f"Validation result: {is_valid_response}")

        return int(is_valid_response)