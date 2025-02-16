import nltk
from dotenv import load_dotenv
load_dotenv()

nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('punkt', quiet=True)