import ollama
from typing import Dict, Any, List, Union
import os

def call_ollama(model: str, prompt: Union[str, List[Dict[str, str]]], **kwargs: Any) -> str:
    """Ollama provider implementation (local model).
    
    Args:
        model: The model name (must be downloaded to Ollama locally)
        prompt: Either a string or a list of message dictionaries
        **kwargs: Additional parameters for Ollama API
        
    Returns:
        Generated text response
        
    Raises:
        ValueError: If there's an error with the API call or model is not available
    """
    try:
        # Set Ollama host if specified in environment, otherwise use default
        ollama_host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
        
        # Convert to Ollama's expected format if not already
        if isinstance(prompt, str):
            messages = [{"role": "user", "content": prompt}]
        elif isinstance(prompt, list):
            messages = prompt
        else:
            raise ValueError("Prompt must be a string or a list of message dictionaries")
        
        # Make the API call
        response = ollama.chat(
            model=model,
            messages=messages,
            **kwargs
        )
        
        return response["message"]["content"]
    except Exception as e:
        raise ValueError(f"Ollama API error: {str(e)}\nMake sure Ollama is running and you've pulled the model with 'ollama pull {model}'.")