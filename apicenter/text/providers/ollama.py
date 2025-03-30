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
            # Some Ollama models might support system prompts directly,
            # others might need special handling, but most will simply
            # ignore system messages. Process them for consistency.
            messages = []
            system_content = None
            
            # Process messages and extract system content if present
            for msg in prompt:
                if msg.get("role") == "system":
                    # Save system content, but don't add to messages
                    system_content = msg.get("content")
                else:
                    messages.append(msg)
            
            # If we have a system message but no user messages, add a default one
            if system_content and not messages:
                messages = [{"role": "user", "content": "Hello"}]
                
            # If we have system content and the first message is from the user,
            # prepend system content to that message for models that don't support
            # system messages directly
            if system_content and messages and messages[0].get("role") == "user":
                user_msg = messages[0]
                # Combine system instruction with user message
                user_msg["content"] = f"[System: {system_content}]\n\n{user_msg['content']}"
        else:
            raise ValueError("Prompt must be a string or a list of message dictionaries")
        
        # Separate chat parameters from model parameters
        chat_params = {}
        model_options = {}
        
        # Extract parameters supported by the chat method
        if "stream" in kwargs:
            chat_params["stream"] = kwargs.pop("stream")
        if "format" in kwargs:
            chat_params["format"] = kwargs.pop("format")
        if "keep_alive" in kwargs:
            chat_params["keep_alive"] = kwargs.pop("keep_alive")
        if "tools" in kwargs:
            chat_params["tools"] = kwargs.pop("tools")
        
        # All other parameters go to options
        # These include: temperature, top_p, top_k, num_predict, etc.
        if kwargs:
            model_options = kwargs
        
        # Prepare API call parameters
        api_params = {
            "model": model,
            "messages": messages,
        }
        
        # Add options if we have any
        if model_options:
            api_params["options"] = model_options
            
        # Add other chat parameters
        api_params.update(chat_params)
            
        # Make the API call
        response = ollama.chat(**api_params)
        
        return response["message"]["content"]
    except Exception as e:
        raise ValueError(f"Ollama API error: {str(e)}\nMake sure Ollama is running and you've pulled the model with 'ollama pull {model}'.")