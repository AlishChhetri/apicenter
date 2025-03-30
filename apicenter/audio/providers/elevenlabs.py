"""ElevenLabs text-to-speech provider implementation."""

from elevenlabs.client import ElevenLabs
from elevenlabs.types import VoiceSettings
from typing import Dict, Any, List, Optional


def call_elevenlabs(model: str, prompt: str, credentials: Dict[str, Any], **kwargs: Any) -> bytes:
    """Handle text-to-speech conversion through ElevenLabs API."""
    try:
        # Initialize ElevenLabs client with credentials
        client = ElevenLabs(**credentials)

        # Set default parameters if not provided
        kwargs.setdefault("voice_id", "JBFqnCBsd6RMkjVDRZzb")  # Default voice
        kwargs.setdefault("output_format", "mp3_44100_128")  # Default format

        # Separate parameters by destination
        text_to_speech_params = {}
        voice_settings_params = {}

        # List of parameters for VoiceSettings object
        voice_settings_fields = [
            "stability",
            "similarity_boost",
            "style",
            "use_speaker_boost",
            "speed",
        ]

        # Extract voice settings parameters
        for field in voice_settings_fields:
            if field in kwargs:
                voice_settings_params[field] = kwargs.pop(field)

        # Create VoiceSettings object if parameters were provided
        if voice_settings_params:
            voice_settings = VoiceSettings(**voice_settings_params)
            text_to_speech_params["voice_settings"] = voice_settings

        # List of valid parameters for the convert method
        valid_params = [
            "voice_id",
            "output_format",
            "model_id",
            "optimize_streaming_latency",
            "enable_logging",
            "language_code",
            "seed",
            "previous_text",
            "next_text",
            "previous_request_ids",
            "next_request_ids",
            "use_pvc_as_ivc",
            "apply_text_normalization",
            "apply_language_text_normalization",
        ]

        # Extract API-specific parameters
        for param in valid_params:
            if param in kwargs:
                text_to_speech_params[param] = kwargs.pop(param)

        # Set model ID - the API expects model_id but we use model for consistency
        text_to_speech_params.setdefault("model_id", model)

        # Generate audio from text
        audio_generator = client.text_to_speech.convert(text=prompt, **text_to_speech_params)

        # Concatenate all audio chunks and return as bytes
        return b"".join(audio_generator)
    except Exception as e:
        raise ValueError(f"ElevenLabs audio generation error: {str(e)}")
