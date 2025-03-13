import sys
import os
from pathlib import Path
import base64

# Add the project root directory to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from apicenter.image.image import image

def test_openai():
    """Test OpenAI DALL-E image generation."""
    response = image(
        provider="openai",
        model="dall-e-3",
        prompt="a cute puppy",
    )
    print("OpenAI Generated Image URL(s):\n", response)

def test_stability():
    """Test Stability AI image generation."""
    # Create output directory if it doesn't exist
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    response = image(
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

    # print("\nTesting OpenAI DALL-E:")
    # test_openai()

    print("\nTesting Stability AI:")
    test_stability()

if __name__ == "__main__":
    main()

