from apicenter.core.credentials import credentials
from .providers.openai import call_openai
from .providers.anthropic import call_anthropic
from .providers.ollama import call_ollama
from .providers.deepseek import call_deepseek


class LLMProvider:
    def __init__(self, provider, model, prompt, **kwargs):
        self.provider = provider.lower()
        self.model = model
        self.prompt = self.format_prompt(prompt)
        self.kwargs = kwargs
        self.credentials = credentials.get_credentials("llm", self.provider)

    def format_prompt(self, prompt):
        """Format the prompt to ensure it meets the API requirements."""
        if isinstance(prompt, str):
            return [{"role": "user", "content": prompt}]
        elif isinstance(prompt, list):
            return prompt
        else:
            raise ValueError(
                "Invalid prompt format. Must be a string or a list of messages."
            )

    def get_response(self):
        """Automatically call the right API based on provider."""
        providers = {
            "openai": lambda: call_openai(self.model, self.prompt, self.credentials, **self.kwargs),
            "anthropic": lambda: call_anthropic(self.model, self.prompt, self.credentials, **self.kwargs),
            "ollama": lambda: call_ollama(self.model, self.prompt, **self.kwargs),
            "deepseek": lambda: call_deepseek(self.model, self.prompt, self.credentials, **self.kwargs),
        }

        return providers.get(
            self.provider, lambda: f"Error: Unsupported provider {self.provider}"
        )()


def llm(provider, model, prompt, **kwargs):
    """Universal function to call any supported AI model with minimal input."""
    return LLMProvider(provider, model, prompt, **kwargs).get_response()
