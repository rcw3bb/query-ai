from query_ai.database import db_manager
from query_ai.model import model_manager
from query_ai.util import create_sample_context

import nltk

nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('punkt', quiet=True)

create_sample_context(db_manager)

# Example usage
questions = [
    "What is the fox known for?",
    "What proverb emphasizes on perseverance in achieving long-term goals?",
    "Who wrote 'To be or not to be'?",
    "What is a subset of artificial intelligence?",
    "What is deep learning?",
    "What are some concerns with artificial intelligence?",
    "How to address the challenges in artificial intelligence?",
]

final_results = {}
for question in questions:
    results = model_manager.generate_answer(db_manager, question)
    for result in results:
        print(f"Context: {result['context']}")
        print(f"Question: {result['question']}")
        print(f"Generated Text: {result['generated_text']}")
        print("-" * 50)