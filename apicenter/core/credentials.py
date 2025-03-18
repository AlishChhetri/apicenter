import json
from pathlib import Path


class CredentialsProvider:
    def __init__(self):
        """Load and parse API credentials from JSON file."""
        self.credentials_path = Path(__file__).parent.parent.parent / "credentials.json"
        self.credentials = self.load_credentials()

    def load_credentials(self):
        """Load credentials from JSON file."""
        try:
            with open(self.credentials_path) as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(
                "credentials.json not found. Please create one using the template."
            )
        except json.JSONDecodeError:
            raise ValueError(
                "credentials.json is not a valid JSON file."
            )

    def get_credentials(self, mode, provider):
        """Get credentials for a specific mode and provider."""
        try:
            return self.credentials["modes"][mode]["providers"][provider]
        except KeyError:
            if provider == "ollama":  # Special case for local providers
                return {}
            raise ValueError(f"No credentials found for {provider} in {mode} mode")


# Singleton instance
credentials = CredentialsProvider()
