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
    
    print("\nRunning audio examples...")
    audio_examples()

if __name__ == "__main__":
    main() 