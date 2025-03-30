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

def image_examples():
    """Examples of image generation using different providers."""
    # OpenAI DALL-E example
    dall_e_image = apicenter.image(
        provider="openai",
        model="dall-e-3",
        prompt="A beautiful sunset over mountains, digital art style",
        size="1024x1024",
        quality="standard",
        style="vivid"
    )
    print("DALL-E Image URL:", dall_e_image)

    # Stability AI example
    stability_image = apicenter.image(
        provider="stability",
        model="stable-diffusion-xl",
        prompt="A futuristic cityscape at night, cyberpunk style",
        width=1024,
        height=1024,
        steps=30
    )
    print("Stability Image:", stability_image)

def main():
    """Run all examples."""
    print("\nRunning image examples...")
    image_examples()

if __name__ == "__main__":
    main() 