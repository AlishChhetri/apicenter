"""Test the Stability AI image provider."""

import unittest
from unittest.mock import patch, MagicMock
import json
import base64


class TestStabilityAI(unittest.TestCase):
    """Test the Stability AI image provider."""

    @patch("apicenter.image.providers.stability.requests.post")
    def test_call_stability_with_parameters(self, mock_post):
        """Test that parameters are handled correctly."""
        # Import inside the test to ensure the mock is applied
        from apicenter.image.providers.stability import call_stability

        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "artifacts": [{"base64": base64.b64encode(b"test_image_data").decode("utf-8")}]
        }
        mock_post.return_value = mock_response

        # Call with parameters
        result = call_stability(
            model="stable-diffusion-xl-1024-v1-0",
            prompt="A beautiful sunset",
            credentials={"api_key": "test_key"},
            height=768,
            width=512,
            steps=40,
            cfg_scale=8.0,
            negative_prompt="ugly, blurry",
        )

        # Check that the API was called correctly
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args

        # Check that the URL is correct for the model
        self.assertEqual(
            args[0],
            "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image",
        )

        # Check that the headers are correct
        self.assertEqual(kwargs["headers"]["Authorization"], "Bearer test_key")

        # Check that the JSON body contains the correct data
        json_data = kwargs["json"]
        self.assertEqual(json_data["text_prompts"][0]["text"], "A beautiful sunset")
        self.assertEqual(json_data["height"], 768)
        self.assertEqual(json_data["width"], 512)
        self.assertEqual(json_data["steps"], 40)
        self.assertEqual(json_data["cfg_scale"], 8.0)

        # Check that negative prompt is handled correctly
        self.assertEqual(json_data["text_prompts"][1]["text"], "ugly, blurry")
        self.assertEqual(json_data["text_prompts"][1]["weight"], -1.0)

        # Check that the returned image data is correct
        self.assertEqual(result, b"test_image_data")


if __name__ == "__main__":
    unittest.main()
