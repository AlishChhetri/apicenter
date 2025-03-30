"""OpenAI text generation provider implementation."""

from openai import OpenAI
from typing import Dict, Any, Union, List

def call_openai(model: str, prompt: Any, credentials: Dict[str, Any], **kwargs: Any) -> str:
    """Handle text generation requests through OpenAI's API."""
    try:
        # Format prompt as messages if it's a simple string
        if isinstance(prompt, str):
            messages = [{"role": "user", "content": prompt}]
        else:
            messages = prompt
            
        # Initialize OpenAI client with credentials
        client = OpenAI(**credentials)
        
        # Make API request
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            **kwargs
        )
        
        # Extract and return the generated text
        return response.choices[0].message.content
    except Exception as e:
        raise ValueError(f"OpenAI API error: {str(e)}")