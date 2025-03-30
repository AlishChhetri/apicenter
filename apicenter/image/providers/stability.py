import requests
from typing import Dict, Any, Optional, Union

def call_stability(model: str, prompt: str, credentials: Dict[str, Any], **kwargs: Any) -> bytes:
    """Stability AI provider implementation.
    
    Args:
        model: The model to use (e.g., 'stable-diffusion-xl-1024-v1-0')
        prompt: The text description of the image to generate
        credentials: API credentials dictionary containing api_key
        **kwargs: Additional parameters for the Stability AI API
        
    Returns:
        Raw image data as bytes
        
    Raises:
        ValueError: If there's an error with the API call
    """
    try:
        api_key = credentials.get("api_key")
        if not api_key:
            raise ValueError("Missing Stability AI API key")
            
        # Hardcoded base URL - not taken from credentials.json
        base_url = "https://api.stability.ai/v2beta"
        
        headers = {
            "authorization": f"Bearer {api_key}",
            "accept": "image/*"
        }

        # Default parameters
        data = {
            "prompt": prompt,
            "output_format": kwargs.pop("output_format", "webp"),
        }
        
        # Add any additional parameters from kwargs
        data.update(kwargs)

        response = requests.post(
            f"{base_url}/stable-image/generate/{model}",
            headers=headers,
            files={"none": ""},  # Required for multipart/form-data
            data=data
        )

        if response.status_code == 200:
            return response.content  # Returns raw image data
        else:
            error_message = f"Stability AI API error: {response.status_code}"
            try:
                error_details = response.json()
                error_message = f"{error_message} - {error_details.get('message', 'Unknown error')}"
            except:
                error_message = f"{error_message} - {response.text}"
            
            raise ValueError(error_message)
    except Exception as e:
        if isinstance(e, ValueError):
            raise
        raise ValueError(f"Stability AI API error: {str(e)}")