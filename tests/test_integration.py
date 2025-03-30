"""Integration tests for APICenter."""

import unittest
from unittest.mock import patch, MagicMock
import json
import io


class TestAPIIntegration(unittest.TestCase):
    """Integration tests for APICenter."""

    def setUp(self):
        """Set up the test environment."""
        from apicenter import apicenter

        self.apicenter = apicenter

    @patch("apicenter.text.providers.openai.OpenAI")
    def test_text_integration_openai(self, mock_openai_class):
        """Test the full text generation flow with OpenAI."""
        # Setup mock OpenAI client
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        mock_chat = MagicMock()
        mock_client.chat = mock_chat

        mock_completions = MagicMock()
        mock_chat.completions = mock_completions

        mock_create = MagicMock()
        mock_completions.create = mock_create

        # Mock response
        mock_message = MagicMock()
        mock_message.content = "This is a test response from OpenAI"

        mock_choice = MagicMock()
        mock_choice.message = mock_message

        mock_response = MagicMock()
        mock_response.choices = [mock_choice]

        mock_create.return_value = mock_response

        # Mock the credentials system
        with patch("apicenter.core.credentials.CredentialsProvider.get_credentials") as mock_get:
            mock_get.return_value = {"api_key": "test-key", "organization": "test-org"}

            # Call the text method
            result = self.apicenter.text(
                provider="openai", model="gpt-4", prompt="Test prompt", temperature=0.7
            )

            # Check the result
            self.assertEqual(result, "This is a test response from OpenAI")

            # Verify that the credentials were retrieved
            mock_get.assert_called_once_with("text", "openai")

            # Verify that the OpenAI client was created correctly
            mock_openai_class.assert_called_once_with(api_key="test-key", organization="test-org")

            # Verify that the completion was called with the right parameters
            mock_create.assert_called_once()
            args, kwargs = mock_create.call_args
            self.assertEqual(kwargs["model"], "gpt-4")
            self.assertEqual(len(kwargs["messages"]), 1)
            self.assertEqual(kwargs["messages"][0]["role"], "user")
            self.assertEqual(kwargs["messages"][0]["content"], "Test prompt")
            self.assertEqual(kwargs["temperature"], 0.7)

    @patch("apicenter.image.providers.stability.requests.post")
    def test_image_integration_stability(self, mock_post):
        """Test the full image generation flow with Stability AI."""
        # Mock the requests response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "artifacts": [
                {
                    "base64": "VGVzdEltYWdlRGF0YQ=="  # "TestImageData" in base64
                }
            ]
        }
        mock_post.return_value = mock_response

        # Mock the credentials system
        with patch("apicenter.core.credentials.CredentialsProvider.get_credentials") as mock_get:
            mock_get.return_value = {"api_key": "test-key"}

            # Call the image method
            result = self.apicenter.image(
                provider="stability",
                model="stable-diffusion-xl-1024-v1-0",
                prompt="A beautiful sunset",
                height=1024,
                width=1024,
                negative_prompt="ugly, blurry",
            )

            # Check the result (should be decoded from base64)
            self.assertEqual(result, b"TestImageData")

            # Verify that the credentials were retrieved
            mock_get.assert_called_once_with("image", "stability")

            # Verify that the post was called with the right parameters
            mock_post.assert_called_once()
            args, kwargs = mock_post.call_args
            self.assertEqual(
                args[0],
                "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image",
            )
            self.assertEqual(kwargs["headers"]["Authorization"], "Bearer test-key")
            self.assertEqual(kwargs["json"]["text_prompts"][0]["text"], "A beautiful sunset")
            self.assertEqual(kwargs["json"]["height"], 1024)
            self.assertEqual(kwargs["json"]["width"], 1024)

            # Check that negative prompt is handled correctly
            self.assertEqual(kwargs["json"]["text_prompts"][1]["text"], "ugly, blurry")
            self.assertEqual(kwargs["json"]["text_prompts"][1]["weight"], -1.0)

    @patch("apicenter.audio.providers.elevenlabs.ElevenLabs")
    def test_audio_integration_elevenlabs(self, mock_elevenlabs_class):
        """Test the full audio generation flow with ElevenLabs."""
        # Setup mock ElevenLabs client
        mock_client = MagicMock()
        mock_elevenlabs_class.return_value = mock_client

        mock_tts = MagicMock()
        mock_client.text_to_speech = mock_tts

        mock_convert = MagicMock()
        mock_tts.convert = mock_convert

        # Mock return value (list of audio chunks)
        mock_convert.return_value = [b"chunk1", b"chunk2"]

        # Mock the credentials system
        with patch("apicenter.core.credentials.CredentialsProvider.get_credentials") as mock_get:
            mock_get.return_value = {"api_key": "test-key"}

            # Call the audio method
            result = self.apicenter.audio(
                provider="elevenlabs",
                model="eleven_multilingual_v2",
                prompt="Hello world",
                voice_id="test_voice",
                stability=0.5,
                similarity_boost=0.8,
            )

            # Check the result
            self.assertEqual(result, b"chunk1chunk2")

            # Verify that the credentials were retrieved
            mock_get.assert_called_once_with("audio", "elevenlabs")

            # Verify that the ElevenLabs client was created correctly
            mock_elevenlabs_class.assert_called_once_with(api_key="test-key")

            # Verify that the convert method was called with the right parameters
            mock_convert.assert_called_once()
            args, kwargs = mock_convert.call_args
            self.assertEqual(kwargs["text"], "Hello world")
            self.assertEqual(kwargs["model_id"], "eleven_multilingual_v2")
            self.assertEqual(kwargs["voice_id"], "test_voice")

            # Check that voice settings are created correctly
            self.assertIn("voice_settings", kwargs)
            self.assertEqual(kwargs["voice_settings"].stability, 0.5)
            self.assertEqual(kwargs["voice_settings"].similarity_boost, 0.8)


if __name__ == "__main__":
    unittest.main()
