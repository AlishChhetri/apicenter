"""Test the OpenAI text provider."""

import unittest
from unittest.mock import patch, MagicMock
import sys


class TestOpenAI(unittest.TestCase):
    """Test the OpenAI text provider."""

    @patch("apicenter.text.providers.openai.OpenAI")
    def test_call_openai_with_string_prompt(self, mock_openai_class):
        """Test that string prompts are handled correctly."""
        # Import inside the test to ensure the mock is applied
        from apicenter.text.providers.openai import call_openai

        # Setup mock client and response
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        mock_chat = MagicMock()
        mock_client.chat = mock_chat

        mock_completions = MagicMock()
        mock_chat.completions = mock_completions

        mock_create = MagicMock()
        mock_completions.create = mock_create

        # Mock the response structure
        mock_message = MagicMock()
        mock_message.content = "This is a test response"

        mock_choice = MagicMock()
        mock_choice.message = mock_message

        mock_response = MagicMock()
        mock_response.choices = [mock_choice]

        mock_create.return_value = mock_response

        # Call the function with a string prompt
        result = call_openai(
            model="gpt-4",
            prompt="Hello world",
            credentials={"api_key": "test_key", "organization": "test_org"},
            temperature=0.7,
            max_tokens=100,
        )

        # Check the result
        self.assertEqual(result, "This is a test response")

        # Check that OpenAI was initialized correctly
        mock_openai_class.assert_called_once_with(api_key="test_key", organization="test_org")

        # Get the call arguments
        mock_create.assert_called_once()
        args, kwargs = mock_create.call_args

        # Check that the parameters were correctly passed
        self.assertEqual(kwargs["model"], "gpt-4")
        self.assertEqual(len(kwargs["messages"]), 1)
        self.assertEqual(kwargs["messages"][0]["role"], "user")
        self.assertEqual(kwargs["messages"][0]["content"], "Hello world")
        self.assertEqual(kwargs["temperature"], 0.7)
        self.assertEqual(kwargs["max_tokens"], 100)

    @patch("apicenter.text.providers.openai.OpenAI")
    def test_call_openai_with_message_list(self, mock_openai_class):
        """Test that message lists are handled correctly."""
        # Import inside the test to ensure the mock is applied
        from apicenter.text.providers.openai import call_openai

        # Setup mock client and response
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        mock_chat = MagicMock()
        mock_client.chat = mock_chat

        mock_completions = MagicMock()
        mock_chat.completions = mock_completions

        mock_create = MagicMock()
        mock_completions.create = mock_create

        # Mock the response structure
        mock_message = MagicMock()
        mock_message.content = "This is a test response"

        mock_choice = MagicMock()
        mock_choice.message = mock_message

        mock_response = MagicMock()
        mock_response.choices = [mock_choice]

        mock_create.return_value = mock_response

        # Call the function with a message list
        messages = [
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": "Hello world"},
            {"role": "assistant", "content": "Hi there!"},
            {"role": "user", "content": "How are you?"},
        ]

        result = call_openai(
            model="gpt-4", prompt=messages, credentials={"api_key": "test_key"}, temperature=0.5
        )

        # Check the result
        self.assertEqual(result, "This is a test response")

        # Get the call arguments
        mock_create.assert_called_once()
        args, kwargs = mock_create.call_args

        # Check that the parameters were correctly passed
        self.assertEqual(kwargs["model"], "gpt-4")
        self.assertEqual(len(kwargs["messages"]), 4)
        self.assertEqual(kwargs["messages"][0]["role"], "system")
        self.assertEqual(kwargs["messages"][0]["content"], "You are a helpful assistant")
        self.assertEqual(kwargs["messages"][1]["role"], "user")
        self.assertEqual(kwargs["messages"][3]["role"], "user")
        self.assertEqual(kwargs["messages"][3]["content"], "How are you?")
        self.assertEqual(kwargs["temperature"], 0.5)


if __name__ == "__main__":
    unittest.main()
