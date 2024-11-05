"""TextToImage class to handle requests for image generation models like OpenAI's DALL-E"""

import openai
from apicenter.config import OPENAI_KEY, OPENAI_ORG


class TextToImage:
    """Handles requests for image generation models"""

    def __init__(self):
        # Initialize the OpenAI client
        self.openai_client = openai.OpenAI(api_key=OPENAI_KEY, organization=OPENAI_ORG)

    def call_openai_dalle(
        self, model, prompt, size="1024x1024", n=1, quality="standard"
    ):
        """Sends a request to OpenAI DALL-E model to generate an image based on text"""
        response = self.openai_client.images.generate(
            model=model, prompt=prompt, size=size, n=n, quality=quality
        )
        return [img.url for img in response.data]
