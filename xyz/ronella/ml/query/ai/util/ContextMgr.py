from xyz.ronella.ml.query.ai.database import is_existing_context, DBMgr
from xyz.ronella.ml.query.ai.model import model_manager

def create_sample_context(db_manager: DBMgr):
    """
    Creates sample context data and inserts it into the database if it does not already exist.

    Args:
        db_manager (DBMgr): An instance of the database manager to execute database operations.

    Author: Ron Webb
    Since: 1.0.0
    """

    sample_texts = [
        "The quick brown fox jumps over the lazy dog. The fox is known for its agility and speed, while the dog is often characterized by its relaxed nature.",
        "A journey of a thousand miles begins with a single step. This proverb emphasizes the importance of starting and perseverance in achieving long-term goals.",
        "To be or not to be, that is the question. This famous line from Shakespeare's Hamlet reflects on the philosophical nature of existence and the challenges of life.",
    ]

    # Insert sample data and embeddings
    for text in sample_texts:
        if is_existing_context(db_manager, text):
            continue

        embedding = model_manager.get_embedding(text)

        db_manager.execute(stmt="INSERT INTO qa_embeddings (context, embedding) VALUES (%s, %s)",
                           stmt_vars=(text, embedding))