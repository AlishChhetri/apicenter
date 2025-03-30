"""Ollama local model text generation provider implementation."""

import ollama
from typing import Dict, Any, List, Union
import os

def call_ollama(model: str, prompt: Union[str, List[Dict[str, str]]], **kwargs: Any) -> str:
    """Handle text generation requests through locally running Ollama models."""
    try:
        # Configure Ollama host from environment or use default
        ollama_host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
        
        # Process input based on format
        if isinstance(prompt, str):
            # Simple string prompt becomes a user message
            messages = [{"role": "user", "content": prompt}]
        elif isinstance(prompt, list):
            # Handle message list format with special system prompt handling
            messages = []
            system_content = None
            
            # Extract system messages since not all models support them directly
            for msg in prompt:
                if msg.get("role") == "system":
                    system_content = msg.get("content")
                else:
                    messages.append(msg)
            
            # Add default message if only system prompt was provided
            if system_content and not messages:
                messages = [{"role": "user", "content": "Hello"}]
                
            # Incorporate system message into first user message for compatibility
            if system_content and messages and messages[0].get("role") == "user":
                user_msg = messages[0]
                user_msg["content"] = f"[System: {system_content}]\n\n{user_msg['content']}"
        else:
            raise ValueError("Prompt must be a string or a list of message dictionaries")
        
        # Separate parameters for direct chat API vs. model options
        chat_params = {}
        model_options = {}
        
        # Extract core chat parameters
        if "stream" in kwargs:
            chat_params["stream"] = kwargs.pop("stream")
        if "format" in kwargs:
            chat_params["format"] = kwargs.pop("format")
        if "keep_alive" in kwargs:
            chat_params["keep_alive"] = kwargs.pop("keep_alive")
        if "tools" in kwargs:
            chat_params["tools"] = kwargs.pop("tools")
        
        # All remaining parameters become model options
        if kwargs:
            model_options = kwargs
        
        # Build API parameters
        api_params = {
            "model": model,
            "messages": messages,
        }
        
        # Add model options if provided
        if model_options:
            api_params["options"] = model_options
            
        # Add chat-specific parameters
        api_params.update(chat_params)
            
        # Make API call to local Ollama instance
        response = ollama.chat(**api_params)
        
        # Extract and return generated text
        return response["message"]["content"]
    except Exception as e:
        raise ValueError(f"Ollama API error: {str(e)}\nMake sure Ollama is running and you've pulled the model with 'ollama pull {model}'.")