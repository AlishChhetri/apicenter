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
            
        # Base URL depends on model
        if model.startswith("stable-diffusion-xl") or model.startswith("sdxl"):
            # SDXL models
            base_url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
        elif model == "stable-diffusion-v1-6":
            base_url = "https://api.stability.ai/v1/generation/stable-diffusion-v1-6/text-to-image"
        else:
            # Fallback to a default model if not specifically handled
            base_url = f"https://api.stability.ai/v1/generation/{model}/text-to-image"
        
        # Determine the correct Accept header based on output_format
        accept_header = "application/json"
        if "accept" in kwargs:
            accept_header = kwargs.pop("accept")
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": accept_header,
            "Content-Type": "application/json"
        }

        # Default parameters
        data = {
            "text_prompts": [
                {
                    "text": prompt
                }
            ],
            "height": kwargs.pop("height", 1024),
            "width": kwargs.pop("width", 1024),
            "cfg_scale": kwargs.pop("cfg_scale", 7.0),
            "steps": kwargs.pop("steps", 30),
            "samples": kwargs.pop("samples", 1)
        }
        
        # Add negative prompt if provided
        if "negative_prompt" in kwargs:
            data["text_prompts"].append({
                "text": kwargs.pop("negative_prompt"),
                "weight": -1.0
            })
        
        # Add remaining parameters from kwargs
        for key, value in kwargs.items():
            data[key] = value

        # Make the API call
        response = requests.post(
            base_url,
            headers=headers,
            json=data
        )

        if response.status_code == 200:
            # Extract and return the first image
            result = response.json()
            if 'artifacts' in result and len(result['artifacts']) > 0:
                import base64
                return base64.b64decode(result['artifacts'][0]['base64'])
            else:
                raise ValueError("No images returned by Stability AI API")
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