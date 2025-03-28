from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, TypeVar, Generic
from dataclasses import dataclass
import json
import os
from pathlib import Path

T = TypeVar('T')

@dataclass
class ProviderConfig:
    """Configuration for an AI provider."""
    api_key: str
    organization: Optional[str] = None
    base_url: Optional[str] = None
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
        self.config = self._load_config()
        
    def _load_config(self) -> ProviderConfig:
        """Load provider configuration from credentials file."""
        # First try environment variable
        credentials_path = os.getenv('APICENTER_CREDENTIALS_PATH')
        
        if not credentials_path:
            # If not set, look in several locations
            possible_paths = [
                Path.cwd() / 'credentials.json',  # Current directory
                Path(__file__).parent.parent.parent / 'credentials.json',  # Project root
                Path.home() / '.apicenter' / 'credentials.json'  # User's home directory
            ]
            
            for path in possible_paths:
                if path.exists():
                    credentials_path = path
                    break
            else:
                raise FileNotFoundError(
                    "Credentials file not found. Looked in:\n" +
                    "\n".join(f"- {p}" for p in possible_paths) +
                    "\nPlease create a credentials.json file or set APICENTER_CREDENTIALS_PATH."
                )
        
        try:
            with open(credentials_path, 'r') as f:
                credentials = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Credentials file not found at {credentials_path}. "
                "Please create a credentials.json file or set APICENTER_CREDENTIALS_PATH."
            )
            
        # Get the mode-specific provider config
        mode = self._get_mode()
        provider_config = credentials.get('modes', {}).get(mode, {}).get('providers', {}).get(self.provider, {})
        
        if not provider_config:
            raise ValueError(f"Provider {self.provider} not found in credentials for mode {mode}")
            
        return ProviderConfig(
            api_key=provider_config.get('api_key'),
            organization=provider_config.get('organization'),
            base_url=provider_config.get('base_url'),
            additional_params=provider_config.get('additional_params', {})
        )
    
    @abstractmethod
    def _get_mode(self) -> str:
        """Return the mode this provider handles (text, image, audio)."""
        pass
    
    @abstractmethod
    def validate_params(self) -> None:
        """Validate the provider-specific parameters."""
        pass
    
    @abstractmethod
    def call(self) -> T:
        """Make the actual API call and return the response."""
        pass
    
    def get_response(self) -> T:
        """Validate parameters and make the API call."""
        self.validate_params()
        return self.call() 