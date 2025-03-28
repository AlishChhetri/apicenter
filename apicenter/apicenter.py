from typing import Any, Dict, Optional, Union
from .text.text import TextProvider
from .image.image import ImageProvider
from .audio.audio import AudioProvider
from .core.base import BaseProvider


class APICenter:
    """Universal class for managing AI API interactions."""

    def __init__(self):
        self._providers: Dict[str, Dict[str, type[BaseProvider]]] = {
            "text": {
                "openai": TextProvider,
                "anthropic": TextProvider,
            },
            "image": {
                "openai": ImageProvider,
                "stability": ImageProvider,
            },
            "audio": {
                "elevenlabs": AudioProvider,
            }
        }

    def _get_provider_class(self, mode: str, provider: str) -> type[BaseProvider]:
        """Get the appropriate provider class for the given mode and provider."""
        if mode not in self._providers:
            raise ValueError(f"Unsupported mode: {mode}")
        if provider not in self._providers[mode]:
            raise ValueError(f"Unsupported provider '{provider}' for mode '{mode}'")
        return self._providers[mode][provider]

    def text(
        self,
        provider: str,
        model: str,
        prompt: str,
        **kwargs: Any
    ) -> str:
        """Generate text using the specified AI model.
        
        Args:
            provider: The AI service provider (e.g., "openai", "anthropic")
            model: The specific model to use (e.g., "gpt-4", "claude-3-sonnet-20240229")
            prompt: The input text for the AI operation
            **kwargs: Additional parameters specific to the provider and model
            
        Returns:
            The generated text response
        """
        provider_class = self._get_provider_class("text", provider)
        return provider_class(provider, model, prompt, **kwargs).get_response()

    def image(
        self,
        provider: str,
        model: str,
        prompt: str,
        **kwargs: Any
    ) -> Union[str, bytes]:
        """Generate an image using the specified AI model.
        
        Args:
            provider: The AI service provider (e.g., "openai", "stability")
            model: The specific model to use (e.g., "dall-e-3", "stable-diffusion-xl")
            prompt: The input text for the AI operation
            **kwargs: Additional parameters specific to the provider and model
            
        Returns:
            The generated image (URL or bytes depending on provider)
        """
        provider_class = self._get_provider_class("image", provider)
        return provider_class(provider, model, prompt, **kwargs).get_response()

    def audio(
        self,
        provider: str,
        model: str,
        prompt: str,
        **kwargs: Any
    ) -> bytes:
        """Generate audio using the specified AI model.
        
        Args:
            provider: The AI service provider (e.g., "elevenlabs")
            model: The specific model to use (e.g., "eleven_multilingual_v2")
            prompt: The input text for the AI operation
            **kwargs: Additional parameters specific to the provider and model
            
        Returns:
            The generated audio as bytes
        """
        provider_class = self._get_provider_class("audio", provider)
        return provider_class(provider, model, prompt, **kwargs).get_response()


apicenter = APICenter()
