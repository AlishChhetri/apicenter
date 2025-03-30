from apicenter.core.credentials import credentials
from .providers.openai import call_openai
from .providers.stability import call_stability
from typing import Any, Dict, Optional, Union, List
from ..core.base import BaseProvider, ProviderConfig


class ImageProvider(BaseProvider[Union[str, bytes, List[str]]]):
    """Provider for image generation using various AI services."""
    
    def get_mode(self) -> str:
        """Return the mode this provider handles."""
        return "image"
    
    def call(self) -> Union[str, bytes, List[str]]:
        """Make the API call and return the response."""
        # Dictionary mapping providers to their call methods
        provider_methods = {
            "openai": self.call_openai,
            "stability": self.call_stability
        }
        
        try:
            if self.provider in provider_methods:
                return provider_methods[self.provider]()
            else:
                raise ValueError(f"Unsupported image provider: {self.provider}")
        except Exception as e:
            raise ValueError(f"Error calling {self.provider} image API: {str(e)}")
    
    def call_openai(self) -> Union[str, bytes, List[str]]:
        """Call OpenAI's DALL-E API."""
        credentials_dict = {
            "api_key": self.config.api_key,
            "organization": self.config.organization
        }
        
        # Remove None values
        credentials_dict = {k: v for k, v in credentials_dict.items() if v is not None}
        
        return call_openai(
            model=self.model,
            prompt=self.prompt,
            credentials=credentials_dict,
            **self.kwargs
        )
    
    def call_stability(self) -> bytes:
        """Call Stability AI's API."""
        credentials_dict = {
            "api_key": self.config.api_key
        }
        
        # Remove None values
        credentials_dict = {k: v for k, v in credentials_dict.items() if v is not None}
        
        return call_stability(
            model=self.model,
            prompt=self.prompt,
            credentials=credentials_dict,
            **self.kwargs
        )


def image(provider: str, model: str, prompt: str, **kwargs: Any) -> Union[str, bytes, List[str]]:
    """Universal function to generate images from text with minimal input.
    
    Args:
        provider: The AI service provider (e.g., "openai", "stability")
        model: The specific model to use (e.g., "dall-e-3", "stable-diffusion-xl")
        prompt: The text description of the image to generate
        **kwargs: Additional parameters specific to the provider and model
        
    Returns:
        The generated image URL, bytes, or list of URLs depending on the provider and settings
    """
    return ImageProvider(provider, model, prompt, **kwargs).get_response()
