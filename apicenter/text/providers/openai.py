from openai import OpenAI

def call_openai(model, prompt, credentials, **kwargs):
    """OpenAI provider implementation."""
    client = OpenAI(**credentials)
    
    response = client.chat.completions.create(
        model=model,
        messages=prompt,
        **kwargs,
    )
    return response.choices[0].message.content