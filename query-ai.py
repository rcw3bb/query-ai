from xyz.ronella.ml.query.ai.database import db_manager
from xyz.ronella.ml.query.ai.model import model_manager
from xyz.ronella.ml.query.ai.util import create_sample_context

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
    "What is artificial intelligence?",
    "What is the potential of artificial intelligence?",
]

final_results = {}
for question in questions:
    results = model_manager.answer_question(db_manager, question)
    for result in results:
        if result['score'] < 0.3:  # Threshold for unanswerable questions
            print(f"Question: {result['question']}")
            print(f"[Answer: This question is unanswerable based on the given context. ({result['answer']})]")
            print(f"Context: {result['context']}")
            print(f"Score: {result['score']:.4f}")
        else:
            if result['question'] not in final_results:
                final_results[result['question']] = result['answer']

            print(f"Question: {result['question']}")
            print(f"Answer: {result['answer']}")
            print(f"Context: {result['context']}")
            print(f"Score: {result['score']:.4f}")

        print("-" * 50)

print("\n\n----[Final Answers]-------------------------------")
for key, value in final_results.items():
    print(f"Question: {key}")
    print(f"Answer: {value}")
    print("-" * 50)
