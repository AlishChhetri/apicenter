from typing import Any
from elevenlabs import client
from ..core.base import BaseProvider

class AudioProvider(BaseProvider[bytes]):
    """Provider for audio generation using ElevenLabs."""
    
    def _get_mode(self) -> str:
        return "audio"
    
    def validate_params(self) -> None:
        """Validate the provider-specific parameters."""
        if self.provider != "elevenlabs":
            raise ValueError(f"Unsupported audio provider: {self.provider}")
        if not self.model.startswith(("eleven_", "eleven_multilingual_")):
            raise ValueError(f"Invalid ElevenLabs model: {self.model}")
    
    def call(self) -> bytes:
        """Make the API call and return the response."""
        api_client = client.Client(api_key=self.config.api_key)
        
        # Get available voices
        voices = api_client.voices.get_all()
        voice = next(
            (v for v in voices if v.voice_id == self.kwargs.get("voice_id", "21m00Tcm4TlvDq8ikWAM")),
            voices[0]  # Default to first voice if specified voice not found
        )
        
        # Generate audio
        audio = api_client.generate(
            text=self.prompt,
            voice=voice,
            model=self.model
        )
        
        return audio


def audio(provider, model, prompt, **kwargs):
    """Universal function to generate audio from text with minimal input."""
    return AudioProvider(provider, model, prompt, **kwargs).get_response()