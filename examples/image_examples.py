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
import os
from pathlib import Path
import requests

# Create examples/outputs directory if it doesn't exist
OUTPUTS_DIR = Path(__file__).parent / "outputs"
OUTPUTS_DIR.mkdir(exist_ok=True)


def image_examples():
    """Examples of image generation using different providers."""
    # OpenAI DALL-E example
    try:
        dall_e_image = apicenter.image(
            provider="openai",
            model="dall-e-3",
            prompt="A beautiful sunset over mountains, digital art style",
            size="1024x1024",
            quality="standard",
            style="vivid",
        )
        print("DALL-E Image URL:", dall_e_image)

        # Save the URL to a text file
        with open(OUTPUTS_DIR / "dalle_sunset_url.txt", "w") as f:
            f.write(dall_e_image)

        # Download the image
        try:
            response = requests.get(dall_e_image)
            if response.status_code == 200:
                with open(OUTPUTS_DIR / "dalle_sunset.png", "wb") as f:
                    f.write(response.content)
                print(f"Image downloaded to {OUTPUTS_DIR}/dalle_sunset.png")
        except Exception as e:
            print(f"Could not download DALL-E image: {e}")
    except Exception as e:
        print(f"Error with DALL-E: {e}")

    # Stability AI example
    try:
        stability_image = apicenter.image(
            provider="stability",
            model="stable-diffusion-xl",
            prompt="A futuristic cityscape at night, cyberpunk style",
            width=1024,
            height=1024,
            steps=30,
        )
        print("Stability Image generated (bytes):", len(stability_image) if stability_image else 0)

        # Save the image bytes to a file
        if stability_image:
            with open(OUTPUTS_DIR / "stability_cityscape.png", "wb") as f:
                f.write(stability_image)
            print(f"Image saved to {OUTPUTS_DIR}/stability_cityscape.png")
    except Exception as e:
        print(f"Error with Stability AI: {e}")


def main():
    """Run all examples."""
    print("\nRunning image examples...")
    print(f"All outputs will be saved to the '{OUTPUTS_DIR}' directory.")
    image_examples()


if __name__ == "__main__":
    main()
