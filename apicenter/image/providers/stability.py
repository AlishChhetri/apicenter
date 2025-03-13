import requests

def call_stability(model, prompt, credentials, **kwargs):
    """Stability AI provider implementation."""
    api_key = credentials.get("api_key")
    if not api_key:
        return "Error: Missing Stability API key"
        
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
        return f"Error: {response.status_code} - {response.text}"