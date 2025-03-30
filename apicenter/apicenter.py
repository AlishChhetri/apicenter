"""Universal interface for interacting with various AI APIs."""

from typing import Any, Dict, Optional, Union, List, Type
from .text.text import TextProvider
from .image.image import ImageProvider
from .audio.audio import AudioProvider
from .core.base import BaseProvider


class APICenter:
    """Universal class for managing AI API interactions."""

    def __init__(self) -> None:
        """Initialize the APICenter with available providers for each mode."""
        # Dictionary of supported providers for each mode
        self.providers: Dict[str, Dict[str, Type[BaseProvider]]] = {
            "text": {
                "openai": TextProvider,
                "anthropic": TextProvider,
                "ollama": TextProvider,
            },
            "image": {
                "openai": ImageProvider,
                "stability": ImageProvider,
            },
            "audio": {
                "elevenlabs": AudioProvider,
            },
        }

    def get_provider_class(self, mode: str, provider: str) -> Type[BaseProvider]:
        """Retrieve the appropriate provider class for the given mode and provider."""
        # Check if mode is supported
        if mode not in self.providers:
            raise ValueError(f"Unsupported mode: {mode}")

        # Check if provider is supported for this mode
        if provider not in self.providers[mode]:
            raise ValueError(f"Unsupported provider '{provider}' for mode '{mode}'")

        return self.providers[mode][provider]

    def text(self, provider: str, model: str, prompt: Any, **kwargs: Any) -> str:
        """Generate text using the specified AI provider and model."""
        # Get provider class and create instance with parameters
        provider_class = self.get_provider_class("text", provider)
        return provider_class(provider, model, prompt, **kwargs).get_response()

    def image(
        self, provider: str, model: str, prompt: Any, **kwargs: Any
    ) -> Union[str, bytes, List[str]]:
        """Generate an image using the specified AI provider and model."""
        # Get provider class and create instance with parameters
        provider_class = self.get_provider_class("image", provider)
        return provider_class(provider, model, prompt, **kwargs).get_response()

    def audio(self, provider: str, model: str, prompt: Any, **kwargs: Any) -> bytes:
        """Generate audio using the specified AI provider and model."""
        # Get provider class and create instance with parameters
        provider_class = self.get_provider_class("audio", provider)
        return provider_class(provider, model, prompt, **kwargs).get_response()


# Singleton instance for easy import and use
apicenter = APICenter()
