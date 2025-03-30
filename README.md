# APICenter

A universal Python SDK for AI APIs that provides a simple and consistent interface for multiple AI providers. APICenter standardizes the way you interact with different AI services, making it easy to switch between providers without changing your code.

## Features

- **Universal Interface**: Same simple API structure for all providers
- **Multiple Modes**:
  - Text Generation (OpenAI, Anthropic, Ollama)
  - Image Generation (OpenAI DALL-E, Stability AI)
  - Audio Generation (ElevenLabs)
- **Local Model Support**: Use local models with Ollama integration
- **Flexible Configuration**: Easy credential management with fallbacks
- **Type Safety**: Full type hints and validation
- **Error Handling**: Comprehensive error handling and validation
- **Extensible**: Easy to add new providers and modes

## Installation

```bash
# Using pip
pip install apicenter

# Using poetry
poetry add apicenter
```

## Quick Start

```python
from apicenter import apicenter

# Generate text with a cloud provider
response = apicenter.text(
    provider="anthropic",
    model="claude-3-sonnet-20240229",
    prompt="Write a haiku about programming"
)

# Generate text with a local model (Ollama)
response = apicenter.text(
    provider="ollama",
    model="llama2",  # or any model you've pulled locally
    prompt="What is the capital of France?"
)

# Generate image
image_url = apicenter.image(
    provider="openai",
    model="dall-e-3",
    prompt="A beautiful sunset over mountains"
)

# Generate audio
audio_bytes = apicenter.audio(
    provider="elevenlabs",
    model="eleven_multilingual_v2",
    prompt="Hello! This is a test of text to speech."
)

# Save audio to file
with open("output.mp3", "wb") as f:
    f.write(audio_bytes)
```

## Configuration

APICenter requires a `credentials.json` file with your API keys. You can place it in:
- Current working directory
- Project root directory
- User's home directory under `.apicenter/`
- System config directory under `.config/apicenter/`
- Custom location specified by `APICENTER_CREDENTIALS_PATH` environment variable

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

### Local Models (No API Keys Required)

For local models like Ollama, no API keys are needed in the credentials file. Just make sure the local service is running.

For Ollama:
1. Install Ollama from https://ollama.ai/
2. Pull your desired model: `ollama pull llama2` (or any other model)
3. Start Ollama (it will run as a service)
4. Use APICenter with the "ollama" provider

## Universal API Pattern

All APICenter calls follow the same pattern:
```python
apicenter.<mode>(
    provider="provider_name",
    model="model_name",
    prompt="your prompt",
    **kwargs  # Provider-specific parameters
)
```

### Required Parameters
- `provider`: The AI service provider (e.g., "openai", "anthropic", "ollama")
- `model`: The specific model to use (e.g., "gpt-4", "claude-3-sonnet-20240229", "llama2")
- `prompt`: The input text for the AI operation (can be a string or a message list for some providers)

### Optional Parameters
Each provider supports additional parameters via `**kwargs`. These are passed directly to the underlying API.

## Text Generation

```python
# Basic usage
response = apicenter.text(
    provider="openai",
    model="gpt-4",
    prompt="Write a haiku about programming"
)

# With additional parameters
response = apicenter.text(
    provider="anthropic",
    model="claude-3-sonnet-20240229",
    prompt="Write a story about space exploration",
    temperature=0.7,
    max_tokens=1000
)

# Using a list of messages (for chat-based APIs)
response = apicenter.text(
    provider="openai",
    model="gpt-4",
    prompt=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain quantum computing."}
    ]
)

# Using Ollama (local model)
response = apicenter.text(
    provider="ollama",
    model="llama2",
    prompt="What is the capital of France?",
    temperature=0.8,
    num_predict=300
)
```

## Image Generation

```python
# Generate image (get URL back)
image_url = apicenter.image(
    provider="openai",
    model="dall-e-3",
    prompt="A serene lake at sunset with mountains in the background",
    size="1024x1024",
    quality="hd",
    style="natural"
)

# Save the image to a file
import requests
response = requests.get(image_url)
with open("generated_image.png", "wb") as f:
    f.write(response.content)
```

## Audio Generation

```python
# Generate audio
audio_data = apicenter.audio(
    provider="elevenlabs",
    model="eleven_multilingual_v2",
    prompt="Hello world! This is a text-to-speech test.",
    voice_id="Adam",
    stability=0.5,
    similarity_boost=0.75
)

# Save audio to file
with open("output.mp3", "wb") as f:
    f.write(audio_data)
```

## Examples

See the [examples](examples/) directory for detailed examples:
- [Basic Usage](examples/basic_usage.py): Simple examples of each mode
- [Advanced Usage](examples/advanced_usage.py): More complex examples with additional parameters
- [Text Examples](examples/llm_examples.py): Focused examples for text generation
- [Image Examples](examples/image_examples.py): Focused examples for image generation
- [Audio Examples](examples/audio_examples.py): Focused examples for audio generation

## Error Handling

APICenter provides comprehensive error handling:
```python
try:
    response = apicenter.text(
        provider="anthropic",
        model="claude-3-sonnet-20240229",
        prompt="Write a story"
    )
except ValueError as e:
    print(f"Invalid parameters: {e}")
except FileNotFoundError as e:
    print(f"Configuration error: {e}")
except Exception as e:
    print(f"API error: {e}")
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on contributing to APICenter.

## License

MIT License - see [LICENSE](LICENSE) for details. 