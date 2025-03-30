# Models Reference

This document provides information about the various AI models supported by different providers in APICenter.

## Table of Contents

- [Models Reference](#models-reference)
  - [Table of Contents](#table-of-contents)
  - [Text Generation Models](#text-generation-models)
    - [OpenAI Models](#openai-models)
      - [Example](#example)
    - [Anthropic Models](#anthropic-models)
      - [Example](#example-1)
    - [Ollama Models](#ollama-models)
      - [Example](#example-2)
  - [Image Generation Models](#image-generation-models)
    - [OpenAI DALL-E Models](#openai-dall-e-models)
      - [Example](#example-3)
    - [Stability AI Models](#stability-ai-models)
      - [Example](#example-4)
  - [Audio Generation Models](#audio-generation-models)
    - [ElevenLabs Models](#elevenlabs-models)
      - [Example](#example-5)
  - [Model Selection Guidelines](#model-selection-guidelines)

## Text Generation Models

### OpenAI Models

| Model | Description | Context Window | Strengths |
|-------|-------------|----------------|-----------|
| `gpt-4` | Most capable GPT-4 model | 8,192 tokens | Advanced reasoning, complex tasks |
| `gpt-4-turbo` | Faster version of GPT-4 | 128,000 tokens | Faster, longer context |
| `gpt-4-vision-preview` | GPT-4 with vision capability | 128,000 tokens | Image understanding |
| `gpt-3.5-turbo` | Fast and cost-effective | 16,385 tokens | Good balance of capabilities and cost |

For the most up-to-date list, see the [OpenAI Models documentation](https://platform.openai.com/docs/models).

#### Example

```python
from apicenter import apicenter

# Using GPT-4
response = apicenter.text(
    provider="openai",
    model="gpt-4",
    prompt="Explain how quantum computing differs from classical computing"
)

# Using GPT-3.5 Turbo
response = apicenter.text(
    provider="openai",
    model="gpt-3.5-turbo",
    prompt="Write a short poem about technology"
)
```

### Anthropic Models

| Model | Description | Context Window | Strengths |
|-------|-------------|----------------|-----------|
| `claude-3-opus-20240229` | Most powerful Claude model | 200K tokens | Highest accuracy, complex reasoning |
| `claude-3-sonnet-20240229` | Balanced performance and cost | 200K tokens | Good balance of capabilities and cost |
| `claude-3-haiku-20240307` | Fastest, most compact model | 200K tokens | Quick responses, lower cost |
| `claude-2.1` | Previous generation | 200K tokens | Legacy support |

For the most up-to-date list, see the [Anthropic models documentation](https://docs.anthropic.com/claude/docs/models-overview).

#### Example

```python
from apicenter import apicenter

# Using Claude 3 Opus
response = apicenter.text(
    provider="anthropic",
    model="claude-3-opus-20240229",
    prompt="Analyze the ethical implications of artificial general intelligence"
)

# Using Claude 3 Haiku
response = apicenter.text(
    provider="anthropic",
    model="claude-3-haiku-20240307",
    prompt="Summarize the benefits of renewable energy"
)
```

### Ollama Models

Ollama supports a wide range of open-source models. Here are some of the more popular ones:

| Model | Description | Strengths | Typical Size |
|-------|-------------|-----------|--------------|
| `llama2` | Meta's Llama 2 model | General purpose, good reasoning | 7B-70B parameters |
| `llama3` | Meta's Llama 3 model | Improved over Llama 2 | 8B-70B parameters |
| `mistral` | Mistral AI's model | Strong performance for size | 7B parameters |
| `codellama` | Code-specialized variant | Code generation, understanding | 7B-34B parameters |
| `orca-mini` | Smaller, optimized model | Fast, efficient | 3B parameters |
| `vicuna` | Fine-tuned LLaMA model | Conversation, instruction following | 7B-13B parameters |
| `wizardcoder` | Code-specialized model | Programming tasks | 7B-34B parameters |
| `mpt` | MosaicML's model | General purpose | 7B-30B parameters |

For a complete list of available models, run `ollama list` after installing Ollama.

#### Example

```python
from apicenter import apicenter

# Using Llama 2
response = apicenter.text(
    provider="ollama",
    model="llama2",
    prompt="Write a function in Python to find the greatest common divisor of two numbers"
)

# Using Mistral
response = apicenter.text(
    provider="ollama",
    model="mistral",
    prompt="Explain the concept of recursion"
)
```

## Image Generation Models

### OpenAI DALL-E Models

| Model | Description | Resolution Options | Features |
|-------|-------------|-------------------|----------|
| `dall-e-3` | Latest DALL-E model | 1024x1024, 1024x1792, 1792x1024 | High quality, detailed images |
| `dall-e-2` | Previous generation | 256x256, 512x512, 1024x1024 | Wider availability, faster |

For the most up-to-date information, see the [OpenAI DALL-E documentation](https://platform.openai.com/docs/guides/images).

#### Example

```python
from apicenter import apicenter

# Using DALL-E 3
image_url = apicenter.image(
    provider="openai",
    model="dall-e-3",
    prompt="A hyperrealistic photograph of a futuristic city with flying cars and neon lights",
    size="1024x1024",
    quality="hd"
)
```

### Stability AI Models

| Model | Description | Features |
|-------|-------------|----------|
| `stable-diffusion-xl-1024-v1-0` | Stable Diffusion XL | High quality, detailed images |
| `stable-diffusion-v1-6` | Stable Diffusion 1.6 | Fast, efficient |
| `stable-diffusion-512-v2-1` | Lower resolution model | More efficient, faster |

For the most up-to-date information, see the [Stability AI documentation](https://platform.stability.ai/docs/api/generation).

#### Example

```python
from apicenter import apicenter

# Using Stable Diffusion XL
image_bytes = apicenter.image(
    provider="stability",
    model="stable-diffusion-xl-1024-v1-0",
    prompt="A detailed oil painting of an ancient forest with mythical creatures",
    steps=50,
    cfg_scale=7.0
)
```

## Audio Generation Models

### ElevenLabs Models

| Model | Description | Features |
|-------|-------------|----------|
| `eleven_multilingual_v2` | Latest multilingual model | Multiple languages, high quality |
| `eleven_monolingual_v1` | English-only model | Optimized for English |
| `eleven_turbo_v2` | Fast generation model | Quick response time |

For the most up-to-date information, see the [ElevenLabs documentation](https://docs.elevenlabs.io/api-reference/text-to-speech).

#### Example

```python
from apicenter import apicenter

# Using multilingual model
audio_bytes = apicenter.audio(
    provider="elevenlabs",
    model="eleven_multilingual_v2",
    prompt="Hello, welcome to the world of artificial intelligence and text-to-speech technology.",
    voice_id="Rachel"
)
```

## Model Selection Guidelines

When choosing a model, consider these factors:

1. **Task Complexity**: For more complex tasks, use more powerful models:
   - Complex reasoning: GPT-4, Claude 3 Opus
   - Simple questions: GPT-3.5 Turbo, Claude 3 Haiku, Ollama models

2. **Cost Efficiency**: More powerful models typically cost more:
   - Budget-sensitive: GPT-3.5 Turbo, Claude 3 Haiku, Ollama models
   - Quality priority: GPT-4, Claude 3 Opus, DALL-E 3

3. **Speed Requirements**:
   - Faster responses: GPT-3.5 Turbo, Claude 3 Haiku, smaller Ollama models
   - Quality over speed: GPT-4, Claude 3 Opus

4. **Context Length**:
   - Longer documents: Models with larger context windows
   - Short interactions: Any model

5. **Local vs. Cloud**:
   - Privacy concerns: Ollama models (run locally)
   - No hardware limitations: Cloud-based models (OpenAI, Anthropic)

6. **Multimodal Needs**:
   - Image understanding: GPT-4 Vision
   - Code generation: Codellama, Wizardcoder
   - Multi-language audio: eleven_multilingual_v2

Always check the provider's documentation for the most up-to-date model capabilities and recommendations. 