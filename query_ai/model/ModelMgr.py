import torch

from transformers import (AutoTokenizer, AutoModel, AutoModelForQuestionAnswering, pipeline,
                          AutoModelForSeq2SeqLM)

from query_ai.database import DBMgr
from query_ai.commons import embedding_token_length, generator_model_name, embedding_model_name


class ModelMgr:
    """
    A class to manage models for embedding and question answering.

    Attributes:
    embedding_tokenizer (AutoTokenizer): Tokenizer for the embedding model.
    embedding_model (AutoModel): Embedding model.
    qa_tokenizer (AutoTokenizer): Tokenizer for the question answering model.
    qa_model (AutoModelForQuestionAnswering): Question answering model.
    qa_pipeline (pipeline): Pipeline for question answering.

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
        self.embedding_tokenizer = AutoTokenizer.from_pretrained(embedding_model_name)
        self.embedding_model = AutoModel.from_pretrained(embedding_model_name)

        self.generator_tokenizer = AutoTokenizer.from_pretrained(generator_model_name)
        self.generator_model = AutoModelForSeq2SeqLM.from_pretrained(generator_model_name)
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

        inputs = self.embedding_tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=embedding_token_length)
        with torch.no_grad():
            outputs = self.embedding_model(**inputs)

        return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

    def get_embeddings(self, text: str, chunk_size=embedding_token_length, overlap=50):
        """
        Splits the text into overlapping chunks and gets the embedding for each chunk.

        Args:
        text (str): The text to embed.
        chunk_size (int, optional): The size of each chunk. Defaults to embedding_token_length.
        overlap (int, optional): The number of words to overlap between chunks. Defaults to 0.

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

    @staticmethod
    def format_conversation(conversation):
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
        formatted_conversation += "assistant:"  # Important for prompting the model
        return formatted_conversation

    def generate_answer(self, db_manager: DBMgr, question: str):
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

        relevant_contexts = db_manager.execute(
            stmt="SELECT context, embedding <=> %s AS distance FROM qa_embeddings ORDER BY distance LIMIT 1",
            stmt_vars=(question_embedding,),
            output_logic=lambda ___connection, ___cursor: ___cursor.fetchall()
        )

        for context in relevant_contexts:

            message = f"""You are a chatbot that can answer questions based on the given context.
Context: 

{context[0]}

Your answer must be paraphrased from the context.
"""
            chat = [
                {'role': 'system', 'content' : message},
                {'role': 'user', 'content' : question}
            ]

            formatted_chat = ModelMgr.format_conversation(chat)

            result = self.generator_pipeline(formatted_chat,
                                             max_length=len(formatted_chat) + 50,
                                             )[0]

            result["question"] = question
            result["context"] = context[0]
            results.append(result)

        return results