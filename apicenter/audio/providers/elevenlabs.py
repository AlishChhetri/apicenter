from elevenlabs.client import ElevenLabs
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

        # Get the generator object and convert to bytes automatically
        audio_generator = client.text_to_speech.convert(
            text=prompt, 
            model_id=model, 
            **kwargs
        )
        
        return b"".join(audio_generator)
    except Exception as e:
        raise ValueError(f"ElevenLabs audio generation error: {str(e)}")
