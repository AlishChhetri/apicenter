"""Test the Anthropic text provider."""

import unittest
from unittest.mock import patch, MagicMock
import sys


class TestAnthropic(unittest.TestCase):
    """Test the Anthropic text provider."""

    @patch("apicenter.text.providers.anthropic.Anthropic")
    def test_call_anthropic_with_string_prompt(self, mock_anthropic_class):
        """Test that string prompts are handled correctly."""
        # Import inside the test to ensure the mock is applied
        from apicenter.text.providers.anthropic import call_anthropic

        # Setup mock client and response
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client

        mock_messages = MagicMock()
        mock_client.messages = mock_messages

        mock_create = MagicMock()
        mock_messages.create = mock_create

        # Mock return value
        mock_content = MagicMock()
        mock_content.text = "This is a test response"
        mock_create.return_value = MagicMock(content=[mock_content])

        # Call the function with a string prompt
        result = call_anthropic(
            model="claude-3-sonnet-20240229",
            prompt="Hello world",
            credentials={"api_key": "test_key"},
            temperature=0.7,
        )

        # Check the result
        self.assertEqual(result, "This is a test response")

        # Get the call arguments
        mock_create.assert_called_once()
        args, kwargs = mock_create.call_args

        # Check that the parameters were correctly passed
        self.assertEqual(kwargs["model"], "claude-3-sonnet-20240229")
        self.assertEqual(kwargs["messages"][0]["role"], "user")
        self.assertEqual(kwargs["messages"][0]["content"], "Hello world")
        self.assertEqual(kwargs["temperature"], 0.7)
        self.assertEqual(kwargs["max_tokens"], 4096)
        self.assertNotIn("system", kwargs)

    @patch("apicenter.text.providers.anthropic.Anthropic")
    def test_call_anthropic_with_system_message(self, mock_anthropic_class):
        """Test that system messages are handled correctly."""
        # Import inside the test to ensure the mock is applied
        from apicenter.text.providers.anthropic import call_anthropic

        # Setup mock client and response
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client

        mock_messages = MagicMock()
        mock_client.messages = mock_messages

        mock_create = MagicMock()
        mock_messages.create = mock_create

        # Mock return value
        mock_content = MagicMock()
        mock_content.text = "This is a test response"
        mock_create.return_value = MagicMock(content=[mock_content])

        # Call the function with a message list including system prompt
        result = call_anthropic(
            model="claude-3-sonnet-20240229",
            prompt=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": "Hello world"},
            ],
            credentials={"api_key": "test_key"},
            temperature=0.7,
        )

        # Check the result
        self.assertEqual(result, "This is a test response")

        # Get the call arguments
        mock_create.assert_called_once()
        args, kwargs = mock_create.call_args

        # Check that the parameters were correctly passed
        self.assertEqual(kwargs["model"], "claude-3-sonnet-20240229")
        self.assertEqual(len(kwargs["messages"]), 1)
        self.assertEqual(kwargs["messages"][0]["role"], "user")
        self.assertEqual(kwargs["messages"][0]["content"], "Hello world")
        self.assertEqual(kwargs["system"], "You are a helpful assistant")
        self.assertEqual(kwargs["temperature"], 0.7)
        self.assertEqual(kwargs["max_tokens"], 4096)

    @patch("apicenter.text.providers.anthropic.Anthropic")
    def test_call_anthropic_only_system_message(self, mock_anthropic_class):
        """Test that a prompt with only system message gets a default user message."""
        # Import inside the test to ensure the mock is applied
        from apicenter.text.providers.anthropic import call_anthropic

        # Setup mock client and response
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client

        mock_messages = MagicMock()
        mock_client.messages = mock_messages

        mock_create = MagicMock()
        mock_messages.create = mock_create

        # Mock return value
        mock_content = MagicMock()
        mock_content.text = "This is a test response"
        mock_create.return_value = MagicMock(content=[mock_content])

        # Call the function with only a system message
        result = call_anthropic(
            model="claude-3-sonnet-20240229",
            prompt=[{"role": "system", "content": "You are a helpful assistant"}],
            credentials={"api_key": "test_key"},
        )

        # Check the result
        self.assertEqual(result, "This is a test response")

        # Get the call arguments
        mock_create.assert_called_once()
        args, kwargs = mock_create.call_args

        # Check that the parameters were correctly passed
        self.assertEqual(kwargs["model"], "claude-3-sonnet-20240229")
        self.assertEqual(len(kwargs["messages"]), 1)
        self.assertEqual(kwargs["messages"][0]["role"], "user")
        self.assertEqual(kwargs["messages"][0]["content"], "Hello")
        self.assertEqual(kwargs["system"], "You are a helpful assistant")


if __name__ == "__main__":
    unittest.main()
