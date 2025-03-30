"""Test the APICenter main class."""

import unittest
from unittest.mock import patch, MagicMock
import sys


class TestAPICenter(unittest.TestCase):
    """Test the APICenter main class."""
    
    def setUp(self):
        """Set up the test environment."""
        # Import inside the test to ensure mocks are applied
        from apicenter import apicenter
        self.apicenter = apicenter
        
    def test_get_provider_class(self):
        """Test the get_provider_class method."""
        # Test valid provider
        from apicenter.text.text import TextProvider
        provider_class = self.apicenter.get_provider_class("text", "openai")
        self.assertEqual(provider_class, TextProvider)
        
        # Test invalid mode
        with self.assertRaises(ValueError) as context:
            self.apicenter.get_provider_class("invalid_mode", "openai")
        self.assertTrue("Unsupported mode" in str(context.exception))
        
        # Test invalid provider
        with self.assertRaises(ValueError) as context:
            self.apicenter.get_provider_class("text", "invalid_provider")
        self.assertTrue("Unsupported provider" in str(context.exception))
        
    @patch('apicenter.text.text.TextProvider.get_response')
    def test_text_method(self, mock_get_response):
        """Test the text method."""
        # Setup mock response
        mock_get_response.return_value = "This is a test response"
        
        # Call the text method
        result = self.apicenter.text(
            provider="openai",
            model="gpt-4",
            prompt="Hello world",
            temperature=0.7
        )
        
        # Check the result
        self.assertEqual(result, "This is a test response")
        
        # Check that get_response was called once
        mock_get_response.assert_called_once()
        
    @patch('apicenter.image.image.ImageProvider.get_response')
    def test_image_method(self, mock_get_response):
        """Test the image method."""
        # Setup mock response
        mock_get_response.return_value = "https://example.com/test_image.png"
        
        # Call the image method
        result = self.apicenter.image(
            provider="openai",
            model="dall-e-3",
            prompt="A beautiful sunset",
            size="1024x1024"
        )
        
        # Check the result
        self.assertEqual(result, "https://example.com/test_image.png")
        
        # Check that get_response was called once
        mock_get_response.assert_called_once()
        
    @patch('apicenter.audio.audio.AudioProvider.get_response')
    def test_audio_method(self, mock_get_response):
        """Test the audio method."""
        # Setup mock response
        mock_get_response.return_value = b"test_audio_data"
        
        # Call the audio method
        result = self.apicenter.audio(
            provider="elevenlabs",
            model="eleven_multilingual_v2",
            prompt="Hello world",
            voice_id="test_voice"
        )
        
        # Check the result
        self.assertEqual(result, b"test_audio_data")
        
        # Check that get_response was called once
        mock_get_response.assert_called_once()


if __name__ == '__main__':
    unittest.main() 