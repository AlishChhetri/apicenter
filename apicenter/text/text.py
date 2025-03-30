from apicenter.core.credentials import credentials
from .providers.openai import call_openai
from .providers.anthropic import call_anthropic
from .providers.ollama import call_ollama
from .providers.deepseek import call_deepseek
from typing import Any, Dict, Optional, Union, List, Callable
import openai
from anthropic import Anthropic
import ollama
from ..core.base import BaseProvider, ProviderConfig


class TextProvider(BaseProvider[str]):
    """Provider for text generation using various AI services."""
    
    def get_mode(self) -> str:
        """Return the mode this provider handles."""
        return "text"
    
    def call(self) -> str:
        """Make the API call and return the response."""
        # Dictionary mapping providers to their call methods
        provider_methods = {
            "openai": self.call_openai,
            "anthropic": self.call_anthropic,
            "ollama": self.call_ollama
        }
        
        try:
            if self.provider in provider_methods:
                return provider_methods[self.provider]()
            else:
                raise ValueError(f"Unsupported text provider: {self.provider}")
        except Exception as e:
            raise ValueError(f"Error calling {self.provider} API: {str(e)}")
    
    def call_openai(self) -> str:
        """Call OpenAI's API."""
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
    
    def call_anthropic(self) -> str:
        """Call Anthropic's API."""
        credentials_dict = {
            "api_key": self.config.api_key
        }
        
        return call_anthropic(
            model=self.model,
            prompt=self.prompt,
            credentials=credentials_dict,
            **self.kwargs
        )
        
    def call_ollama(self) -> str:
        """Call Ollama's API (local model)."""
        # Ollama doesn't need any API credentials as it runs locally
        return call_ollama(
            model=self.model,
            prompt=self.prompt,
            **self.kwargs
        )


def text(provider: str, model: str, prompt: Union[str, List[Dict[str, str]]], **kwargs: Any) -> str:
    """Universal function to call any supported AI model with minimal input.
    
    Args:
        provider: The AI service provider (e.g., "openai", "anthropic", "ollama")
        model: The specific model to use
        prompt: The input text for the AI operation (string or message list)
        **kwargs: Additional parameters specific to the provider and model
        
    Returns:
        The generated text response
    """
    return TextProvider(provider, model, prompt, **kwargs).get_response()
