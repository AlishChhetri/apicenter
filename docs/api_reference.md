# API Reference

This document provides detailed information about the APICenter API, including all public methods and their parameters.

## Core API

### apicenter

The `apicenter` object is the main entry point for all API functions.

```python
from apicenter import apicenter
```

## Text Generation

Generate text with AI models from various providers.

```python
apicenter.text(
    provider: str,          # AI service provider name
    model: str,             # Model name
    prompt: Union[str, List[Dict[str, str]]],  # Text prompt or message list
    **kwargs: Any           # Provider-specific parameters
) -> str                    # Returns generated text
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `provider` | `str` | The AI service provider (e.g., "openai", "anthropic", "ollama") |
| `model` | `str` | The specific model to use (e.g., "gpt-4", "claude-3-sonnet-20240229") |
| `prompt` | `str` or `List[Dict[str, str]]` | Either a string prompt or a list of message dictionaries |
| `**kwargs` | Any | Additional provider-specific parameters |

### Supported Providers

| Provider | Models | Description |
|----------|--------|-------------|
| `openai` | gpt-4, gpt-3.5-turbo, etc. | OpenAI's GPT models |
| `anthropic` | claude-3-opus, claude-3-sonnet, etc. | Anthropic's Claude models |
| `ollama` | llama2, mistral, etc. | Local models via Ollama |

### Examples

```python
# Simple text prompt
response = apicenter.text(
    provider="openai",
    model="gpt-4",
    prompt="Explain how quantum computing works in simple terms."
)

# Chat message format
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the distance between Earth and Mars?"}
]
response = apicenter.text(
    provider="anthropic",
    model="claude-3-sonnet-20240229",
    prompt=messages
)

# Local model with Ollama
response = apicenter.text(
    provider="ollama",
    model="llama2",
    prompt="Write a poem about artificial intelligence.",
    temperature=0.7
)
```

## Image Generation

Generate images with AI models from various providers.

```python
apicenter.image(
    provider: str,        # AI service provider name
    model: str,           # Model name
    prompt: str,          # Text description of the image to generate
    **kwargs: Any         # Provider-specific parameters
) -> Union[str, bytes, List[str]]  # Returns URL(s) or image bytes
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `provider` | `str` | The AI service provider (e.g., "openai", "stability") |
| `model` | `str` | The specific model to use (e.g., "dall-e-3") |
| `prompt` | `str` | Text description of the image to generate |
| `**kwargs` | Any | Additional provider-specific parameters |

### Return Value

The return type varies depending on the provider:
- OpenAI: Returns a URL string (or list of URL strings)
- Stability AI: Returns image bytes

### Supported Providers

| Provider | Models | Return Type | Description |
|----------|--------|-------------|-------------|
| `openai` | dall-e-3, dall-e-2 | URL string | OpenAI's DALL-E models |
| `stability` | stable-diffusion-xl-1024-v1-0, etc. | Image bytes | Stability AI's models |

### Examples

```python
# OpenAI DALL-E (returns URL)
image_url = apicenter.image(
    provider="openai",
    model="dall-e-3",
    prompt="A photorealistic image of a futuristic city with flying cars",
    size="1024x1024",
    quality="hd"
)

# Download and save the image
import requests
response = requests.get(image_url)
with open("city_image.png", "wb") as f:
    f.write(response.content)

# Stability AI (returns bytes directly)
image_bytes = apicenter.image(
    provider="stability",
    model="stable-diffusion-xl-1024-v1-0",
    prompt="A fantasy landscape with dragons and castles",
    steps=50,
    cfg_scale=7.0
)

with open("fantasy_landscape.png", "wb") as f:
    f.write(image_bytes)
```

## Audio Generation

Generate audio (text-to-speech) with AI models.

```python
apicenter.audio(
    provider: str,        # AI service provider name
    model: str,           # Model name
    prompt: str,          # Text to convert to speech
    **kwargs: Any         # Provider-specific parameters
) -> bytes               # Returns audio data as bytes
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `provider` | `str` | The AI service provider (e.g., "elevenlabs") |
| `model` | `str` | The specific model to use (e.g., "eleven_multilingual_v2") |
| `prompt` | `str` | Text to convert to speech |
| `**kwargs` | Any | Additional provider-specific parameters |

### Supported Providers

| Provider | Models | Description |
|----------|--------|-------------|
| `elevenlabs` | eleven_multilingual_v2, etc. | ElevenLabs' text-to-speech models |

### Examples

```python
# Generate speech with ElevenLabs
audio_bytes = apicenter.audio(
    provider="elevenlabs",
    model="eleven_multilingual_v2",
    prompt="Hello world! This is a text-to-speech demonstration.",
    voice_id="Rachel",
    stability=0.5,
    similarity_boost=0.75
)

# Save audio to file
with open("speech.mp3", "wb") as f:
    f.write(audio_bytes)
```

## Common Provider-Specific Parameters

### OpenAI Text Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `temperature` | `float` | Controls randomness (0.0-2.0) |
| `max_tokens` | `int` | Maximum tokens to generate |
| `top_p` | `float` | Nucleus sampling parameter (0.0-1.0) |
| `frequency_penalty` | `float` | Reduces repetition of tokens (-2.0 to 2.0) |
| `presence_penalty` | `float` | Reduces repetition of topics (-2.0 to 2.0) |
| `stop` | `List[str]` | Sequences where the API will stop generating |

### OpenAI Image Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `size` | `str` | Image size ("256x256", "512x512", "1024x1024", "1024x1792", "1792x1024") |
| `quality` | `str` | Image quality ("standard", "hd") |
| `style` | `str` | Image style ("vivid", "natural") |
| `n` | `int` | Number of images to generate |

### Anthropic Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `max_tokens` | `int` | Maximum tokens to generate |
| `temperature` | `float` | Controls randomness (0.0-1.0) |
| `top_p` | `float` | Nucleus sampling parameter (0.0-1.0) |
| `top_k` | `int` | Limits vocabulary to top K options |

### Ollama Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `temperature` | `float` | Controls randomness (0.0-1.0) |
| `num_predict` | `int` | Maximum tokens to generate |
| `top_p` | `float` | Nucleus sampling parameter (0.0-1.0) |
| `top_k` | `int` | Limits vocabulary to top K options |
| `repeat_penalty` | `float` | Penalty for repeated tokens |

### Stability AI Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `steps` | `int` | Number of diffusion steps (10-150) |
| `cfg_scale` | `float` | How closely to follow the prompt (0-35) |
| `width` | `int` | Image width (multiple of 64) |
| `height` | `int` | Image height (multiple of 64) |
| `samples` | `int` | Number of images to generate |
| `seed` | `int` | Random seed for reproducibility |

### ElevenLabs Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `voice_id` | `str` | Voice to use |
| `stability` | `float` | Voice stability (0.0-1.0) |
| `similarity_boost` | `float` | Voice similarity boost (0.0-1.0) |
| `style` | `float` | Speaking style (0.0-1.0) |
| `output_format` | `str` | Audio format ("mp3_44100_128", etc.) |

For a complete list of available parameters for each provider, refer to the provider's official API documentation. 