import torch
from transformers import AutoTokenizer, AutoModel, AutoModelForQuestionAnswering, pipeline
from xyz.ronella.ml.query.ai.database import DBMgr

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

    def __init__(self, embedding_model_name: str, qa_model_name: str):
        """
        Initializes the ModelMgr with specified model names.

        Args:
        embedding_model_name (str): The name of the embedding model.
        qa_model_name (str): The name of the question answering model.
        """
        self.embedding_tokenizer = AutoTokenizer.from_pretrained(embedding_model_name)
        self.embedding_model = AutoModel.from_pretrained(embedding_model_name)

        self.qa_tokenizer = AutoTokenizer.from_pretrained(qa_model_name)
        self.qa_model = AutoModelForQuestionAnswering.from_pretrained(qa_model_name)

        self.qa_pipeline = pipeline("question-answering", model=self.qa_model, tokenizer=self.qa_tokenizer)

    def get_embedding(self, text: str):
        """
        Get the embedding of the text.

        Args:
        text (str): The text to embed.

        Returns:
        numpy.ndarray: The embedding of the text.
        """
        max_length = 256
        inputs = self.embedding_tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=max_length)
        with torch.no_grad():
            outputs = self.embedding_model(**inputs)

        return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

    def answer_question(self, db_manager: DBMgr, question: str):
        """
        Answer a question using the question answering model and database manager.

        Args:
        db_manager (DBMgr): The database manager to retrieve relevant contexts.
        question (str): The question to answer.

        Returns:
        list: A list of dictionaries containing the answers and their contexts.
        """
        question_embedding = self.get_embedding(question)

        results = []

        relevant_contexts = db_manager.execute(
            stmt="SELECT context, embedding <=> %s AS distance FROM qa_embeddings ORDER BY distance LIMIT 5",
            stmt_vars=(question_embedding,),
            output_logic=lambda ___connection, ___cursor: ___cursor.fetchall()
        )

        for context in relevant_contexts:
            result = self.qa_pipeline(question=question, context=context[0])
            result["question"] = question
            result["context"] = context[0]
            results.append(result)

        return results