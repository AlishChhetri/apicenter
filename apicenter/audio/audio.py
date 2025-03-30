"""Audio generation provider implementations for various AI services."""

from apicenter.core.credentials import credentials
from .providers.elevenlabs import call_elevenlabs
from typing import Any, Dict, Optional
from ..core.base import BaseProvider, ProviderConfig


class AudioProvider(BaseProvider[bytes]):
    """Provider for text-to-speech conversion across multiple AI services."""
    
    def get_mode(self) -> str:
        """Return the mode identifier for this provider."""
        return "audio"
    
    def call(self) -> bytes:
        """Route the request to the appropriate provider implementation."""
        # Map each provider to its implementation method
        provider_methods = {
            "elevenlabs": self.call_elevenlabs
        }
        
        try:
            # Call the appropriate provider method if supported
            if self.provider in provider_methods:
                return provider_methods[self.provider]()
            else:
                raise ValueError(f"Unsupported audio provider: {self.provider}")
        except Exception as e:
            raise ValueError(f"Error calling {self.provider} audio API: {str(e)}")
    
    def call_elevenlabs(self) -> bytes:
        """Process request through ElevenLabs' text-to-speech API."""
        # Prepare credentials dictionary
        credentials_dict = {
            "api_key": self.config.api_key
        }
        
        # Remove None values from credentials
        credentials_dict = {k: v for k, v in credentials_dict.items() if v is not None}
        
        # Call the ElevenLabs implementation
        return call_elevenlabs(
            model=self.model,
            prompt=self.prompt,
            credentials=credentials_dict,
            **self.kwargs
        )


def audio(provider: str, model: str, prompt: str, **kwargs: Any) -> bytes:
    """Generate audio using any supported AI provider with a unified interface."""
    # Create provider instance and get response
    return AudioProvider(provider, model, prompt, **kwargs).get_response()