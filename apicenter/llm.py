"""LLM class to handle requests to both Anthropic and OpenAI APIs"""

import anthropic
import openai

from apicenter.config import ANTHROPIC_KEY, OPENAI_KEY, OPENAI_ORG



class LLM:
    """Handles requests to both Anthropic and OpenAI APIs"""

    def __init__(self):
        # Initialize clients for both APIs
        self.anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)
        self.openai_client = openai.OpenAI(api_key=OPENAI_KEY, organization=OPENAI_ORG)

    def call_anthropic_api(
        self, model, system, messages, max_tokens=100, temperature=0.7
    ):
        """Sends a request to the Anthropic API with specified configurations"""
        message = self.anthropic_client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system,
            messages=messages,
        )

        # Return just the text content to keep the output format consistent
        if hasattr(message, "content"):
            return message.content
        else:
            return message

    def call_openai_api(self, model, messages, max_tokens=100, temperature=0.7):
        """Sends a request to the OpenAI API with specified configurations"""
        response = self.openai_client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return response.choices[0].message.content.strip()
