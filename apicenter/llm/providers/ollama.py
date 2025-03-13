from ollama import chat as ollama_chat

def call_ollama(model, prompt, **kwargs):
    """Ollama provider implementation (local model)."""
    response = ollama_chat(
        model=model,
        messages=prompt,
        **kwargs,
    )
    return response.message.content