from .ModelMgr import ModelMgr

embedding_model_name = "sentence-transformers/all-MiniLM-L6-v2"
qa_model_name = "bert-large-uncased-whole-word-masking-finetuned-squad"

model_manager = ModelMgr(embedding_model_name, qa_model_name)

__all__ = ["model_manager"]