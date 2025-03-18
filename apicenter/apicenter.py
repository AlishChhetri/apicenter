from .text.text import TextProvider
from .image.image import ImageProvider
from .audio.audio import AudioProvider


class APICenter:
    """Universal class for managing AI API interactions."""

    def text(self, provider, model, prompt, **kwargs):
        """Universal function to call any supported AI model with minimal input."""
        return TextProvider(provider, model, prompt, **kwargs).get_response()

    def image(self, provider, model, prompt, **kwargs):
        """Universal function to generate images from text with minimal input."""
        return ImageProvider(provider, model, prompt, **kwargs).get_response()

    def audio(self, provider, model, prompt, **kwargs):
        """Universal function to generate audio from text with minimal input."""
        return AudioProvider(provider, model, prompt, **kwargs).get_response()


apicenter = APICenter()
