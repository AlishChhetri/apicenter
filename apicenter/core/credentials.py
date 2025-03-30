import json
import os
from pathlib import Path
from typing import Dict, Any, Optional


class CredentialsProvider:
    """Provider for loading and managing API credentials."""
    
    def __init__(self):
        """Load and parse API credentials from JSON file."""
        self.credentials_path = self.find_credentials_file()
        self.credentials = self.load_credentials()

    def find_credentials_file(self) -> Path:
        """Find the credentials file in standard locations.
        
        Returns:
            Path to the credentials file
        """
        # First try environment variable
        env_path = os.getenv('APICENTER_CREDENTIALS_PATH')
        if env_path:
            return Path(env_path)
            
        # Check standard locations
        possible_paths = [
            Path.cwd() / 'credentials.json',  # Current directory
            Path(__file__).parent.parent.parent / 'credentials.json',  # Project root
            Path.home() / '.apicenter' / 'credentials.json',  # User's home directory
            Path.home() / '.config' / 'apicenter' / 'credentials.json',  # XDG config dir
        ]
        
        for path in possible_paths:
            if path.exists():
                return path
                
        # Default to project root if not found (will be created if needed)
        return Path(__file__).parent.parent.parent / 'credentials.json'

    def load_credentials(self) -> Dict[str, Any]:
        """Load credentials from JSON file.
        
        Returns:
            Dictionary containing the credentials
            
        Raises:
            ValueError: If the credentials file is not a valid JSON file
        """
        try:
            with open(self.credentials_path) as f:
                return json.load(f)
        except FileNotFoundError:
            # Return minimal structure for local-only usage
            return {
                "modes": {
                    "text": {"providers": {}},
                    "image": {"providers": {}},
                    "audio": {"providers": {}}
                }
            }
        except json.JSONDecodeError:
            raise ValueError(
                f"Credentials file at {self.credentials_path} is not a valid JSON file."
            )

    def get_credentials(self, mode: str, provider: str) -> Dict[str, Any]:
        """Get credentials for a specific mode and provider.
        
        Args:
            mode: The operation mode (text, image, audio)
            provider: The provider name
            
        Returns:
            Dictionary containing the credentials for the provider
            
        Raises:
            ValueError: If no credentials are found for the provider in the specified mode
        """
        # Special handling for local providers that don't need API keys
        if provider in ["ollama"]:
            return {}
            
        try:
            return self.credentials["modes"][mode]["providers"][provider]
        except KeyError:
            raise ValueError(f"No credentials found for {provider} in {mode} mode")


# Singleton instance
credentials = CredentialsProvider()
