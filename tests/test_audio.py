import sys
import os
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from apicenter.apicenter import apicenter

def test_elevenlabs_minimal():
    """Test ElevenLabs with minimal parameters."""
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Minimal parameters
    response = apicenter.audio(
        provider="elevenlabs",
        model="eleven_multilingual_v2",
        prompt="Hello, this is a test with minimal parameters.",
    )
    
    if isinstance(response, bytes):
        output_path = output_dir / "elevenlabs_minimal.mp3"
        with open(output_path, "wb") as f:
            f.write(response)
        print(f"ElevenLabs audio (minimal) saved as: {output_path}")
    else:
        print("ElevenLabs Error:", response)

def test_elevenlabs_detailed():
    """Test ElevenLabs with additional parameters."""
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Detailed parameters
    response = apicenter.audio(
        provider="elevenlabs",
        model="eleven_multilingual_v2",
        prompt="This is a test with additional parameters.",
        voice_id="JBFqnCBsd6RMkjVDRZzb",
        output_format="mp3_44100_128",
        stability=0.5,
        similarity_boost=0.8
    )
    
    if isinstance(response, bytes):
        output_path = output_dir / "elevenlabs_detailed.mp3"
        with open(output_path, "wb") as f:
            f.write(response)
        print(f"ElevenLabs audio (detailed) saved as: {output_path}")
    else:
        print("ElevenLabs Error:", response)

def test_google_minimal():
    """Test Google TTS with minimal parameters."""
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Minimal parameters
    response = apicenter.audio(
        provider="google",
        model="en-US-Neural2-A",
        prompt="Hello, this is a test of Google Text-to-Speech.",
    )
    
    if isinstance(response, bytes):
        output_path = output_dir / "google_minimal.mp3"
        with open(output_path, "wb") as f:
            f.write(response)
        print(f"Google TTS audio (minimal) saved as: {output_path}")
    else:
        print("Google TTS Error:", response)

def test_google_detailed():
    """Test Google TTS with additional parameters."""
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    from google.cloud import texttospeech
    
    # Detailed parameters
    response = apicenter.audio(
        provider="google",
        model="en-US-Neural2-A",
        prompt="This is a test with additional parameters.",
        language_code="en-US",
        voice_gender=texttospeech.SsmlVoiceGender.FEMALE,
        speaking_rate=1.1,
        pitch=0,
        volume_gain_db=0.0
    )
    
    if isinstance(response, bytes):
        output_path = output_dir / "google_detailed.mp3"
        with open(output_path, "wb") as f:
            f.write(response)
        print(f"Google TTS audio (detailed) saved as: {output_path}")
    else:
        print("Google TTS Error:", response)

def main():
    """Main function to test audio generation providers."""
    # print("\nTesting ElevenLabs (Minimal):")
    # test_elevenlabs_minimal()
    
    # print("\nTesting ElevenLabs (Detailed):")
    # test_elevenlabs_detailed()

    print("\nTesting Google TTS (Minimal):")
    test_google_minimal()
    
    # print("\nTesting Google TTS (Detailed):")
    # test_google_detailed()

if __name__ == "__main__":
    main()