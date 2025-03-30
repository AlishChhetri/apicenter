"""Test error handling in APICenter."""

import unittest
from unittest.mock import patch, MagicMock


class TestErrorHandling(unittest.TestCase):
    """Test error handling in APICenter."""

    def setUp(self):
        """Set up the test environment."""
        from apicenter import apicenter

        self.apicenter = apicenter

    @patch("apicenter.text.providers.openai.OpenAI")
    def test_openai_error_handling(self, mock_openai_class):
        """Test that OpenAI API errors are properly handled."""
        # Import inside the test to ensure the mock is applied
        from apicenter.text.providers.openai import call_openai

        # Setup mock client to raise an exception
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        mock_chat = MagicMock()
        mock_client.chat = mock_chat

        mock_completions = MagicMock()
        mock_chat.completions = mock_completions

        mock_create = MagicMock()
        mock_completions.create = mock_create

        # Make the API call raise an exception
        mock_create.side_effect = Exception("API rate limit exceeded")

        # Call the function and expect a ValueError with the exception message
        with self.assertRaises(ValueError) as context:
            call_openai(
                model="gpt-4",
                prompt="Hello world",
                credentials={"api_key": "test_key"},
                temperature=0.7,
            )

        # Check that the error message contains the original exception message
        self.assertIn("API rate limit exceeded", str(context.exception))
        self.assertIn("OpenAI API error", str(context.exception))

    @patch("apicenter.text.providers.anthropic.Anthropic")
    def test_anthropic_error_handling(self, mock_anthropic_class):
        """Test that Anthropic API errors are properly handled."""
        # Import inside the test to ensure the mock is applied
        from apicenter.text.providers.anthropic import call_anthropic

        # Setup mock client to raise an exception
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client

        mock_messages = MagicMock()
        mock_client.messages = mock_messages

        mock_create = MagicMock()
        mock_messages.create = mock_create

        # Make the API call raise an exception
        mock_create.side_effect = Exception("Invalid API key")

        # Call the function and expect a ValueError with the exception message
        with self.assertRaises(ValueError) as context:
            call_anthropic(
                model="claude-3-sonnet-20240229",
                prompt="Hello world",
                credentials={"api_key": "invalid_key"},
                temperature=0.7,
            )

        # Check that the error message contains the original exception message
        self.assertIn("Invalid API key", str(context.exception))
        self.assertIn("Anthropic API error", str(context.exception))

    @patch("ollama.chat")
    def test_ollama_error_handling(self, mock_chat):
        """Test that Ollama errors are properly handled."""
        # Import inside the test to ensure the mock is applied
        from apicenter.text.providers.ollama import call_ollama

        # Make the API call raise an exception
        mock_chat.side_effect = Exception("Model not found")

        # Call the function and expect a ValueError with the exception message
        with self.assertRaises(ValueError) as context:
            call_ollama(model="nonexistent-model", prompt="Hello world", temperature=0.7)

        # Check that the error message contains the original exception message
        self.assertIn("Model not found", str(context.exception))
        self.assertIn("Ollama API error", str(context.exception))

    @patch("requests.post")
    def test_stability_error_handling(self, mock_post):
        """Test that Stability AI API errors are properly handled."""
        # Import inside the test to ensure the mock is applied
        from apicenter.image.providers.stability import call_stability

        # Mock a failed response
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {"message": "Invalid API key"}
        mock_response.text = "Error: Authentication failed"
        mock_post.return_value = mock_response

        # Call the function and expect a ValueError with the exception message
        with self.assertRaises(ValueError) as context:
            call_stability(
                model="stable-diffusion-xl-1024-v1-0",
                prompt="A beautiful sunset",
                credentials={"api_key": "invalid_key"},
                height=1024,
                width=1024,
            )

        # Check that the error message contains the original exception message
        self.assertIn("Invalid API key", str(context.exception))
        self.assertIn("Stability AI API error", str(context.exception))

    @patch("apicenter.audio.providers.elevenlabs.ElevenLabs")
    def test_elevenlabs_error_handling(self, mock_elevenlabs_class):
        """Test that ElevenLabs API errors are properly handled."""
        # Import inside the test to ensure the mock is applied
        from apicenter.audio.providers.elevenlabs import call_elevenlabs

        # Setup mock client to raise an exception
        mock_client = MagicMock()
        mock_elevenlabs_class.return_value = mock_client

        mock_tts = MagicMock()
        mock_client.text_to_speech = mock_tts

        mock_convert = MagicMock()
        mock_tts.convert = mock_convert

        # Make the API call raise an exception
        mock_convert.side_effect = Exception("Invalid voice ID")

        # Call the function and expect a ValueError with the exception message
        with self.assertRaises(ValueError) as context:
            call_elevenlabs(
                model="eleven_multilingual_v2",
                prompt="Hello world",
                credentials={"api_key": "test_key"},
                voice_id="invalid_voice_id",
            )

        # Check that the error message contains the original exception message
        self.assertIn("Invalid voice ID", str(context.exception))
        self.assertIn("ElevenLabs audio generation error", str(context.exception))


if __name__ == "__main__":
    unittest.main()
