import unittest
from query_ai.model.model_manager import ModelMgr

class TestModelMgr(unittest.TestCase):

    def test_format_conversation_formats_correctly(self):
        conversation = [
            {'role': 'user', 'content': 'Hello'},
            {'role': 'assistant', 'content': 'Hi there!'}
        ]
        expected_output = "user: Hello\nassistant: Hi there!\nassistant:"
        self.assertEqual(ModelMgr.format_conversation(conversation), expected_output)

    def test_format_conversation_empty_conversation(self):
        conversation = []
        expected_output = "assistant:"
        self.assertEqual(ModelMgr.format_conversation(conversation), expected_output)

    def test_format_conversation_single_message(self):
        conversation = [{'role': 'user', 'content': 'Hello'}]
        expected_output = "user: Hello\nassistant:"
        self.assertEqual(ModelMgr.format_conversation(conversation), expected_output)

if __name__ == '__main__':
    unittest.main()