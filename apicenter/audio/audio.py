from apicenter.core.credentials import credentials
from .providers.elevenlabs import call_elevenlabs
from typing import Any, Dict, Optional
from ..core.base import BaseProvider, ProviderConfig


class AudioProvider(BaseProvider[bytes]):
    """Provider for audio generation using various AI services."""
    
    def get_mode(self) -> str:
        """Return the mode this provider handles."""
        return "audio"
    
    def call(self) -> bytes:
        """Make the API call and return the response."""
        # Dictionary mapping providers to their call methods
        provider_methods = {
            "elevenlabs": self.call_elevenlabs
        }
        
        try:
            if self.provider in provider_methods:
                return provider_methods[self.provider]()
            else:
                raise ValueError(f"Unsupported audio provider: {self.provider}")
        except Exception as e:
            raise ValueError(f"Error calling {self.provider} audio API: {str(e)}")
    
    def call_elevenlabs(self) -> bytes:
        """Call ElevenLabs' API."""
        credentials_dict = {
            "api_key": self.config.api_key
        }
        
        # Remove None values
        credentials_dict = {k: v for k, v in credentials_dict.items() if v is not None}
        
        return call_elevenlabs(
            model=self.model,
            prompt=self.prompt,
            credentials=credentials_dict,
            **self.kwargs
        )


def audio(provider: str, model: str, prompt: str, **kwargs: Any) -> bytes:
    """Universal function to generate audio from text with minimal input.
    
    Args:
        provider: The AI service provider (e.g., "elevenlabs")
        model: The specific model to use (e.g., "eleven_multilingual_v2")
        prompt: The text to convert to speech
        **kwargs: Additional parameters specific to the provider and model
        
    Returns:
        The generated audio as bytes
    """
    return AudioProvider(provider, model, prompt, **kwargs).get_response()