"""
This module is used to initialize the text_util module.

Author: Ron Webb
Since: 1.0.0
"""

import nltk
from dotenv import load_dotenv
from .text_util import TextUtil

load_dotenv()

nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('punkt', quiet=True)

text_util = TextUtil()

__all__ = ['text_util']
