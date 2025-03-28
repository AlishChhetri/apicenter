from apicenter.core.credentials import credentials
from .providers.openai import call_openai
from .providers.anthropic import call_anthropic
from .providers.ollama import call_ollama
from .providers.deepseek import call_deepseek
from typing import Any, Dict, Optional
import openai
from anthropic import Anthropic
from ..core.base import BaseProvider, ProviderConfig


class TextProvider(BaseProvider[str]):
    """Provider for text generation using various AI services."""
    
    def _get_mode(self) -> str:
        return "text"
    
    def validate_params(self) -> None:
        """Validate the provider-specific parameters."""
        if self.provider == "openai":
            if not self.model.startswith(("gpt-", "text-", "code-")):
                raise ValueError(f"Invalid OpenAI model: {self.model}")
            if "temperature" in self.kwargs and not 0 <= self.kwargs["temperature"] <= 2:
                raise ValueError("OpenAI temperature must be between 0 and 2")
        elif self.provider == "anthropic":
            if not self.model.startswith(("claude-", "sonnet-", "opus-")):
                raise ValueError(f"Invalid Anthropic model: {self.model}")
            if "temperature" in self.kwargs and not 0 <= self.kwargs["temperature"] <= 1:
                raise ValueError("Anthropic temperature must be between 0 and 1")
        else:
            raise ValueError(f"Unsupported text provider: {self.provider}")
    
    def call(self) -> str:
        """Make the API call and return the response."""
        if self.provider == "openai":
            return self._call_openai()
        elif self.provider == "anthropic":
            return self._call_anthropic()
        else:
            raise ValueError(f"Unsupported text provider: {self.provider}")
    
    def _call_openai(self) -> str:
        """Call OpenAI's API."""
        client = openai.OpenAI(
            api_key=self.config.api_key,
            organization=self.config.organization
        )
        
        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": self.prompt}],
            **self.kwargs
        )
        
        return response.choices[0].message.content
    
    def _call_anthropic(self) -> str:
        """Call Anthropic's API."""
        client = Anthropic(api_key=self.config.api_key)
        
        response = client.messages.create(
            model=self.model,
            max_tokens=self.kwargs.get("max_tokens", 4096),
            temperature=self.kwargs.get("temperature", 0.7),
            messages=[{"role": "user", "content": self.prompt}]
        )
        
        return response.content[0].text


def text(provider, model, prompt, **kwargs):
    """Universal function to call any supported AI model with minimal input."""
    return TextProvider(provider, model, prompt, **kwargs).call()
