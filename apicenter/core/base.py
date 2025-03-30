"""Base classes and interfaces for provider implementations."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, TypeVar, Generic, Union, List
from dataclasses import dataclass
import json
import os
from pathlib import Path
from .credentials import credentials as creds_provider

# Generic type for provider responses
T = TypeVar('T')

@dataclass
class ProviderConfig:
    """Configuration settings for an AI provider."""
    api_key: Optional[str] = None
    organization: Optional[str] = None
    additional_params: Optional[Dict[str, Any]] = None

class BaseProvider(ABC, Generic[T]):
    """Base abstract class for all AI service providers."""
    
    def __init__(
        self,
        provider: str,
        model: str,
        prompt: Union[str, List[Dict[str, str]]],
        **kwargs: Any
    ) -> None:
        """Initialize a provider with model, prompt and additional parameters."""
        self.provider = provider
        self.model = model
        self.prompt = prompt
        self.kwargs = kwargs
        self.config = self.load_config()
        
    def load_config(self) -> ProviderConfig:
        """Load provider configuration from credentials system."""
        # Get the mode for this provider
        mode = self.get_mode()
        
        try:
            # Fetch credentials for this provider
            provider_config = creds_provider.get_credentials(mode, self.provider)
            
            # Handle local providers that don't need credentials
            if not provider_config and self.provider in ["ollama"]:
                return ProviderConfig()
                
            # Create provider configuration with available settings
            return ProviderConfig(
                api_key=provider_config.get('api_key'),
                organization=provider_config.get('organization'),
                additional_params=provider_config.get('additional_params', {})
            )
        except ValueError as e:
            # Provide a more helpful error message
            raise ValueError(
                f"Error loading credentials for {self.provider} in {mode} mode: {str(e)}\n"
                f"Please make sure your credentials.json includes the necessary configuration.\n"
                f"For local providers like 'ollama', no credentials are needed."
            ) from e
    
    @abstractmethod
    def get_mode(self) -> str:
        """Return the mode this provider handles (text, image, audio)."""
        pass
    
    @abstractmethod
    def call(self) -> T:
        """Make the actual API call and return the response."""
        pass
    
    def get_response(self) -> T:
        """Process the request and return the provider response."""
        return self.call() 