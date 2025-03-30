"""Test the Deepseek text provider."""

import unittest
from unittest.mock import patch, MagicMock


class TestDeepseek(unittest.TestCase):
    """Test the Deepseek text provider."""
    
    @patch('apicenter.text.providers.deepseek.OpenAI')
    def test_call_deepseek(self, mock_openai_class):
        """Test that Deepseek API calls are handled correctly."""
        # Import inside the test to ensure the mock is applied
        from apicenter.text.providers.deepseek import call_deepseek
        
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
            {"role": "user", "content": "Hello world"}
        ]
        
        result = call_deepseek(
            model="deepseek-chat",
            prompt=messages,
            credentials={"api_key": "test_key"},
            temperature=0.5
        )
        
        # Check the result
        self.assertEqual(result, "This is a test response")
        
        # Get the call arguments
        mock_create.assert_called_once()
        args, kwargs = mock_create.call_args
        
        # Check that the parameters were correctly passed
        self.assertEqual(kwargs['model'], "deepseek-chat")
        self.assertEqual(kwargs['messages'], messages)
        self.assertEqual(kwargs['temperature'], 0.5)


if __name__ == '__main__':
    unittest.main() 