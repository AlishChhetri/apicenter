import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


class APIConfig:
    def __init__(self):
        """Load and parse API credentials from environment variables."""
        self.credentials = {
            "openai": {
                "api_key": os.getenv("OPENAI_API_KEY"),
                "organization": os.getenv("OPENAI_ORGANIZATION")
            },
            "anthropic": {
                "api_key": os.getenv("ANTHROPIC_API_KEY")
            },
            "deepseek": {
                "api_key": os.getenv("DEEPSEEK_API_KEY"),
                "base_url": os.getenv("DEEPSEEK_BASE_URL")
            },
            "monster": {
                "api_key": os.getenv("MONSTER_API_KEY")
            },
            "stablediffusion": {
                "api_key": os.getenv("STABLEDIFFUSION_API_KEY"),
                "base_url": os.getenv("STABLEDIFFUSION_BASE_URL")
            },
            "creatomate": {
                "api_key": os.getenv("CREATOMATE_API_KEY"),
                "base_url": os.getenv("CREATOMATE_BASE_URL")
            }
        }

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
