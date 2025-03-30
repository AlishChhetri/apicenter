"""Image generation provider implementations for various AI services."""

from apicenter.core.credentials import credentials
from .providers.openai import call_openai
from .providers.stability import call_stability
from typing import Any, Dict, Optional, Union, List
from ..core.base import BaseProvider, ProviderConfig


class ImageProvider(BaseProvider[Union[str, bytes, List[str]]]):
    """Provider for image generation across multiple AI services."""
    
    def get_mode(self) -> str:
        """Return the mode identifier for this provider."""
        return "image"
    
    def call(self) -> Union[str, bytes, List[str]]:
        """Route the request to the appropriate provider implementation."""
        # Map each provider to its implementation method
        provider_methods = {
            "openai": self.call_openai,
            "stability": self.call_stability
        }
        
        try:
            # Call the appropriate provider method if supported
            if self.provider in provider_methods:
                return provider_methods[self.provider]()
            else:
                raise ValueError(f"Unsupported image provider: {self.provider}")
        except Exception as e:
            raise ValueError(f"Error calling {self.provider} image API: {str(e)}")
    
    def call_openai(self) -> Union[str, bytes, List[str]]:
        """Process request through OpenAI's DALL-E image generation API."""
        # Prepare credentials dictionary
        credentials_dict = {
            "api_key": self.config.api_key,
            "organization": self.config.organization
        }
        
        # Remove None values from credentials
        credentials_dict = {k: v for k, v in credentials_dict.items() if v is not None}
        
        # Call the OpenAI implementation
        return call_openai(
            model=self.model,
            prompt=self.prompt,
            credentials=credentials_dict,
            **self.kwargs
        )
    
    def call_stability(self) -> bytes:
        """Process request through Stability AI's image generation API."""
        # Prepare credentials dictionary
        credentials_dict = {
            "api_key": self.config.api_key
        }
        
        # Remove None values from credentials
        credentials_dict = {k: v for k, v in credentials_dict.items() if v is not None}
        
        # Call the Stability AI implementation
        return call_stability(
            model=self.model,
            prompt=self.prompt,
            credentials=credentials_dict,
            **self.kwargs
        )


def image(provider: str, model: str, prompt: str, **kwargs: Any) -> Union[str, bytes, List[str]]:
    """Generate images using any supported AI provider with a unified interface."""
    # Create provider instance and get response
    return ImageProvider(provider, model, prompt, **kwargs).get_response()
