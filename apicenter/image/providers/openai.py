from openai import OpenAI

def call_openai(model, prompt, credentials, **kwargs):
    """OpenAI DALL-E provider implementation."""
    client = OpenAI(**credentials)
    
    response = client.images.generate(
        model=model,
        prompt=prompt,
        **kwargs,
    )
    return [img.url for img in response.data]