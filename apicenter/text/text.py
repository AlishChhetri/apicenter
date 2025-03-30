"""Text generation provider implementations for various AI services."""

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
    """Provider for text generation across multiple AI services."""

    def get_mode(self) -> str:
        """Return the mode identifier for this provider."""
        return "text"

    def call(self) -> str:
        """Route the request to the appropriate provider implementation."""
        # Map each provider to its implementation method
        provider_methods = {
            "openai": self.call_openai,
            "anthropic": self.call_anthropic,
            "ollama": self.call_ollama,
        }

        try:
            # Call the appropriate provider method if supported
            if self.provider in provider_methods:
                return provider_methods[self.provider]()
            else:
                raise ValueError(f"Unsupported text provider: {self.provider}")
        except Exception as e:
            raise ValueError(f"Error calling {self.provider} API: {str(e)}")

    def call_openai(self) -> str:
        """Process request through OpenAI's text generation API."""
        # Prepare credentials dictionary
        credentials_dict = {
            "api_key": self.config.api_key,
            "organization": self.config.organization,
        }

        # Remove None values from credentials
        credentials_dict = {k: v for k, v in credentials_dict.items() if v is not None}

        # Call the OpenAI implementation
        return call_openai(
            model=self.model, prompt=self.prompt, credentials=credentials_dict, **self.kwargs
        )

    def call_anthropic(self) -> str:
        """Process request through Anthropic's text generation API."""
        # Prepare credentials dictionary
        credentials_dict = {"api_key": self.config.api_key}

        # Call the Anthropic implementation
        return call_anthropic(
            model=self.model, prompt=self.prompt, credentials=credentials_dict, **self.kwargs
        )

    def call_ollama(self) -> str:
        """Process request through local Ollama text generation."""
        # Call the Ollama implementation (no credentials needed)
        return call_ollama(model=self.model, prompt=self.prompt, **self.kwargs)


def text(provider: str, model: str, prompt: Any, **kwargs: Any) -> str:
    """Generate text using any supported AI provider with a unified interface."""
    # Create provider instance and get response
    return TextProvider(provider, model, prompt, **kwargs).get_response()
