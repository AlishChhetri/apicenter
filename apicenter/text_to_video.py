import requests
from config import config  # Import API credentials from config.py


class TextToVideoProvider:
    def __init__(self, provider, model, prompt, **kwargs):
        self.provider = provider.lower()
        self.model = model
        self.prompt = prompt
        self.kwargs = kwargs  # Stores all optional parameters

        # Auto-load credentials (returns {} if none needed)
        self.credentials = config.get_credentials(self.provider)

    def get_response(self):
        """Automatically call the correct video generation API based on provider."""
        api_methods = {
            "stablediffusion": self._call_stablediffusion,
            "creatomate": self._call_creatomate,
        }

        return api_methods.get(
            self.provider, lambda: f"Error: Unsupported provider {self.provider}"
        )()

    def _call_stablediffusion(self):
        """Calls StableDiffusionAPI for text-to-video generation."""
        base_url = self.credentials.get("base_url")
        api_key = self.credentials.get("api_key")

        if not base_url or not api_key:
            return "Error: Missing StableDiffusion API credentials in .env"

        generate_url = f"{base_url}/text2video"
        headers = {
            "Content-Type": "application/json",
        }
        payload = {
            "key": api_key,
            "prompt": self.prompt,
            **self.kwargs,  # Supports optional params (negative_prompt, scheduler, seconds)
        }

        response = requests.post(generate_url, json=payload, headers=headers)
        response_data = response.json()

        # Retrieve video URL from response
        video_urls = response_data.get("output", [])
        return (
            video_urls
            if video_urls
            else f"Error: No video returned. Response: {response_data}"
        )

    def _call_creatomate(self):
        """Calls Creatomate API for video generation."""
        base_url = self.credentials.get("base_url")
        api_key = self.credentials.get("api_key")

        if not base_url or not api_key:
            return "Error: Missing Creatomate API credentials in .env"

        generate_url = f"{base_url}/renders"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "template_id": self.model,  # Template ID required for Creatomate
            "modifications": {
                "Text": self.prompt,
                **self.kwargs,  # Supports optional modifications (e.g., video URL, text edits)
            },
        }

        response = requests.post(generate_url, json=payload, headers=headers)
        response_data = response.json()

        # Retrieve video URL from response
        video_url = response_data.get("url")
        return (
            video_url
            if video_url
            else f"Error: No video returned. Response: {response_data}"
        )


def text_to_video(provider, model, prompt, **kwargs):
    """Universal function to generate videos from text with minimal input."""
    return TextToVideoProvider(provider, model, prompt, **kwargs).get_response()
