"""
This module is used to import the configuration of the model.

Author: Ron Webb
Since: 1.0.0
"""

from query_ai.config.model_config import EmbeddingConfig, GeneratorConfig

embedding_config=EmbeddingConfig()
generator_config=GeneratorConfig()

__all__=['embedding_config', 'generator_config']
