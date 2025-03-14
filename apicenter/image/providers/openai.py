from openai import OpenAI
import base64


def call_openai(model, prompt, credentials, **kwargs):
    """OpenAI DALL-E provider implementation."""
    client = OpenAI(**credentials)
    
    # Check if direct image output is requested
    want_bytes = kwargs.pop("output_format", None) in ["png", "jpeg"]
    
    response = client.images.generate(
        model=model,
        prompt=prompt,
        response_format="url" if not want_bytes else "b64_json",
        **kwargs,
    )

    # Return URLs by default or image data if requested
    if not want_bytes:
        return [img.url for img in response.data]
    else:
        return [base64.b64decode(img.b64_json) for img in response.data][0]