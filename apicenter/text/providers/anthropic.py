from anthropic import Anthropic

def call_anthropic(model, prompt, credentials, **kwargs):
    """Anthropic provider implementation."""
    client = Anthropic(api_key=credentials["api_key"])
    
    max_tokens = kwargs.pop("max_tokens", 100)
    
    response = client.messages.create(
        model=model,
        messages=prompt,
        max_tokens=max_tokens,
        **kwargs,
    )
    return response.content[0].text