from google.cloud import texttospeech


def call_google(model, prompt, credentials, **kwargs):
    """Google Cloud Text-to-Speech provider implementation."""
    try:
        client = texttospeech.TextToSpeechClient()

        # Default parameters if not provided in kwargs
        language = kwargs.pop("language_code", "en-US")
        voice_gender = kwargs.pop("voice_gender", texttospeech.SsmlVoiceGender.NEUTRAL)
        audio_encoding = kwargs.pop("audio_encoding", texttospeech.AudioEncoding.MP3)

        # Construct the synthesis input
        synthesis_input = texttospeech.SynthesisInput(text=prompt)

        # Build the voice parameters
        voice = texttospeech.VoiceSelectionParams(
            language_code=language,
            name=model,  # e.g., "en-US-Neural2-A"
            ssml_gender=voice_gender,
        )

        # Select the audio file type
        audio_config = texttospeech.AudioConfig(audio_encoding=audio_encoding, **kwargs)

        # Perform the text-to-speech request
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        return response.audio_content
    except Exception as e:
        return f"Error generating audio: {str(e)}"
