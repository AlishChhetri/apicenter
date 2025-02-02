import os
import json
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


class APIConfig:
    def __init__(self):
        """Load and parse API credentials from environment variables."""
        json_string = os.getenv("API_CREDENTIALS")

        if not json_string:
            raise ValueError("Missing API_CREDENTIALS in .env file.")

        try:
            self.credentials = json.loads(json_string)
        except json.JSONDecodeError:
            raise ValueError(
                "Invalid JSON format in API_CREDENTIALS. Please check your .env file."
            )

    def get_credentials(self, provider):
        """Retrieve credentials for a given API provider (LLMs & Image APIs)."""
        creds = self.credentials.get(provider)

        if creds is None:
            return {}  # Local models like Ollama should return an empty dict

        # Ensure required fields exist
        if isinstance(creds, dict) and "api_key" in creds and not creds["api_key"]:
            raise ValueError(f"Error: Missing API key for {provider}.")

        return creds  # Return the full credentials dictionary


# Singleton instance to load config once
config = APIConfig()
