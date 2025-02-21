"""
A utility class for text processing tasks such as splitting text into paragraphs,

Author: Ron Webb
Since: 1.0.0
"""

import re

from nltk import word_tokenize #pylint: disable=unused-import
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from query_ai.logger import get_logger


class TextUtil:
    """
    A utility class for text processing tasks such as splitting text into paragraphs,
    removing emojis, and cleaning text by removing HTML tags and other elements.

    Author: Ron Webb
    Since: 1.0.0
    """

    def __init__(self):
        """
        Initializes the TextUtil class with stop words and a lemmatizer.
        """
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        self.log = get_logger(__name__)

    def split_by_paragraph(self, text):
        """
        Splits a large text into paragraphs.

        Handles various newline characters and empty paragraphs.

        Args:
            text (str): The input text.

        Returns:
            list: A list of strings, where each string is a paragraph.
                  Returns an empty list if the input text is empty or None.
        """
        if not text:
            return []

        # Normalize newline characters (Windows, Linux, Mac)
        text = text.replace("\r\n", "\n").replace("\r", "\n")

        paragraphs = text.split("\n")

        paragraphs = [p.strip() for p in paragraphs if p.strip()] #Removes empty paragraphs

        self.log.debug("Split text by paragraph:\n%s", paragraphs)

        return paragraphs

    def __remove_emojis(self, text):
        """
        Removes emojis from the input text.

        Args:
            text (str): The input text.

        Returns:
            str: The text with emojis removed.
        """
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   "]", flags=re.UNICODE)

        cleaned_text = emoji_pattern.sub(r'', text) # no emoji

        self.log.debug("Removed emojis from text:\n%s", cleaned_text)

        return cleaned_text

    def clean_text(self, text):
        """
        Cleans the input text by removing HTML tags and emojis.

        Args:
            text (str): The input text.

        Returns:
            str: The cleaned text.
        """
        # text = text.lower()  # Lowercasing
        # text = text.translate(str.maketrans('', '', string.punctuation))  # Remove punctuation
        # text = re.sub(r'\d+', '', text)  # Remove numbers
        text = re.sub(r'<.*?>', '', text) # Remove HTML tags
        text = self.__remove_emojis(text) # Remove emojis
        # words = word_tokenize(text)
        # words = [word for word in words if word not in self.stop_words] # Remove Stop words
        # words = [self.lemmatizer.lemmatize(word) for word in words] # Lemmatization
        # cleaned_text = " ".join(words)

        self.log.debug("Cleaned text:\n%s", text)

        return text
