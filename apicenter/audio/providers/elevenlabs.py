from elevenlabs.client import ElevenLabs


def call_elevenlabs(model, prompt, credentials, **kwargs):
    """ElevenLabs provider implementation."""
    client = ElevenLabs(**credentials)

    # Default parameters if not provided in kwargs
    kwargs.setdefault("voice_id", "JBFqnCBsd6RMkjVDRZzb")
    kwargs.setdefault("output_format", "mp3_44100_128")

    # Get the generator object and convert to bytes automatically
    try:
        audio_generator = client.text_to_speech.convert(
            text=prompt, 
            model_id=model, 
            **kwargs
        )
        return b"".join(audio_generator)
    except Exception as e:
        return f"Error generating audio: {str(e)}"
