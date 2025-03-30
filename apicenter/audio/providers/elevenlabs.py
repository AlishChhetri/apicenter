from elevenlabs.client import ElevenLabs
from elevenlabs.types import VoiceSettings
from typing import Dict, Any


def call_elevenlabs(model: str, prompt: str, credentials: Dict[str, Any], **kwargs: Any) -> bytes:
    """ElevenLabs provider implementation.
    
    Args:
        model: The model to use (e.g., 'eleven_multilingual_v2')
        prompt: The text to convert to speech
        credentials: API credentials dictionary containing api_key
        **kwargs: Additional parameters for the ElevenLabs API
        
    Returns:
        Generated audio as bytes
        
    Raises:
        ValueError: If there's an error with the API call
    """
    try:
        # Create client with API key
        client = ElevenLabs(**credentials)

        # Default parameters if not provided in kwargs
        kwargs.setdefault("voice_id", "JBFqnCBsd6RMkjVDRZzb")  # Default voice
        kwargs.setdefault("output_format", "mp3_44100_128")    # Default format
        
        # Extract parameters for the convert method vs. voice_settings
        text_to_speech_params = {}
        voice_settings_params = {}
        
        # Parameters for VoiceSettings object
        voice_settings_fields = ["stability", "similarity_boost", "style", "use_speaker_boost", "speed"]
        
        # Extract voice settings parameters if any
        for field in voice_settings_fields:
            if field in kwargs:
                voice_settings_params[field] = kwargs.pop(field)
                
        # Create voice_settings object if we have any parameters
        if voice_settings_params:
            voice_settings = VoiceSettings(**voice_settings_params)
            text_to_speech_params["voice_settings"] = voice_settings
            
        # Other valid parameters for the convert method
        valid_params = [
            "voice_id", "output_format", "model_id", "optimize_streaming_latency", 
            "enable_logging", "language_code", "seed", "previous_text", "next_text", 
            "previous_request_ids", "next_request_ids", "use_pvc_as_ivc", 
            "apply_text_normalization", "apply_language_text_normalization"
        ]
        
        # Extract parameters for convert method
        for param in valid_params:
            if param in kwargs:
                text_to_speech_params[param] = kwargs.pop(param)
        
        # Handle model_id (API expects model_id, but we use model for consistency)
        text_to_speech_params.setdefault("model_id", model)
                
        # Get the generator object and convert to bytes automatically
        audio_generator = client.text_to_speech.convert(
            text=prompt,
            **text_to_speech_params
        )
        
        return b"".join(audio_generator)
    except Exception as e:
        raise ValueError(f"ElevenLabs audio generation error: {str(e)}")
