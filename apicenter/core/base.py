from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, TypeVar, Generic, Union
from dataclasses import dataclass
import json
import os
from pathlib import Path
from .credentials import credentials as creds_provider

T = TypeVar('T')

@dataclass
class ProviderConfig:
    """Configuration for an AI provider."""
    api_key: Optional[str] = None
    organization: Optional[str] = None
    additional_params: Optional[Dict[str, Any]] = None

class BaseProvider(ABC, Generic[T]):
    """Base class for all AI providers."""
    
    def __init__(
        self,
        provider: str,
        model: str,
        prompt: str,
        **kwargs: Any
    ):
        self.provider = provider
        self.model = model
        self.prompt = prompt
        self.kwargs = kwargs
        self.config = self.load_config()
        
    def load_config(self) -> ProviderConfig:
        """Load provider configuration from credentials."""
        # Get the mode-specific provider config
        mode = self.get_mode()
        
        try:
            provider_config = creds_provider.get_credentials(mode, self.provider)
            
            # Special case for local providers like Ollama
            if not provider_config and self.provider in ["ollama"]:
                return ProviderConfig()
                
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
        """Make the API call."""
        return self.call() 