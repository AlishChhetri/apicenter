"""Test the ElevenLabs audio provider."""

import unittest
from unittest.mock import patch, MagicMock
import sys
from elevenlabs.types import VoiceSettings


class TestElevenLabs(unittest.TestCase):
    """Test the ElevenLabs audio provider."""

    @patch("apicenter.audio.providers.elevenlabs.ElevenLabs")
    def test_call_elevenlabs_with_voice_settings(self, mock_elevenlabs_class):
        """Test that voice settings parameters are handled correctly."""
        # Import inside the test to ensure the mock is applied
        from apicenter.audio.providers.elevenlabs import call_elevenlabs

        # Setup mock client and response
        mock_client = MagicMock()
        mock_elevenlabs_class.return_value = mock_client

        mock_convert = MagicMock()
        mock_client.text_to_speech.convert = mock_convert

        # Mock return value (list of bytes chunks)
        mock_convert.return_value = [b"audio", b"data"]

        # Call the function
        result = call_elevenlabs(
            model="eleven_multilingual_v2",
            prompt="Hello world",
            credentials={"api_key": "test_key"},
            voice_id="test_voice",
            stability=0.5,
            similarity_boost=0.8,
            output_format="mp3_44100_128",
        )

        # Check the result
        self.assertEqual(result, b"audiodata")

        # Get the call arguments
        mock_convert.assert_called_once()
        args, kwargs = mock_convert.call_args

        # Check that the parameters were correctly passed
        self.assertEqual(kwargs["text"], "Hello world")
        self.assertEqual(kwargs["model_id"], "eleven_multilingual_v2")
        self.assertEqual(kwargs["voice_id"], "test_voice")
        self.assertEqual(kwargs["output_format"], "mp3_44100_128")

        # Check voice settings
        voice_settings = kwargs.get("voice_settings")
        self.assertIsNotNone(voice_settings)
        self.assertIsInstance(voice_settings, VoiceSettings)
        self.assertEqual(voice_settings.stability, 0.5)
        self.assertEqual(voice_settings.similarity_boost, 0.8)


if __name__ == "__main__":
    unittest.main()
