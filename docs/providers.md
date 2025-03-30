# Provider Reference

This document provides information about the various providers supported by APICenter, including their capabilities, models, and API specifics.

## Table of Contents

- [Text Generation Providers](#text-generation-providers)
  - [OpenAI](#openai)
  - [Anthropic](#anthropic)
  - [Ollama](#ollama)
- [Image Generation Providers](#image-generation-providers)
  - [OpenAI](#openai-1)
  - [Stability AI](#stability-ai)
- [Audio Generation Providers](#audio-generation-providers)
  - [ElevenLabs](#elevenlabs)

## Text Generation Providers

### OpenAI

OpenAI provides a range of GPT (Generative Pre-trained Transformer) models for natural language processing tasks.

#### Supported Models

- `gpt-4` and variants (`gpt-4-turbo`, `gpt-4-vision-preview`, etc.)
- `gpt-3.5-turbo` and variants
- `text-davinci-003` (legacy model)
- Numerous other specialized models

#### Authentication

Requires an API key and optionally an organization ID. These can be obtained from the [OpenAI platform](https://platform.openai.com/).

#### API Documentation

For the most up-to-date information, refer to the [OpenAI API Documentation](https://platform.openai.com/docs/api-reference).

#### Example

```python
from apicenter import apicenter

response = apicenter.text(
    provider="openai",
    model="gpt-4",
    prompt="Explain the concept of recursion in programming",
    temperature=0.7,
    max_tokens=300
)
```

### Anthropic

Anthropic's Claude models are designed to be helpful, harmless, and honest AI assistants.

#### Supported Models

- `claude-3-opus-20240229`
- `claude-3-sonnet-20240229`
- `claude-3-haiku-20240307`
- Other Claude models and variants

#### Authentication

Requires an API key from Anthropic, which can be obtained from the [Anthropic console](https://console.anthropic.com/).

#### API Documentation

For the most up-to-date information, refer to the [Anthropic API Documentation](https://docs.anthropic.com/claude/reference/getting-started-with-the-api).

#### Example

```python
from apicenter import apicenter

response = apicenter.text(
    provider="anthropic",
    model="claude-3-sonnet-20240229",
    prompt="What are the ethical considerations in artificial intelligence?",
    temperature=0.5,
    max_tokens=1000
)
```

### Ollama

Ollama allows running various large language models locally.

#### Supported Models

Any model that can be pulled into Ollama, including:
- `llama2`
- `mistral`
- `orca-mini`
- `codellama`
- `vicuna`
- `neural-chat`
- And many others

#### Setup

1. Install Ollama from [ollama.ai](https://ollama.ai/)
2. Pull your desired model: `ollama pull llama2`
3. Ensure the Ollama service is running

#### Environment Variables

- `OLLAMA_HOST`: The host address for Ollama (default: `http://localhost:11434`)

#### API Documentation

For the most up-to-date information, refer to the [Ollama GitHub repository](https://github.com/ollama/ollama).

#### Example

```python
from apicenter import apicenter

response = apicenter.text(
    provider="ollama",
    model="llama2",
    prompt="Generate a recursive function in Python to calculate Fibonacci numbers",
    temperature=0.7,
    num_predict=300
)
```

## Image Generation Providers

### OpenAI

OpenAI's DALL-E models generate images from text descriptions.

#### Supported Models

- `dall-e-3`
- `dall-e-2`

#### Authentication

Uses the same API key as OpenAI's text models.

#### API Documentation

For the most up-to-date information, refer to the [OpenAI Images API Documentation](https://platform.openai.com/docs/api-reference/images).

#### Example

```python
from apicenter import apicenter

image_url = apicenter.image(
    provider="openai",
    model="dall-e-3",
    prompt="A photorealistic image of a futuristic city with flying cars and vertical gardens",
    size="1024x1024",
    quality="hd",
    style="vivid"
)
```

### Stability AI

Stability AI provides state-of-the-art image generation models.

#### Supported Models

- `stable-diffusion-xl-1024-v1-0`
- `stable-diffusion-v1-6`
- Other Stability AI models

#### Authentication

Requires an API key from Stability AI, which can be obtained from the [Stability AI platform](https://platform.stability.ai/).

#### API Documentation

For the most up-to-date information, refer to the [Stability AI API Documentation](https://platform.stability.ai/docs/api/generation).

#### Example

```python
from apicenter import apicenter

image_bytes = apicenter.image(
    provider="stability",
    model="stable-diffusion-xl-1024-v1-0",
    prompt="An oil painting of a medieval castle on a hilltop at sunset",
    steps=50,
    cfg_scale=7.0,
    width=1024,
    height=1024
)

# Save image to file
with open("castle.png", "wb") as f:
    f.write(image_bytes)
```

## Audio Generation Providers

### ElevenLabs

ElevenLabs provides high-quality text-to-speech models with various voices.

#### Supported Models

- `eleven_multilingual_v2`
- `eleven_monolingual_v1`
- Other ElevenLabs models

#### Authentication

Requires an API key from ElevenLabs, which can be obtained from the [ElevenLabs website](https://elevenlabs.io/).

#### API Documentation

For the most up-to-date information, refer to the [ElevenLabs API Documentation](https://docs.elevenlabs.io/api-reference).

#### Example

```python
from apicenter import apicenter

audio_bytes = apicenter.audio(
    provider="elevenlabs",
    model="eleven_multilingual_v2",
    prompt="Hello world! This is a demonstration of text-to-speech technology.",
    voice_id="Adam",
    stability=0.5,
    similarity_boost=0.75
)

# Save audio to file
with open("speech.mp3", "wb") as f:
    f.write(audio_bytes)
```

## Adding New Providers

For information on adding new providers to APICenter, see the [Contributing Guide](../CONTRIBUTING.md). 