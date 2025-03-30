from openai import OpenAI
from typing import Dict, Any, Union, List

def call_openai(model: str, prompt: Union[str, List[Dict[str, str]]], credentials: Dict[str, Any], **kwargs: Any) -> str:
    """OpenAI provider implementation.
    
    Args:
        model: The model to use (e.g., 'gpt-4')
        prompt: Either a string or a list of message dictionaries
        credentials: API credentials dictionary containing api_key and possibly organization
        **kwargs: Additional parameters for the OpenAI API
        
    Returns:
        Generated text response
        
    Raises:
        ValueError: If there's an error with the API call
    """
    try:
        # Convert simple string prompt to messages format if needed
        if isinstance(prompt, str):
            messages = [{"role": "user", "content": prompt}]
        else:
            messages = prompt
            
        # Create client with API key and optional organization
        client = OpenAI(**credentials)
        
        # Call the API
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            **kwargs
        )
        
        return response.choices[0].message.content
    except Exception as e:
        raise ValueError(f"OpenAI API error: {str(e)}")