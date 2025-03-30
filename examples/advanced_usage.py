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
            temperature=0.8,      # Will be passed through options parameter
            num_predict=300,      # Will be passed through options parameter
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
        response = apicenter.image(
            provider="openai",
            model="dall-e-3",
            prompt="A detailed steampunk cityscape with flying airships and clockwork machines",
            size="1024x1024",
            quality="hd",
            style="vivid",
        )
        print("\nOpenAI DALL-E Advanced Response (URL):")
        print(response)
        print("You can download this image from the URL and save it locally if needed.")
    except Exception as e:
        print(f"\nError with OpenAI DALL-E: {e}")

    # Stability AI with specific parameters
    try:
        response = apicenter.image(
            provider="stability",
            model="stable-diffusion-xl-1024-v1-0",
            prompt="A photorealistic portrait of a Viking warrior with detailed armor and weapons",
            height=1024,
            width=1024,
            steps=50,
            cfg_scale=7.0,
            negative_prompt="ugly, blurry, low quality",
        )
        print("\nStability AI Advanced Response (bytes length):")
        print(f"Generated image bytes: {len(response) if response else 0}")
        
        # Save the image if we got a response
        if response:
            os.makedirs("outputs", exist_ok=True)
            with open("outputs/stability_viking.png", "wb") as f:
                f.write(response)
            print("Image saved to outputs/stability_viking.png")
    except Exception as e:
        print(f"\nError with Stability AI: {e}")


def advanced_audio_generation():
    """Advanced audio generation examples with various parameters."""
    print("\n=== ADVANCED AUDIO GENERATION ===")
    
    # ElevenLabs with specific parameters
    try:
        response = apicenter.audio(
            provider="elevenlabs",
            model="eleven_multilingual_v2",
            prompt="Hello! This is a test of advanced text-to-speech parameters with APICenter.",
            stability=0.5,         # VoiceSettings parameter
            similarity_boost=0.75, # VoiceSettings parameter
        )
        print("\nElevenLabs Advanced Response (bytes):")
        print(f"Generated audio bytes: {len(response) if response else 0}")
        
        # Save the audio if we got a response
        if response:
            os.makedirs("outputs", exist_ok=True)
            with open("outputs/elevenlabs_advanced.mp3", "wb") as f:
                f.write(response)
            print("Audio saved to outputs/elevenlabs_advanced.mp3")
    except Exception as e:
        print(f"\nError with ElevenLabs: {e}")


def save_responses_example():
    """Example of how to save responses from different providers."""
    print("\n=== SAVING RESPONSES EXAMPLE ===")
    
    try:
        # Generate a text response
        text_response = apicenter.text(
            provider="openai",
            model="gpt-3.5-turbo",
            prompt="Generate a short JSON object describing a fictional person",
        )
        
        # Save as plain text
        os.makedirs("outputs", exist_ok=True)
        with open("outputs/text_response.txt", "w") as f:
            f.write(text_response)
            
        # Save as structured data (assume JSON response)
        try:
            person_data = json.loads(text_response)
            with open("outputs/structured_response.json", "w") as f:
                json.dump(person_data, f, indent=2)
            print("\nText response saved as both plain text and structured JSON")
        except json.JSONDecodeError:
            # Not valid JSON, just save as text
            print("\nText response saved as plain text only (not valid JSON)")
        
        print("""
To save an image from a URL returned by some providers:
import requests
image_url = apicenter.image(...)
response = requests.get(image_url)
with open('outputs/image.png', 'wb') as f:
    f.write(response.content)
""")
    except Exception as e:
        print(f"\nError saving responses: {e}")


def main():
    """Advanced examples of using APICenter with various parameters."""
    print("APICenter Advanced Usage Examples")
    print("================================")
    print("This demonstrates more complex usage of the API with various parameters.")
    
    # Run advanced examples
    advanced_text_generation()
    advanced_image_generation()
    advanced_audio_generation()
    save_responses_example()
    
    print("\nAll advanced examples completed!")


if __name__ == "__main__":
    main() 