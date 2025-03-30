# APICenter API Reference

This document provides comprehensive details about APICenter's API interface, all available providers, supported parameters, and usage patterns.

## Core Interface

APICenter follows a simple, consistent pattern for all API calls:

```python
from apicenter import apicenter

response = apicenter.<mode>(
    provider="<provider_name>",
    model="<model_name>",
    prompt="<your_prompt>",
    **kwargs  # Additional provider-specific parameters
)
```

Where:
- `mode` is one of: `text`, `image`, or `audio`
- `provider` is the AI service provider (e.g., "openai", "anthropic", "stability")
- `model` is the specific model to use (varies by provider)
- `prompt` is the input text (or message list for chat models)
- `**kwargs` allows passing provider-specific parameters

## Text Generation

### Basic Usage

```python
response = apicenter.text(
    provider="openai",
    model="gpt-4",
    prompt="Explain quantum computing in simple terms"
)
```

### Available Providers

#### OpenAI

```python
response = apicenter.text(
    provider="openai",
    model="gpt-4",  # gpt-3.5-turbo, gpt-4-turbo, etc.
    prompt="Write a poem about mountains",
    temperature=0.7,
    max_tokens=500,
    top_p=1.0
)
```

**Supported Parameters:**
- `temperature`: Controls randomness (0.0-2.0)
- `max_tokens`: Maximum tokens to generate
- `top_p`: Nucleus sampling parameter
- `frequency_penalty`: Reduces repetition of token sequences
- `presence_penalty`: Encourages diversity
- `stop`: Sequences where the API will stop generating further tokens
- And any other parameters supported by OpenAI's Chat Completions API

#### Anthropic

```python
response = apicenter.text(
    provider="anthropic",
    model="claude-3-sonnet-20240229",  # or claude-3-opus-20240229, etc.
    prompt="Explain how photosynthesis works",
    temperature=0.5,
    max_tokens=1000
)
```

**Supported Parameters:**
- `temperature`: Controls randomness (0.0-1.0)
- `max_tokens`: Maximum tokens to generate
- `top_p`: Nucleus sampling parameter
- `top_k`: Limits token selection to top k options
- And any other parameters supported by Anthropic's API

#### Ollama (Local Models)

```python
response = apicenter.text(
    provider="ollama",
    model="llama2",  # or mistral, phi-2, etc.
    prompt="What is the capital of France?",
    temperature=0.8,
    num_predict=100
)
```

**Supported Parameters:**
- `temperature`: Controls randomness
- `num_predict`: Maximum tokens to generate
- `top_p`: Nucleus sampling parameter
- `top_k`: Limits token selection to top k options
- `stop`: Sequences where generation will stop
- And other parameters supported by Ollama

### Chat Conversations

For chat-based models, you can use message lists:

```python
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the distance to the Moon?"}
]

response = apicenter.text(
    provider="openai",
    model="gpt-4",
    prompt=messages
)
```

## Image Generation

### Basic Usage

```python
image_url = apicenter.image(
    provider="openai",
    model="dall-e-3",
    prompt="A serene mountain lake at sunset"
)
```

### Available Providers

#### OpenAI (DALL-E)

```python
image = apicenter.image(
    provider="openai",
    model="dall-e-3",  # or dall-e-2
    prompt="A beautiful sunset over mountains",
    size="1024x1024",  # 256x256, 512x512, 1024x1024, 1792x1024, 1024x1792
    quality="hd",  # "standard" or "hd"
    style="vivid",  # "vivid" or "natural"
    output_format="url"  # "url" (default), "png", or "jpeg"
)
```

**Supported Parameters:**
- `size`: Image dimensions
- `quality`: Image quality
- `style`: Image style
- `output_format`: Return format (URL or binary data)
- And other parameters supported by OpenAI's Image Generation API

#### Stability AI

```python
image = apicenter.image(
    provider="stability", 
    model="stable-diffusion-xl-1024-v1-0",
    prompt="A cyberpunk cityscape at night with neon lights",
    height=1024,
    width=1024,
    steps=30,
    cfg_scale=7.0,
    negative_prompt="blurry, ugly, deformed"
)
```

**Supported Parameters:**
- `height`: Image height
- `width`: Image width
- `steps`: Number of diffusion steps
- `cfg_scale`: How closely the image should follow the prompt
- `negative_prompt`: What to avoid in the image
- And other parameters supported by Stability AI's API

## Audio Generation

### Basic Usage

```python
audio_bytes = apicenter.audio(
    provider="elevenlabs",
    model="eleven_multilingual_v2",
    prompt="Hello, this is a text-to-speech test."
)
```

### Available Providers

#### ElevenLabs

```python
audio = apicenter.audio(
    provider="elevenlabs",
    model="eleven_multilingual_v2",
    prompt="Hello, this is a text-to-speech test.",
    voice_id="Adam",  # Voice ID from ElevenLabs
    stability=0.5,
    similarity_boost=0.8,
    output_format="mp3_44100_128"
)
```

**Supported Parameters:**
- `voice_id`: The voice to use
- `stability`: Voice stability (0.0-1.0)
- `similarity_boost`: Voice similarity boost (0.0-1.0)
- `output_format`: Audio format
- `style`: Voice style parameter
- `speed`: Speech speed
- And other parameters supported by ElevenLabs API

## Error Handling

APICenter provides standardized error handling:

```python
try:
    response = apicenter.text(
        provider="openai",
        model="gpt-4",
        prompt="Hello, world!"
    )
except ValueError as e:
    print(f"Error: {e}")
```

Common error scenarios:
- Missing or invalid API credentials
- Unsupported provider or model
- API rate limits
- Invalid parameters
- Network issues

## Credential Management

APICenter uses `credentials.json` for API keys. Place it in one of:
- Current working directory
- Project root directory
- User's home directory (`~/.apicenter/credentials.json`)
- System config directory (`~/.config/apicenter/credentials.json`)
- Custom path specified by `APICENTER_CREDENTIALS_PATH` environment variable

Example `credentials.json`:

```json
{
    "modes": {
        "text": {
            "providers": {
                "openai": {
                    "api_key": "your-openai-api-key",
                    "organization": "your-org-id"
                },
                "anthropic": {
                    "api_key": "your-anthropic-api-key"
                }
            }
        },
        "image": {
            "providers": {
                "openai": {
                    "api_key": "your-openai-api-key",
                    "organization": "your-org-id"
                },
                "stability": {
                    "api_key": "your-stability-api-key"
                }
            }
        },
        "audio": {
            "providers": {
                "elevenlabs": {
                    "api_key": "your-elevenlabs-api-key"
                }
            }
        }
    }
}
``` 