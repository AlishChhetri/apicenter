from typing import Any, Dict, Optional, Union, List
from .text.text import TextProvider
from .image.image import ImageProvider
from .audio.audio import AudioProvider
from .core.base import BaseProvider


class APICenter:
    """Universal class for managing AI API interactions."""

    def __init__(self):
        """Initialize the APICenter with supported providers for each mode."""
        self.providers: Dict[str, Dict[str, type[BaseProvider]]] = {
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
            }
        }

    def get_provider_class(self, mode: str, provider: str) -> type[BaseProvider]:
        """Get the appropriate provider class for the given mode and provider.
        
        Args:
            mode: The operation mode (text, image, audio)
            provider: The provider name
            
        Returns:
            The provider class to use
            
        Raises:
            ValueError: If the mode or provider is not supported
        """
        if mode not in self.providers:
            raise ValueError(f"Unsupported mode: {mode}")
        if provider not in self.providers[mode]:
            raise ValueError(f"Unsupported provider '{provider}' for mode '{mode}'")
        return self.providers[mode][provider]

    def text(
        self,
        provider: str,
        model: str,
        prompt: Union[str, List[Dict[str, str]]],
        **kwargs: Any
    ) -> str:
        """Generate text using the specified AI model.
        
        Args:
            provider: The AI service provider (e.g., "openai", "anthropic", "ollama")
            model: The specific model to use (e.g., "gpt-4", "claude-3-sonnet-20240229", "deepseek-r1")
            prompt: The input text or message list for the AI operation
            **kwargs: Any additional parameters specific to the provider and model
            
        Returns:
            The generated text response
            
        Raises:
            ValueError: If the provider or mode is not supported
        """
        provider_class = self.get_provider_class("text", provider)
        return provider_class(provider, model, prompt, **kwargs).get_response()

    def image(
        self,
        provider: str,
        model: str,
        prompt: str,
        **kwargs: Any
    ) -> Union[str, bytes, List[str]]:
        """Generate an image using the specified AI model.
        
        Args:
            provider: The AI service provider (e.g., "openai", "stability")
            model: The specific model to use (e.g., "dall-e-3", "stable-diffusion-xl")
            prompt: The text description of the image to generate
            **kwargs: Any additional parameters specific to the provider and model
            
        Returns:
            The generated image (URL or bytes depending on provider)
            
        Raises:
            ValueError: If the provider or mode is not supported
        """
        provider_class = self.get_provider_class("image", provider)
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
            prompt: The text to convert to speech
            **kwargs: Any additional parameters specific to the provider and model
            
        Returns:
            The generated audio as bytes
            
        Raises:
            ValueError: If the provider or mode is not supported
        """
        provider_class = self.get_provider_class("audio", provider)
        return provider_class(provider, model, prompt, **kwargs).get_response()


# Singleton instance for easy import and use
apicenter = APICenter()
