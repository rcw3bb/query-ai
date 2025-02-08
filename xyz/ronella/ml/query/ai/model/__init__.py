from .ModelMgr import ModelMgr
from xyz.ronella.ml.query.ai.commons import embedding_model_name, qa_model_name

model_manager = ModelMgr(embedding_model_name, qa_model_name)

__all__ = ["model_manager"]