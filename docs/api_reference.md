# API Reference

This document provides detailed information about the APICenter API, including all public methods and their parameters.

## Core API

### apicenter

The `apicenter` object is the main entry point for all API functions.

```python
from apicenter import apicenter
```

## Universal Parameter Handling

One of APICenter's core features is universal parameter handling through `**kwargs`. This means you can pass any parameters supported by the underlying provider's API directly in your function call, and APICenter will handle the routing correctly.

Each provider implementation includes intelligent handling of parameters, including:

- **Automatic parameter routing**: Parameters are routed to their correct destination (e.g., stability parameters for ElevenLabs, options dictionary for Ollama)
- **Default values**: Sensible defaults are provided for required parameters
- **Provider-specific structures**: Parameters are converted to the structure expected by each provider

This flexibility means you don't need to learn different parameter structures for each provider - simply pass parameters according to the provider's API documentation, and APICenter takes care of the rest.

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

### Improved System Prompt Support

APICenter now provides universal support for system prompts across all text providers, allowing you to use the same messaging format regardless of which provider you're using.

When you provide a list of message dictionaries with a "system" role message, APICenter will:

- For OpenAI: Pass the system message directly as part of the messages list
- For Anthropic: Extract the system message and pass it as a separate `system` parameter
- For Ollama: Properly handle the system message based on model capabilities

This means you can write code like this and it will work with any provider:

```python
response = apicenter.text(
    provider="any_provider",  # openai, anthropic, ollama, etc.
    model="model_name",
    prompt=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Your question here"}
    ]
)
```

### Supported Providers

| Provider | Example Models | Description |
|----------|--------|-------------|
| `openai` | gpt-4, gpt-3.5-turbo | OpenAI's GPT models |
| `anthropic` | claude-3-opus, claude-3-sonnet | Anthropic's Claude models |
| `ollama` | llama2, mistral | Local models via Ollama |

APICenter supports the latest models from each provider. As providers release new models, you can simply specify the new model name without waiting for an APICenter update.

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

### Provider-Specific Message Formats

APICenter is designed to handle different message formats properly for each provider:

#### OpenAI

With OpenAI, you can use the standard format with "system", "user", and "assistant" roles:

```python
response = apicenter.text(
    provider="openai",
    model="gpt-4",
    prompt=[
        {"role": "system", "content": "You are a helpful assistant specialized in science."},
        {"role": "user", "content": "Explain black holes."},
        {"role": "assistant", "content": "Black holes are regions of spacetime..."},
        {"role": "user", "content": "What happens if you fall into one?"}
    ]
)
```

#### Anthropic

For Anthropic models, system prompts are automatically extracted and handled correctly:

```python
response = apicenter.text(
    provider="anthropic",
    model="claude-3-sonnet-20240229",
    prompt=[
        {"role": "system", "content": "You are a helpful assistant that explains complex topics simply."},
        {"role": "user", "content": "Explain quantum computing to me like I'm 10 years old."}
    ],
    temperature=0.3,
    max_tokens=800
)
```

#### Ollama

For Ollama local models, you can use a simplified format:

```python
response = apicenter.text(
    provider="ollama",
    model="llama2",
    prompt=[
        {"role": "user", "content": "What are the three laws of robotics?"},
        {"role": "assistant", "content": "The three laws are..."},
        {"role": "user", "content": "Who created these laws?"}
    ]
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

| Provider | Example Models | Return Type | Description |
|----------|--------|-------------|-------------|
| `openai` | dall-e-3, dall-e-2 | URL string | OpenAI's DALL-E models |
| `stability` | stable-diffusion-xl-1024-v1-0 | Image bytes | Stability AI's models |

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
    cfg_scale=7.0,
    negative_prompt="ugly, blurry, low quality"
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

| Provider | Example Models | Description |
|----------|--------|-------------|
| `elevenlabs` | eleven_multilingual_v2 | ElevenLabs' text-to-speech models |

### Examples

```python
# Generate speech with ElevenLabs
audio_bytes = apicenter.audio(
    provider="elevenlabs",
    model="eleven_multilingual_v2",
    prompt="Hello world! This is a text-to-speech demonstration.",
    voice_id="Rachel",
    stability=0.5,  # Voice settings parameter
    similarity_boost=0.75,  # Voice settings parameter
    output_format="mp3_44100_128"
)

# Save audio to file
with open("speech.mp3", "wb") as f:
    f.write(audio_bytes)
```

## Common Provider-Specific Parameters

APICenter is designed to be flexible, allowing you to pass any parameters supported by the underlying APIs. Below are some common parameters for each provider, but you can use any parameters documented in the provider's official API documentation.

### OpenAI Text Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `temperature` | `float` | Controls randomness (0.0-2.0) |
| `max_tokens` | `int` | Maximum tokens to generate |
| `top_p` | `float` | Nucleus sampling parameter (0.0-1.0) |

### OpenAI Image Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `size` | `str` | Image size ("256x256", "512x512", "1024x1024", etc.) |
| `quality` | `str` | Image quality ("standard", "hd") |
| `style` | `str` | Image style ("vivid", "natural") |

### Anthropic Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `max_tokens` | `int` | Maximum tokens to generate |
| `temperature` | `float` | Controls randomness (0.0-1.0) |
| `top_p` | `float` | Nucleus sampling parameter (0.0-1.0) |

### Ollama Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `temperature` | `float` | Controls randomness (0.0-1.0) |
| `num_predict` | `int` | Maximum tokens to generate |
| `top_p` | `float` | Nucleus sampling parameter (0.0-1.0) |

### Stability AI Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `steps` | `int` | Number of diffusion steps (10-150) |
| `cfg_scale` | `float` | How closely to follow the prompt (0-35) |
| `width` | `int` | Image width (multiple of 64) |
| `height` | `int` | Image height (multiple of 64) |
| `negative_prompt` | `str` | Text prompts to avoid in the generation |

### ElevenLabs Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `voice_id` | `str` | Voice to use |
| `stability` | `float` | Voice stability (0.0-1.0) |
| `similarity_boost` | `float` | Voice similarity boost (0.0-1.0) |
| `output_format` | `str` | Audio format (e.g., "mp3_44100_128") |

The flexibility of APICenter's design means you can pass any parameter supported by the underlying provider's API without needing to update the library. For a complete list of available parameters for each provider, refer to their official API documentation. 