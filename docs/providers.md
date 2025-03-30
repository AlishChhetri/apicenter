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
- [Input and Output Formats](#input-and-output-formats)

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

# Simple string input
response = apicenter.text(
    provider="openai",
    model="gpt-4",
    prompt="Explain the concept of recursion in programming",
    temperature=0.7,
    max_tokens=300
)

# Chat message list input
response = apicenter.text(
    provider="openai",
    model="gpt-4",
    prompt=[
        {"role": "system", "content": "You are a programming tutor."},
        {"role": "user", "content": "Explain the concept of recursion in programming"}
    ],
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

# Simple string input
response = apicenter.text(
    provider="anthropic",
    model="claude-3-sonnet-20240229",
    prompt="What are the ethical considerations in artificial intelligence?",
    temperature=0.5,
    max_tokens=1000
)

# Chat message list input
response = apicenter.text(
    provider="anthropic",
    model="claude-3-sonnet-20240229",
    prompt=[
        {"role": "system", "content": "You are an ethics professor."},
        {"role": "user", "content": "What are the ethical considerations in artificial intelligence?"}
    ],
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

# Simple string input
response = apicenter.text(
    provider="ollama",
    model="llama2",
    prompt="Generate a recursive function in Python to calculate Fibonacci numbers",
    temperature=0.7,
    num_predict=300
)

# Chat message list input
response = apicenter.text(
    provider="ollama",
    model="llama2",
    prompt=[
        {"role": "system", "content": "You are a programming expert."},
        {"role": "user", "content": "Generate a recursive function in Python to calculate Fibonacci numbers"}
    ],
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

#### Return Format

The OpenAI DALL-E provider returns a single URL string pointing to the generated image.

#### API Documentation

For the most up-to-date information, refer to the [OpenAI Images API Documentation](https://platform.openai.com/docs/api-reference/images).

#### Example

```python
from apicenter import apicenter
import requests

# Generate image (returns a URL string)
image_url = apicenter.image(
    provider="openai",
    model="dall-e-3",
    prompt="A photorealistic image of a futuristic city with flying cars and vertical gardens",
    size="1024x1024",
    quality="hd",
    style="vivid"
)

# Download the image
response = requests.get(image_url)
with open("future_city.png", "wb") as f:
    f.write(response.content)
```

### Stability AI

Stability AI provides state-of-the-art image generation models.

#### Supported Models

- `stable-diffusion-xl-1024-v1-0`
- `stable-diffusion-v1-6`
- Other Stability AI models

#### Authentication

Requires an API key from Stability AI, which can be obtained from the [Stability AI platform](https://platform.stability.ai/).

#### Return Format

The Stability AI provider returns image data as bytes directly, ready to be saved to a file.

#### API Documentation

For the most up-to-date information, refer to the [Stability AI API Documentation](https://platform.stability.ai/docs/api/generation).

#### Example

```python
from apicenter import apicenter

# Generate image (returns image bytes directly)
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

#### Return Format

The ElevenLabs provider returns audio data as bytes, which can be saved directly to an audio file.

#### API Documentation

For the most up-to-date information, refer to the [ElevenLabs API Documentation](https://docs.elevenlabs.io/api-reference).

#### Example

```python
from apicenter import apicenter

# Generate audio (returns audio bytes)
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

## Input and Output Formats

### Input Formats

APICenter provides a flexible interface for different types of input formats:

- **Text Generation**:
  - String prompts: Simple text queries (`"Tell me about quantum physics"`)
  - Message lists: Structured chat conversations with roles (`[{"role": "system", "content": "..."}, ...]`)

- **Image Generation**:
  - String prompts: Text descriptions of the desired image (`"A cat wearing a space suit"`)

- **Audio Generation**:
  - String prompts: Text to be converted to speech (`"Hello, this is a test"`)

### Output Formats

Each provider returns a specific output format:

- **Text Generation**: All text providers return a string containing the generated text.
- **Image Generation**:
  - OpenAI: Returns a single URL string pointing to the generated image.
  - Stability AI: Returns the image data as bytes directly.
- **Audio Generation**:
  - ElevenLabs: Returns the audio data as bytes.

## Adding New Providers

For information on adding new providers to APICenter, see the [Contributing Guide](../CONTRIBUTING.md). 