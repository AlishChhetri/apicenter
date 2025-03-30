"""Stability AI image generation provider implementation."""

import requests
import base64
from typing import Dict, Any, Optional, Union, List


def call_stability(model: str, prompt: str, credentials: Dict[str, Any], **kwargs: Any) -> bytes:
    """Handle image generation requests through Stability AI's API."""
    try:
        # Verify API key is present
        api_key = credentials.get("api_key")
        if not api_key:
            raise ValueError("Missing Stability AI API key")

        # Determine appropriate API endpoint based on model
        if model.startswith("stable-diffusion-xl") or model.startswith("sdxl"):
            # SDXL models
            base_url = (
                "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
            )
        elif model == "stable-diffusion-v1-6":
            base_url = "https://api.stability.ai/v1/generation/stable-diffusion-v1-6/text-to-image"
        else:
            # Use generic endpoint for other models
            base_url = f"https://api.stability.ai/v1/generation/{model}/text-to-image"

        # Set up request headers
        accept_header = "application/json"
        if "accept" in kwargs:
            accept_header = kwargs.pop("accept")

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": accept_header,
            "Content-Type": "application/json",
        }

        # Configure generation parameters with defaults
        data = {
            "text_prompts": [{"text": prompt}],
            "height": kwargs.pop("height", 1024),
            "width": kwargs.pop("width", 1024),
            "cfg_scale": kwargs.pop("cfg_scale", 7.0),
            "steps": kwargs.pop("steps", 30),
            "samples": kwargs.pop("samples", 1),
        }

        # Add negative prompt if provided
        if "negative_prompt" in kwargs:
            data["text_prompts"].append({"text": kwargs.pop("negative_prompt"), "weight": -1.0})

        # Include any remaining parameters
        for key, value in kwargs.items():
            data[key] = value

        # Make API request to generate image
        response = requests.post(base_url, headers=headers, json=data)

        # Handle successful response
        if response.status_code == 200:
            # Extract and decode the first generated image
            result = response.json()
            if "artifacts" in result and len(result["artifacts"]) > 0:
                return base64.b64decode(result["artifacts"][0]["base64"])
            else:
                raise ValueError("No images returned by Stability AI API")
        else:
            # Handle error response
            error_message = f"Stability AI API error: {response.status_code}"
            try:
                error_details = response.json()
                error_message = f"{error_message} - {error_details.get('message', 'Unknown error')}"
            except Exception as json_error:
                error_message = f"{error_message} - {response.text}"

            raise ValueError(error_message)
    except Exception as e:
        if isinstance(e, ValueError):
            raise
        raise ValueError(f"Stability AI API error: {str(e)}")
