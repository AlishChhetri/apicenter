"""TextToImage class to handle requests for image generation models like OpenAI's DALL-E"""

import openai
from apicenter.config import OPENAI_KEY


class TextToImage:
    """Handles requests for image generation models"""

    def __init__(self):
        # Initialize the OpenAI API key
        openai.api_key = OPENAI_KEY

    def call_openai_dalle(
        self, model, prompt, size="1024x1024", n=1, quality="standard"
    ):
        """Sends a request to OpenAI DALL-E model to generate an image based on text"""

        # Sends a request to the OpenAI image generation API
        response = openai.images.generate(model=model, prompt=prompt, size=size, n=n)

        # Extract and return the URL(s) of the generated image(s)
        image_urls = [img.url for img in response.data]
        return image_urls
