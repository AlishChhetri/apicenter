from openai import OpenAI


def call_deepseek(model, prompt, credentials, **kwargs):
    """Deepseek provider implementation."""
    client = OpenAI(**credentials)

    response = client.chat.completions.create(
        model=model,
        messages=prompt,
        **kwargs,
    )
    return response.choices[0].message.content
