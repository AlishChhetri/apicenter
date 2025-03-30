from apicenter import apicenter
import os

def text_examples():
    """Examples of text generation with different providers."""
    print("\n=== TEXT GENERATION EXAMPLES ===")

    # OpenAI text generation
    try:
        response = apicenter.text(
            provider="openai",
            model="gpt-4",
            prompt="Write a haiku about programming"
        )
        print("\nOpenAI Response:")
        print(response)
    except Exception as e:
        print(f"\nError with OpenAI: {e}")
    
    # Anthropic text generation
    try:
        response = apicenter.text(
            provider="anthropic",
            model="claude-3-sonnet-20240229",
            prompt="Write a short story about a robot"
        )
        print("\nAnthropic Response:")
        print(response)
    except Exception as e:
        print(f"\nError with Anthropic: {e}")
    
    # Local Ollama text generation
    try:
        print("\nTrying Ollama (requires local installation)...")
        response = apicenter.text(
            provider="ollama",
            model="llama2", # or another model you've pulled locally
            prompt="What is the capital of France?"
        )
        print("\nOllama Response:")
        print(response)
    except Exception as e:
        print(f"\nError with Ollama: {e}")
        print("Note: Ollama requires a local installation with models downloaded.")
        print("Install Ollama and pull a model with: 'ollama pull llama2'")

def image_examples():
    """Examples of image generation with different providers."""
    print("\n=== IMAGE GENERATION EXAMPLES ===")

    # OpenAI image generation
    try:
        image_url = apicenter.image(
            provider="openai",
            model="dall-e-3",
            prompt="A beautiful sunset over mountains"
        )
        print("\nOpenAI Image URL:")
        print(image_url)
    except Exception as e:
        print(f"\nError with OpenAI image: {e}")

def audio_examples():
    """Examples of audio generation with different providers."""
    print("\n=== AUDIO GENERATION EXAMPLES ===")

    # ElevenLabs audio generation
    try:
        audio_data = apicenter.audio(
            provider="elevenlabs",
            model="eleven_multilingual_v2",
            prompt="Hello! This is a test of text to speech."
        )
        print("\nElevenLabs Audio generated (bytes):", len(audio_data))
        
        # Example of saving audio to a file
        save_path = "output.mp3"
        if audio_data:
            with open(save_path, "wb") as f:
                f.write(audio_data)
            print(f"Audio saved to {save_path}")
    except Exception as e:
        print(f"\nError with ElevenLabs: {e}")

def main():
    """Basic examples of using APICenter with minimal parameters."""
    print("APICenter Basic Usage Examples")
    print("=============================")
    print("This demonstrates the minimal usage of each mode and provider.")
    
    # Run examples
    text_examples()
    image_examples()
    audio_examples()
    
    print("\nDone!")

if __name__ == "__main__":
    main() 