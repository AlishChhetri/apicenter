from apicenter.core.credentials import credentials
from .providers.elevenlabs import call_elevenlabs
from .providers.google import call_google


class AudioProvider:
    def __init__(self, provider, model, prompt, **kwargs):
        self.provider = provider.lower()
        self.model = model
        self.prompt = prompt
        self.kwargs = kwargs
        self.credentials = credentials.get_credentials("audio", self.provider)

    def get_response(self):
        """Automatically call the correct audio generation API based on provider."""
        providers = {
            "elevenlabs": lambda: call_elevenlabs(self.model, self.prompt, self.credentials, **self.kwargs),
            "google": lambda: call_google(self.model, self.prompt, self.credentials, **self.kwargs),
        }

        return providers.get(
            self.provider, lambda: f"Error: Unsupported provider {self.provider}"
        )()


def audio(provider, model, prompt, **kwargs):
    """Universal function to generate audio from text with minimal input."""
    return AudioProvider(provider, model, prompt, **kwargs).get_response()