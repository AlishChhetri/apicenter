import sys
import os
from pathlib import Path

# Add the project root directory to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from apicenter.apicenter import apicenter


def test_openai_url():
    """Test OpenAI DALL-E image generation."""
    response = apicenter.image(
        provider="openai",
        model="dall-e-3",
        prompt="a cute puppy",
    )
    print("OpenAI Generated Image URL(s):\n", response)


def test_openai_byte():
    """Test OpenAI DALL-E image generation."""
    # Create output directory if it doesn't exist
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    # Test direct image output
    response = apicenter.image(
        provider="openai",
        model="dall-e-3",
        prompt="a cute puppy",
        output_format="png",
    )

    if isinstance(response, bytes):
        output_path = output_dir / "test_openai_byte_output.png"
        with open(output_path, "wb") as f:
            f.write(response)
        print(f"OpenAI image saved as: {output_path}")
    else:
        print("OpenAI Error:", response)


def test_stability():
    """Test Stability AI image generation."""
    # Create output directory if it doesn't exist
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    response = apicenter.image(
        provider="stability",
        model="ultra",
        prompt="a cute puppy playing in the snow",
        output_format="png",  # Changed to png
    )

    # Save the image
    if isinstance(response, bytes):  # Check if response is binary data
        output_path = output_dir / "stability_test_output.png"
        with open(output_path, "wb") as f:
            f.write(response)
        print(f"Stability AI image saved as: {output_path}")
    else:
        print("Stability AI Error:", response)


def main():
    """Main function to test image generation providers."""

    print("\nTesting OpenAI URL DALL-E:")
    test_openai_url()

    print("\nTesting OpenAI Byte DALL-E:")
    test_openai_byte()

    # print("\nTesting Stability AI:")
    # test_stability()


if __name__ == "__main__":
    main()
