import unittest
from query_ai.util.text_util import TextUtil

class TestTextUtil(unittest.TestCase):

    def setUp(self):
        self.text_util = TextUtil()

    def test_split_by_paragraph_handles_empty_text(self):
        self.assertEqual(self.text_util.split_by_paragraph(""), [])

    def test_split_by_paragraph_handles_none_text(self):
        self.assertEqual(self.text_util.split_by_paragraph(None), [])

    def test_split_by_paragraph_splits_text_into_paragraphs(self):
        text = "Paragraph 1.\n\nParagraph 2.\n\nParagraph 3."
        expected = ["Paragraph 1.", "Paragraph 2.", "Paragraph 3."]
        self.assertEqual(self.text_util.split_by_paragraph(text), expected)

    def test_split_by_paragraph_removes_empty_paragraphs(self):
        text = "Paragraph 1.\n\n\nParagraph 2.\n\n\n\nParagraph 3."
        expected = ["Paragraph 1.", "Paragraph 2.", "Paragraph 3."]
        self.assertEqual(self.text_util.split_by_paragraph(text), expected)

    def test_clean_text_removes_html_tags(self):
        text = "This is a <b>bold</b> statement."
        expected = "This is a bold statement."
        self.assertEqual(self.text_util.clean_text(text), expected)

    def test_clean_text_removes_emojis(self):
        text = "This is a test 😊."
        expected = "This is a test ."
        self.assertEqual(self.text_util.clean_text(text), expected)

if __name__ == '__main__':
    unittest.main()