"""Test the Ollama text provider."""

import unittest
from unittest.mock import patch, MagicMock
from apicenter.text.providers.ollama import call_ollama


class TestOllama(unittest.TestCase):
    """Test the Ollama text provider."""

    @patch("ollama.chat")
    def test_call_ollama_with_options(self, mock_chat):
        """Test that options are passed correctly through the options parameter."""
        # Setup mock response
        mock_chat.return_value = {"message": {"content": "This is a test response"}}

        # Call with parameters that should go to options
        result = call_ollama(
            model="llama2",
            prompt="Hello world",
            temperature=0.7,
            top_p=0.95,
            top_k=40,
            num_predict=100,
        )

        # Check that ollama.chat was called correctly
        call_args = mock_chat.call_args

        # Check that the model is correct
        self.assertEqual(call_args[1]["model"], "llama2")

        # Check that the messages are correct
        self.assertEqual(call_args[1]["messages"][0]["role"], "user")
        self.assertEqual(call_args[1]["messages"][0]["content"], "Hello world")

        # Check that options were passed correctly
        self.assertIn("options", call_args[1])
        self.assertEqual(call_args[1]["options"]["temperature"], 0.7)
        self.assertEqual(call_args[1]["options"]["top_p"], 0.95)
        self.assertEqual(call_args[1]["options"]["top_k"], 40)
        self.assertEqual(call_args[1]["options"]["num_predict"], 100)

        # Check the result
        self.assertEqual(result, "This is a test response")

    @patch("ollama.chat")
    def test_call_ollama_with_system_message(self, mock_chat):
        """Test that system messages are handled correctly."""
        # Setup mock response
        mock_chat.return_value = {"message": {"content": "This is a test response"}}

        # Call with a system message in prompt
        result = call_ollama(
            model="llama2",
            prompt=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": "Hello world"},
            ],
        )

        # Check that ollama.chat was called correctly
        call_args = mock_chat.call_args

        # Check that the messages contain only the user message with system prepended
        messages = call_args[1]["messages"]
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0]["role"], "user")
        self.assertTrue(messages[0]["content"].startswith("[System: You are a helpful assistant]"))
        self.assertTrue("Hello world" in messages[0]["content"])

        # Check the result
        self.assertEqual(result, "This is a test response")


if __name__ == "__main__":
    unittest.main()
