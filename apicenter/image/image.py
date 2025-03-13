from apicenter.core.credentials import credentials
from .providers.openai import call_openai
from .providers.stability import call_stability


class ImageProvider:
    def __init__(self, provider, model, prompt, **kwargs):
        self.provider = provider.lower()
        self.model = model
        self.prompt = prompt
        self.kwargs = kwargs
        self.credentials = credentials.get_credentials("image", self.provider)

    def get_response(self):
        """Automatically call the correct image generation API based on provider."""
        providers = {
            "openai": lambda: call_openai(self.model, self.prompt, self.credentials, **self.kwargs),
            "stability": lambda: call_stability(self.model, self.prompt, self.credentials, **self.kwargs),
        }

        return providers.get(
            self.provider, lambda: f"Error: Unsupported provider {self.provider}"
        )()


def image(provider, model, prompt, **kwargs):
    """Universal function to generate images from text with minimal input."""
    return ImageProvider(provider, model, prompt, **kwargs).get_response()
