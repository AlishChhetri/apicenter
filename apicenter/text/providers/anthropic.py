"""Anthropic text generation provider implementation."""

from anthropic import Anthropic
from typing import Dict, Any, Union, List

def call_anthropic(model: str, prompt: Union[str, List[Dict[str, str]]], credentials: Dict[str, Any], **kwargs: Any) -> str:
    """Handle text generation requests through Anthropic's Claude API."""
    try:
        # Initialize Anthropic client
        client = Anthropic(api_key=credentials["api_key"])
        
        # Set default max_tokens if not provided
        max_tokens = kwargs.pop("max_tokens", 4096)
        
        # Process input prompt format
        system_prompt = None
        if isinstance(prompt, str):
            # Create a simple user message if prompt is a string
            messages = [{"role": "user", "content": prompt}]
        else:
            # Extract system message and keep other messages
            messages = []
            for msg in prompt:
                if msg.get("role") == "system":
                    system_prompt = msg.get("content")
                else:
                    messages.append(msg)
            
            # Add default user message if only system message was provided
            if not messages:
                messages = [{"role": "user", "content": "Hello"}]
        
        # Build API parameters
        api_params = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            **kwargs
        }
        
        # Add system parameter if present (Anthropic needs it separated)
        if system_prompt:
            api_params["system"] = system_prompt
        
        # Make API request
        response = client.messages.create(**api_params)
        
        # Extract and return generated text
        return response.content[0].text
    except Exception as e:
        raise ValueError(f"Anthropic API error: {str(e)}")