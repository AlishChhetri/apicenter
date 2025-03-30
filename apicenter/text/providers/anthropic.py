from anthropic import Anthropic
from typing import Dict, Any, Union, List

def call_anthropic(model: str, prompt: Union[str, List[Dict[str, str]]], credentials: Dict[str, Any], **kwargs: Any) -> str:
    """Anthropic provider implementation.
    
    Args:
        model: The model to use (e.g., 'claude-3-sonnet-20240229')
        prompt: Either a string or a list of message dictionaries
        credentials: API credentials dictionary containing api_key
        **kwargs: Additional parameters for the Anthropic API
        
    Returns:
        Generated text response
        
    Raises:
        ValueError: If there's an error with the API call
    """
    try:
        # Create client with API key
        client = Anthropic(api_key=credentials["api_key"])
        
        # Default max_tokens if not provided
        max_tokens = kwargs.pop("max_tokens", 4096)
        
        # Extract system prompt and prepare messages
        system_prompt = None
        if isinstance(prompt, str):
            messages = [{"role": "user", "content": prompt}]
        else:
            # Check if there's a system message in the prompt list
            messages = []
            for msg in prompt:
                if msg.get("role") == "system":
                    system_prompt = msg.get("content")
                else:
                    messages.append(msg)
            
            # If no messages left (only system messages), add a default user message
            if not messages:
                messages = [{"role": "user", "content": "Hello"}]
        
        # Prepare API parameters
        api_params = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            **kwargs
        }
        
        # Add system parameter if present
        if system_prompt:
            api_params["system"] = system_prompt
        
        # Call the API
        response = client.messages.create(**api_params)
        
        return response.content[0].text
    except Exception as e:
        raise ValueError(f"Anthropic API error: {str(e)}")