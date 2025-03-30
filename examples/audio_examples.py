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

# Create examples/outputs directory if it doesn't exist
OUTPUTS_DIR = Path(__file__).parent / "outputs"
OUTPUTS_DIR.mkdir(exist_ok=True)

def audio_examples():
    """Examples of audio generation using ElevenLabs."""
    # ElevenLabs example
    try:
        audio = apicenter.audio(
            provider="elevenlabs",
            model="eleven_multilingual_v2",
            prompt="Hello! This is a test of text to speech.",
            voice_id="21m00Tcm4TlvDq8ikWAM",  # Default voice
            stability=0.5,
            similarity_boost=0.75
        )
        print("Audio generated successfully!")
        print(f"Generated audio bytes: {len(audio) if audio else 0}")
        
        # Save the audio to a file
        if audio:
            with open(OUTPUTS_DIR / "elevenlabs_voice.mp3", "wb") as f:
                f.write(audio)
            print(f"Audio saved to {OUTPUTS_DIR}/elevenlabs_voice.mp3")
    except Exception as e:
        print(f"Error with ElevenLabs: {e}")

def main():
    """Run all examples."""
    
    print("\nRunning audio examples...")
    print(f"All outputs will be saved to the '{OUTPUTS_DIR}' directory.")
    audio_examples()

if __name__ == "__main__":
    main() 