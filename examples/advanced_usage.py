from apicenter import apicenter
import json
import os
from pathlib import Path
import requests
from typing import Optional, Dict, Any

def save_audio_to_file(audio_data: bytes, filename: str) -> None:
    """Save audio data to a file."""
    with open(filename, 'wb') as f:
        f.write(audio_data)
    print(f"Audio saved to {filename}")

def download_image(url: str, filename: str) -> None:
    """Download an image from a URL and save it."""
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Image downloaded to {filename}")
    else:
        print(f"Failed to download image: {response.status_code}")

def advanced_text_generation():
    """Advanced text generation examples with various parameters."""
    print("\n=== ADVANCED TEXT GENERATION ===")

    # OpenAI with specific parameters
    try:
        response = apicenter.text(
            provider="openai",
            model="gpt-4",
            prompt="Generate a recipe for a vegetarian pasta dish",
            temperature=0.7,
            max_tokens=500,
            top_p=0.95,
            frequency_penalty=0.0,
            presence_penalty=0.0,
        )
        print("\nOpenAI Advanced Response:")
        print(response)
    except Exception as e:
        print(f"\nError with OpenAI: {e}")

    # Anthropic with system prompt and message history
    try:
        response = apicenter.text(
            provider="anthropic",
            model="claude-3-sonnet-20240229",
            prompt=[
                {"role": "system", "content": "You are a helpful assistant that explains complex topics simply."},
                {"role": "user", "content": "Explain quantum computing to me like I'm 10 years old."}
            ],
            temperature=0.3,
            max_tokens=800,
        )
        print("\nAnthropic Advanced Response:")
        print(response)
    except Exception as e:
        print(f"\nError with Anthropic: {e}")
        
    # Ollama with custom parameters
    try:
        response = apicenter.text(
            provider="ollama",
            model="deepseek-r1", # or another model you've pulled locally
            prompt="Write a short poem about artificial intelligence",
            temperature=0.8,
            num_predict=300,
        )
        print("\nOllama Advanced Response:")
        print(response)
    except Exception as e:
        print(f"\nError with Ollama: {e}")


def advanced_image_generation():
    """Advanced image generation examples with various parameters."""
    print("\n=== ADVANCED IMAGE GENERATION ===")

    # OpenAI DALL-E with specific parameters
    try:
        image_url = apicenter.image(
            provider="openai",
            model="dall-e-3",
            prompt="A photorealistic image of a futuristic city with flying cars and vertical gardens",
            size="1024x1024",
            quality="hd",
            style="natural",
        )
        print("\nOpenAI DALL-E Advanced Response (URL):")
        print(image_url)
        
        # Example of saving image URL to a file
        print("You can download this image from the URL and save it locally if needed.")
    except Exception as e:
        print(f"\nError with OpenAI image: {e}")

    # Stability AI with specific parameters
    try:
        image_data = apicenter.image(
            provider="stability",
            model="stable-diffusion-xl-1024-v1-0",
            prompt="An oil painting of a peaceful mountain landscape at sunset",
            steps=50,
            cfg_scale=7.5,
            width=1024,
            height=1024,
        )
        
        # For raw image bytes, you would typically save to file
        if isinstance(image_data, bytes):
            save_path = "stability_output.png"
            with open(save_path, "wb") as f:
                f.write(image_data)
            print(f"\nStability AI Advanced Response: Image saved to {save_path}")
        else:
            print(f"\nStability AI Advanced Response: {image_data}")
    except Exception as e:
        print(f"\nError with Stability AI: {e}")


def advanced_audio_generation():
    """Advanced audio generation examples with various parameters."""
    print("\n=== ADVANCED AUDIO GENERATION ===")

    # ElevenLabs with specific parameters
    try:
        audio_data = apicenter.audio(
            provider="elevenlabs",
            model="eleven_multilingual_v2",
            prompt="The quick brown fox jumps over the lazy dog. This is a test of advanced text-to-speech parameters.",
            voice_id="Adam",  # specific voice
            stability=0.5,
            similarity_boost=0.75,
            style=0.3,
            use_speaker_boost=True,
        )
        
        # Save to file with descriptive name
        save_path = "elevenlabs_advanced_output.mp3"
        if audio_data:
            with open(save_path, "wb") as f:
                f.write(audio_data)
            print(f"\nElevenLabs Advanced Response: Audio saved to {save_path}")
            print(f"Audio size: {len(audio_data)} bytes")
    except Exception as e:
        print(f"\nError with ElevenLabs: {e}")


def save_response_example():
    """Example of how to save responses in various formats."""
    print("\n=== SAVING RESPONSES EXAMPLE ===")
    
    # Create output directory if it doesn't exist
    os.makedirs("outputs", exist_ok=True)
    
    # Example 1: Save text to file
    try:
        response = apicenter.text(
            provider="openai",
            model="gpt-3.5-turbo",
            prompt="Write a JSON structure for a user profile",
        )
        
        # Save as plain text
        with open("outputs/text_response.txt", "w") as f:
            f.write(response)
            
        # Try to parse and save as JSON if possible
        try:
            json_data = json.loads(response)
            with open("outputs/parsed_response.json", "w") as f:
                json.dump(json_data, f, indent=2)
            print("\nText response saved as both plain text and structured JSON")
        except json.JSONDecodeError:
            print("\nText response saved as plain text only (not valid JSON)")
    except Exception as e:
        print(f"\nError saving text response: {e}")

    # Example 2: Save image from URL
    # Note: This would typically use a library like requests to download the image
    print("\nTo save an image from a URL returned by some providers:")
    print("import requests")
    print("image_url = apicenter.image(...)")
    print("response = requests.get(image_url)")
    print("with open('outputs/image.png', 'wb') as f:")
    print("    f.write(response.content)")


def main():
    """Advanced examples of using APICenter with various parameters."""
    print("APICenter Advanced Usage Examples")
    print("================================")
    print("This demonstrates more complex usage of the API with various parameters.")
    
    # Run advanced examples
    advanced_text_generation()
    advanced_image_generation()
    advanced_audio_generation()
    save_response_example()
    
    print("\nAll advanced examples completed!")


if __name__ == "__main__":
    main() 