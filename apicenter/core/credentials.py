"""API credential management system for authentication with service providers."""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional


class CredentialsProvider:
    """Provider for loading and managing API credentials across services."""
    
    def __init__(self) -> None:
        """Initialize credentials by locating and loading the credentials file."""
        self.credentials_path = self.find_credentials_file()
        self.credentials = self.load_credentials()

    def find_credentials_file(self) -> Path:
        """Locate credentials file in standard locations or from environment variable."""
        # Check environment variable first
        env_path = os.getenv('APICENTER_CREDENTIALS_PATH')
        if env_path:
            return Path(env_path)
            
        # Search for credentials file in standard locations
        possible_paths = [
            Path.cwd() / 'credentials.json',  # Current directory
            Path(__file__).parent.parent.parent / 'credentials.json',  # Project root
            Path.home() / '.apicenter' / 'credentials.json',  # User's home directory
            Path.home() / '.config' / 'apicenter' / 'credentials.json',  # XDG config dir
        ]
        
        # Return first existing credentials file
        for path in possible_paths:
            if path.exists():
                return path
                
        # Default to project root if no file found
        return Path(__file__).parent.parent.parent / 'credentials.json'

    def load_credentials(self) -> Dict[str, Any]:
        """Load and parse credentials from JSON file with fallback for missing file."""
        try:
            # Try to load from file
            with open(self.credentials_path) as f:
                return json.load(f)
        except FileNotFoundError:
            # Create minimal structure for local-only usage
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
        """Retrieve credentials for a specific provider in a given mode."""
        # No credentials needed for local providers
        if provider in ["ollama"]:
            return {}
            
        # Look up credentials in the loaded configuration
        try:
            return self.credentials["modes"][mode]["providers"][provider]
        except KeyError:
            raise ValueError(f"No credentials found for {provider} in {mode} mode")


# Singleton instance for global access
credentials = CredentialsProvider()
