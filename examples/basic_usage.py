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

def audio_examples():
    """Examples of audio generation using ElevenLabs."""
    # ElevenLabs example
    audio = apicenter.audio(
        provider="elevenlabs",
        model="eleven_multilingual_v2",
        prompt="Hello! This is a test of text to speech.",
        voice_id="21m00Tcm4TlvDq8ikWAM",  # Default voice
        stability=0.5,
        similarity_boost=0.75
    )
    print("Audio generated successfully!")

def main():
    """Run all examples."""
    print("Running text examples...")
    text_examples()
    
    print("\nRunning image examples...")
    image_examples()
    
    print("\nRunning audio examples...")
    audio_examples()

if __name__ == "__main__":
    main() 