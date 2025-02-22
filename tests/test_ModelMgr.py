import unittest
from unittest.mock import patch, MagicMock

from query_ai.database import DBException
from query_ai.model import model_manager, ModelMgr


class TestModelMgr(unittest.TestCase):

    def test_format_conversation_formats_correctly(self):
        conversation = [
            {'role': 'user', 'content': 'Hello'},
            {'role': 'assistant', 'content': 'Hi there!'}
        ]
        expected_output = "user: Hello\nassistant: Hi there!\nassistant:"
        self.assertEqual(model_manager.format_conversation(conversation, 'assistant:'), expected_output)

    def test_format_conversation_empty_conversation(self):
        conversation = []
        expected_output = "assistant:"
        self.assertEqual(model_manager.format_conversation(conversation, 'assistant:'), expected_output)

    def test_format_conversation_single_message(self):
        conversation = [{'role': 'user', 'content': 'Hello'}]
        expected_output = "user: Hello\nassistant:"
        self.assertEqual(model_manager.format_conversation(conversation, 'assistant:'), expected_output)


    @patch('query_ai.model.model_manager.get_logger')
    @patch('query_ai.model.model_manager.AutoTokenizer.from_pretrained')
    @patch('query_ai.model.model_manager.AutoModel.from_pretrained')
    @patch('query_ai.model.model_manager.AutoModelForSeq2SeqLM.from_pretrained')
    @patch('query_ai.model.model_manager.pipeline')
    def test_initializes_with_models(self, mock_pipeline, mock_auto_model_seq2seq, mock_auto_model, mock_auto_tokenizer, mock_get_logger):
        mock_get_logger.return_value = MagicMock()
        mock_auto_tokenizer.return_value = MagicMock()
        mock_auto_model.return_value = MagicMock()
        mock_auto_model_seq2seq.return_value = MagicMock()
        mock_pipeline.return_value = MagicMock()

        model_mgr = ModelMgr()

        self.assertIsNotNone(model_mgr.embedding_tokenizer)
        self.assertIsNotNone(model_mgr.embedding_model)
        self.assertIsNotNone(model_mgr.generator_tokenizer)
        self.assertIsNotNone(model_mgr.generator_model)
        self.assertIsNotNone(model_mgr.generator_pipeline)

    @patch('query_ai.model.model_manager.get_logger')
    @patch('query_ai.model.model_manager.AutoTokenizer.from_pretrained')
    @patch('query_ai.model.model_manager.AutoModel.from_pretrained')
    def test_get_embedding_returns_correct_shape(self, mock_auto_model, mock_auto_tokenizer, mock_get_logger):
        mock_get_logger.return_value = MagicMock()
        mock_tokenizer = MagicMock()
        mock_auto_tokenizer.return_value = mock_tokenizer
        mock_model = MagicMock()
        mock_auto_model.return_value = mock_model
        mock_model.return_value.last_hidden_state.mean.return_value.squeeze.return_value.numpy.return_value = [0.1, 0.2, 0.3]

        model_mgr = ModelMgr()
        embedding = model_mgr.get_embedding("test text")

        self.assertEqual(len(embedding), 3)

    @patch('query_ai.model.model_manager.get_logger')
    @patch('query_ai.model.model_manager.AutoTokenizer.from_pretrained')
    @patch('query_ai.model.model_manager.AutoModel.from_pretrained')
    def test_get_embeddings_splits_text_correctly(self, mock_auto_model, mock_auto_tokenizer, mock_get_logger):
        mock_get_logger.return_value = MagicMock()
        mock_tokenizer = MagicMock()
        mock_auto_tokenizer.return_value = mock_tokenizer
        mock_model = MagicMock()
        mock_auto_model.return_value = mock_model
        mock_model.return_value.last_hidden_state.mean.return_value.squeeze.return_value.numpy.return_value = [0.1, 0.2, 0.3]

        model_mgr = ModelMgr()
        text = "This is a test text that will be split into chunks."
        embeddings = model_mgr.get_embeddings(text, chunk_size=5, overlap=2)

        self.assertEqual(len(embeddings), 4)
        self.assertEqual(embeddings[0][3], "This is a test text")
        self.assertEqual(embeddings[1][3], "test text that will be")
        self.assertEqual(embeddings[2][3], "will be split into chunks.")
        self.assertEqual(embeddings[3][3], "into chunks.")

    @patch('query_ai.model.model_manager.get_logger')
    @patch('query_ai.model.model_manager.pipeline')
    def test_generate_answer_handles_empty_database(self, mock_pipeline, mock_get_logger):
        mock_get_logger.return_value = MagicMock()
        mock_pipeline.return_value = MagicMock()

        model_mgr = ModelMgr()
        db_manager = MagicMock()
        db_manager.execute.side_effect = DBException

        result = model_mgr.generate_answer("What is AI?", db_manager=db_manager)

        self.assertEqual(result[0]['generated_text'], "Sorry, I cannot access my database. Try again later.")
        self.assertEqual(result[0]['question'], "What is AI?")
        self.assertEqual(result[0]['context'], "")

    @patch('query_ai.model.model_manager.get_logger')
    @patch('query_ai.model.model_manager.pipeline')
    def test_generate_answer_handles_provided_context(self, mock_pipeline, mock_get_logger):
        mock_get_logger.return_value = MagicMock()

        pipeline_instance = MagicMock()
        pipeline_instance.side_effect = [
            [{'generated_text': '1'}],
            [{'generated_text': 'AI stands for Artificial Intelligence.'}],
        ]

        mock_pipeline.return_value = pipeline_instance

        model_mgr = ModelMgr()
        provided_context = "AI stands for Artificial Intelligence."
        result = model_mgr.generate_answer("What is AI?", provided_context=provided_context)

        self.assertEqual(result[0]['generated_text'], "AI stands for Artificial Intelligence.")
        self.assertEqual(result[0]['question'], "What is AI?")
        self.assertEqual(result[0]['context'], provided_context)

    @patch.object(ModelMgr, 'validate_question', return_value=0)
    def test_generate_result_invalid_question(self, mock_validate_question):
        context = "context text"
        question = "What is the context?"

        model_mgr = ModelMgr()
        result = model_mgr.generate_answer(question, provided_context=context)

        self.assertEqual(result[0]['generated_text'], "I don't know")

    @patch.object(ModelMgr, 'validate_question', return_value=1)
    def test_generate_result_empty_database(self, mock_validate_question):
        model_mgr = ModelMgr()
        result = model_mgr.generate_answer(None, provided_context=None)

        self.assertEqual(result[0]['generated_text'], "The context database is empty.")

    @patch('query_ai.model.model_manager.pipeline')
    def test_out_of_context_question(self, mock_pipeline):

        mock_pipeline.return_value.side_effect = [[{'generated_text': '0'}]]

        model_mgr = ModelMgr()
        result = model_mgr.validate_question("Context", "Question")

        self.assertEqual(result, 0)

if __name__ == '__main__':
    unittest.main()