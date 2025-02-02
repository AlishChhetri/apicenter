from openai import OpenAI
from anthropic import Anthropic
from ollama import chat as ollama_chat
from config import config


class LLMProvider:
    def __init__(self, provider, model, prompt, **kwargs):
        self.provider = provider.lower()
        self.model = model
        self.prompt = prompt
        self.kwargs = kwargs  # Stores all optional params

        # Load credentials (returns {} if none needed)
        self.credentials = config.get_credentials(self.provider)

    def get_response(self):
        """Automatically call the right API based on provider."""
        providers = {
            "openai": self._call_openai,
            "anthropic": self._call_anthropic,
            "ollama": self._call_ollama,
            "deepseek": self._call_deepseek,
        }

        return providers.get(
            self.provider, lambda: f"Error: Unsupported provider {self.provider}"
        )()

    def _call_openai(self):
        client = OpenAI(**self.credentials)

        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": self.prompt}],
            **self.kwargs,  # Pass optional params (e.g., temperature, stream)
        )
        return response.choices[0].message.content

    def _call_anthropic(self):
        client = Anthropic(**self.credentials)

        response = client.messages.create(
            model=self.model,
            messages=[{"role": "user", "content": self.prompt}],
            **self.kwargs,
        )
        return response.content

    def _call_ollama(self):
        """Ollama is a local model (no credentials needed)."""
        response = ollama_chat(
            model=self.model,
            messages=[{"role": "user", "content": self.prompt}],
            **self.kwargs,
        )
        return response.message.content

    def _call_deepseek(self):
        client = OpenAI(**self.credentials)

        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": self.prompt}],
            **self.kwargs,
        )
        return response.choices[0].message.content


def llm(provider, model, prompt, **kwargs):
    """Universal function to call any supported AI model with minimal input."""
    return LLMProvider(provider, model, prompt, **kwargs).get_response()
