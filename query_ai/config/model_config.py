"""
This file contains the configuration for the models used in the project.

Author: Ron Webb
Since: 1.0.0
"""

#pylint: disable=too-few-public-methods
class EmbeddingConfig:
    """
    Configuration class for the embedding model.
    """

    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    token_length = 384
    db_record_chunk_size = 300
    db_record_overlap = 50

class GeneratorConfig:
    """
    Configuration class for the generator model.
    """

    model_name = "google/flan-t5-large"
    token_length = 512
#pylint: enable=too-few-public-methods
