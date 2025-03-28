# APICenter

A universal Python SDK for AI APIs that provides a simple and consistent interface for multiple AI providers. APICenter standardizes the way you interact with different AI services, making it easy to switch between providers without changing your code.

## Features

- **Universal Interface**: Same simple API structure for all providers
- **Multiple Modes**:
  - Text Generation (OpenAI, Anthropic)
  - Image Generation (OpenAI DALL-E, Stability AI)
  - Audio Generation (ElevenLabs)
- **Flexible Configuration**: Easy credential management
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

# Generate text
response = apicenter.text(
    provider="anthropic",
    model="claude-3-sonnet-20240229",
    prompt="Write a haiku about programming"
)

# Generate image
image = apicenter.image(
    provider="openai",
    model="dall-e-3",
    prompt="A beautiful sunset over mountains"
)

# Generate audio
audio = apicenter.audio(
    provider="elevenlabs",
    model="eleven_multilingual_v2",
    prompt="Hello! This is a test of text to speech."
)
```

## Configuration

APICenter requires a `credentials.json` file with your API keys. You can place it in:
- Project root directory
- User's home directory under `.apicenter/`
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
- `provider`: The AI service provider (e.g., "openai", "anthropic")
- `model`: The specific model to use (e.g., "gpt-4", "claude-3-sonnet-20240229")
- `prompt`: The input text for the AI operation

### Optional Parameters
Each provider supports additional parameters via `**kwargs`. See the [Provider Documentation](docs/providers.md) for details.

## Examples

See the [examples](examples/) directory for detailed examples:
- [Basic Usage](examples/basic_usage.py)
- [Advanced Usage](examples/advanced_usage.py)

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