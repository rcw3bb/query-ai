"""
A module to manage models.

Author: Ron Webb
Since: 1.0.0
"""

import torch

from transformers import (AutoTokenizer, AutoModel, pipeline, AutoModelForSeq2SeqLM)

from query_ai.config import embedding_config, generator_config
from query_ai.database import DBMgr
from query_ai.database.db_manager import DBException

from query_ai.logger import get_logger


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

        self.log.debug("Getting embedding for text:\n%s", text)

        inputs = self.embedding_tokenizer(text, return_tensors="pt", padding=True, truncation=True,
                                          max_length=embedding_config.token_length)
        with torch.no_grad():
            outputs = self.embedding_model(**inputs)

        return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

    def get_embeddings(self, text: str, chunk_size=embedding_config.db_record_chunk_size,
                       overlap=embedding_config.db_record_overlap):
        """
        Splits the text into overlapping chunks and gets the embedding for each chunk.

        Args:
        text (str): The text to embed.
        chunk_size (int, optional): The size of each chunk. Defaults to embedding_token_length.
        overlap (int, optional): The number of words to overlap between chunks. Defaults to 50.

        Returns:
        list: A list of tuples containing the chunk index, start index, end index, chunk text,
            and its embedding.
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
        conversation (list): A list of dictionaries representing the conversation. Each dictionary
            should have 'role' and 'content' keys.

        Returns:
        str: The formatted conversation as a string.
        """

        formatted_conversation = ""
        for message in conversation:
            formatted_conversation += f"{message['role']}: {message['content']}\n"
        formatted_conversation += suffix  # Important for prompting the model

        self.log.debug("Formatted conversation:\n%s", formatted_conversation)

        return formatted_conversation

    def __pipeline(self, chat, suffix):
        formatted_chat = self.format_conversation(chat, suffix)

        result = self.generator_pipeline(formatted_chat,
                                         #truncation=True,
                                         max_length=generator_config.token_length,
                                         )[0]

        return result

    def __ask_question(self, context, question):
        message = f"""You are a chatbot that can answer questions based on the given context.
Context: 

{context}
"""
        chat = [
            {'role': 'system', 'content' : message},
            {'role': 'assistant', 'content' : "Must answer politely and informatively."},
            {'role': 'assistant', 'content' : "Respond 'I don't know' if out of context."},
            {'role': 'user', 'content' : question},
        ]

        return self.__pipeline(chat, "assistant:")

    def __retrieve_context(self, db_manager, question):
        question_embedding = self.get_embedding(question)

        return db_manager.execute(
            stmt="SELECT context, embedding <=> %s AS distance FROM qa_embeddings "
                 "ORDER BY distance LIMIT 1",
            stmt_vars=(question_embedding,),
            output_logic=lambda ___connection, ___cursor: ___cursor.fetchall()
        )

    def __generate_result(self, context, question):

        context_first_field = 0
        retrieved_context = context[context_first_field]
        is_valid_question = self.validate_question(retrieved_context, question)
        result = {}

        if is_valid_question:
            result = self.__ask_question(retrieved_context, question)
        else:
            result['generated_text'] = "I don't know"

        response = result['generated_text']

        self.log.debug("Response:\n%s", response)

        result["question"] = question
        result["context"] = retrieved_context

        return result

    def generate_answer(self, question: str, db_manager: DBMgr = None,
                        provided_context: str = None):
        """
        Answer a question using the generator model and database manager.

        Args:
        db_manager (DBMgr): The database manager to retrieve relevant contexts.
        question (str): The question to answer.

        Returns:
        list: A list of dictionaries containing the answers and their contexts.
        """

        results = []
        relevant_contexts = []

        if provided_context:
            distance = 0
            relevant_contexts = [(provided_context, distance)]
        elif db_manager:
            try:
                relevant_contexts = self.__retrieve_context(db_manager, question)
            except DBException:
                results.append({"generated_text": "Sorry, I cannot access my database. "
                                                  "Try again later.",
                                "question": question, "context": ""})

        for context in relevant_contexts:
            result = self.__generate_result(context, question)
            results.append(result)

        if not results:
            self.log.debug("The database is empty.")
            results.append({"generated_text": "The context database is empty.",
                            "question": question, "context": ""})

        return results

    def validate_question(self, context, question):
        """
        Validates the question if it is valid for the given context.

        Args:
        context (str): The context in which the question must be based on.
        question (str): The question related to the context.

        Returns:
        int: 1 if the response is valid within the context, 0 otherwise.
        """

        message = f"""You are an analyst that validates if question can be answered from the
given context.

Context: 

{context}

Question:

{question}
        """
        chat = [
            {'role': 'system', 'content' : message},
            {'role': 'analyst', 'content' : "Must answer 1 if yes, 0 if no."},
        ]
        result = self.__pipeline(chat, "analyst:")
        is_valid_question = result['generated_text'].strip()

        self.log.debug("Validation result: %s", is_valid_question)

        int_output = int(is_valid_question)

        if not int_output:
            self.log.debug("The question is out of context.")

        return int_output
