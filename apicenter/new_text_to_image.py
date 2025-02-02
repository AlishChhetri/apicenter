import requests
from openai import OpenAI
from config import config


class TextToImageProvider:
    def __init__(self, provider, model, prompt, **kwargs):
        self.provider = provider.lower()
        self.model = model
        self.prompt = prompt
        self.kwargs = kwargs  # Stores all optional parameters

        # Auto-load credentials (returns {} if none needed)
        self.credentials = config.get_credentials(self.provider)

    def get_response(self):
        """Automatically call the correct image generation API based on provider."""
        providers = {"openai": self._call_openai, "monster": self._call_monster}

        return providers.get(
            self.provider, lambda: f"Error: Unsupported provider {self.provider}"
        )()

    def _call_openai(self):
        """Calls OpenAI's DALL·E API for image generation."""
        client = OpenAI(**self.credentials)

        response = client.images.generate(
            model=self.model,
            prompt=self.prompt,
            **self.kwargs,  # Pass optional params like size, n, quality
        )
        return [img.url for img in response.data]  # Returns a list of image URLs

    def _call_monster(self):
        """Calls MonsterAPI for text-to-image generation."""
        api_key = self.credentials.get("api_key")
        if not api_key:
            return "Error: Missing MonsterAPI API key in .env"

        generate_url = "https://api.monsterapi.ai/v1/generate/txt2img"
        results_url = "https://api.monsterapi.ai/v1/results"

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "prompt": self.prompt,
            **self.kwargs,  # Only pass optional parameters
        }

        # Make the request
        response = requests.post(generate_url, json=payload, headers=headers)
        response_data = response.json()

        # Retrieve process ID
        process_id = response_data.get("process_id")
        if not process_id:
            return f"Error: No process ID received from MonsterAPI. Response: {response_data}"

        # Get final image results
        response = requests.get(f"{results_url}/{process_id}", headers=headers)
        response_data = response.json()

        images = response_data.get("images", [])
        return (
            images
            if images
            else f"Error: No images returned. Response: {response_data}"
        )


def text_to_image(provider, model, prompt, **kwargs):
    """Universal function to generate images from text with minimal input."""
    return TextToImageProvider(provider, model, prompt, **kwargs).get_response()
