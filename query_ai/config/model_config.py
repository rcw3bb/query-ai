class EmbeddingConfig:
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    token_length = 384
    db_record_chunk_size = 300
    db_record_overlap = 50

class GeneratorConfig:
    model_name = "google/flan-t5-large"
    token_length = 512
