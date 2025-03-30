"""Test the OpenAI image provider."""

import unittest
from unittest.mock import patch, MagicMock
import base64


class TestOpenAIImage(unittest.TestCase):
    """Test the OpenAI image provider."""
    
    @patch('apicenter.image.providers.openai.OpenAI')
    def test_call_openai_with_url_output(self, mock_openai_class):
        """Test that URL output is handled correctly."""
        # Import inside the test to ensure the mock is applied
        from apicenter.image.providers.openai import call_openai
        
        # Setup mock client and response
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        mock_images = MagicMock()
        mock_client.images = mock_images
        
        mock_generate = MagicMock()
        mock_images.generate = mock_generate
        
        # Create a mock image object with a URL
        mock_image = MagicMock()
        mock_image.url = "https://example.com/test_image.png"
        
        # Mock response
        mock_response = MagicMock()
        mock_response.data = [mock_image]
        
        mock_generate.return_value = mock_response
        
        # Call the function for URL output (default)
        result = call_openai(
            model="dall-e-3",
            prompt="A beautiful sunset",
            credentials={"api_key": "test_key"},
            size="1024x1024",
            quality="hd",
            style="vivid"
        )
        
        # Check the result
        self.assertEqual(result, ["https://example.com/test_image.png"])
        
        # Get the call arguments
        mock_generate.assert_called_once()
        args, kwargs = mock_generate.call_args
        
        # Check that the parameters were correctly passed
        self.assertEqual(kwargs['model'], "dall-e-3")
        self.assertEqual(kwargs['prompt'], "A beautiful sunset")
        self.assertEqual(kwargs['response_format'], "url")
        self.assertEqual(kwargs['size'], "1024x1024")
        self.assertEqual(kwargs['quality'], "hd")
        self.assertEqual(kwargs['style'], "vivid")
        
    @patch('apicenter.image.providers.openai.OpenAI')
    def test_call_openai_with_binary_output(self, mock_openai_class):
        """Test that binary output is handled correctly."""
        # Import inside the test to ensure the mock is applied
        from apicenter.image.providers.openai import call_openai
        
        # Setup mock client and response
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        mock_images = MagicMock()
        mock_client.images = mock_images
        
        mock_generate = MagicMock()
        mock_images.generate = mock_generate
        
        # Create image data and encode it
        test_image_data = b"test_image_data"
        encoded_data = base64.b64encode(test_image_data).decode('utf-8')
        
        # Create a mock image object with base64 data
        mock_image = MagicMock()
        mock_image.b64_json = encoded_data
        
        # Mock response
        mock_response = MagicMock()
        mock_response.data = [mock_image]
        
        mock_generate.return_value = mock_response
        
        # Call the function for binary output
        result = call_openai(
            model="dall-e-3",
            prompt="A beautiful sunset",
            credentials={"api_key": "test_key"},
            size="1024x1024",
            output_format="png"
        )
        
        # Check the result
        self.assertEqual(result, test_image_data)
        
        # Get the call arguments
        mock_generate.assert_called_once()
        args, kwargs = mock_generate.call_args
        
        # Check that the parameters were correctly passed
        self.assertEqual(kwargs['model'], "dall-e-3")
        self.assertEqual(kwargs['prompt'], "A beautiful sunset")
        self.assertEqual(kwargs['response_format'], "b64_json")
        self.assertEqual(kwargs['size'], "1024x1024")


if __name__ == '__main__':
    unittest.main() 