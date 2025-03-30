"""
Basic usage examples for APICenter.

This example demonstrates the universal API pattern for different AI providers.
The key concept is that all providers follow the same basic structure:
    apicenter.<mode>(
        provider="provider_name",
        model="model_name",
        prompt="your prompt",
        **kwargs  # Provider-specific parameters
    )
"""

from apicenter import apicenter

def text_examples():
    """Examples of text generation using different providers."""
    # OpenAI example
    openai_response = apicenter.text(
        provider="openai",
        model="gpt-4",
        prompt="Write a haiku about programming",
        temperature=0.7,
        max_tokens=100
    )
    print("OpenAI Response:", openai_response)

    # Anthropic example
    anthropic_response = apicenter.text(
        provider="anthropic",
        model="claude-3-sonnet-20240229",
        prompt="Explain quantum computing in simple terms",
        temperature=0.7,
        max_tokens=500
    )
    print("Anthropic Response:", anthropic_response)

def main():
    """Run all examples."""
    print("Running text examples...")
    text_examples()

if __name__ == "__main__":
    main() 