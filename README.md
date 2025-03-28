# APICenter

A universal Python SDK for AI APIs that supports multiple modes (text, image, audio) with a simple and consistent interface.

## Features

- Support for multiple AI providers:
  - Text: OpenAI, Anthropic
  - Image: OpenAI DALL-E, Stability AI
  - Audio: ElevenLabs
- Simple and consistent API interface
- Flexible credential management
- Easy to extend with new providers and modes

## Installation

```bash
poetry add apicenter
```

## Configuration

APICenter requires a `credentials.json` file in your project root or specified via the `APICENTER_CREDENTIALS_PATH` environment variable.

### Using credentials.json

Create a `credentials.json` file in your project root:

```json
{
    "modes": {
        "text": {
            "providers": {
                "openai": {
                    "providers": {
                        "openai": {
                            "api_key": "your-openai-api-key",
                            "organization": "your-org-id"
                        }
                    }
                },
                "anthropic": {
                    "providers": {
                        "anthropic": {
                            "api_key": "your-anthropic-api-key"
                        }
                    }
                }
            }
        },
        "image": {
            "providers": {
                "openai": {
                    "providers": {
                        "openai": {
                            "api_key": "your-openai-api-key",
                            "organization": "your-org-id"
                        }
                    }
                },
                "stability": {
                    "providers": {
                        "stability": {
                            "api_key": "your-stability-api-key"
                        }
                    }
                }
            }
        },
        "audio": {
            "providers": {
                "elevenlabs": {
                    "providers": {
                        "elevenlabs": {
                            "api_key": "your-elevenlabs-api-key"
                        }
                    }
                }
            }
        }
    }
}
```

### Custom Credentials Location

You can specify a custom location for your credentials file using the `APICENTER_CREDENTIALS_PATH` environment variable:

```bash
export APICENTER_CREDENTIALS_PATH=/path/to/your/credentials.json
```

## Usage

APICenter provides a universal interface for all AI operations with three required parameters:
- `provider`: The AI service provider (e.g., "openai", "anthropic", "elevenlabs")
- `model`: The specific model to use (e.g., "gpt-4", "claude-3-sonnet-20240229", "eleven_multilingual_v2")
- `prompt`: The input text for the AI operation

Additional parameters can be passed as keyword arguments.

### Text Generation

```python
from apicenter import apicenter

# Minimal call with OpenAI
response = apicenter.text(
    provider="openai",
    model="gpt-4",
    prompt="Give me a list of 5 animals."
)

# Detailed call with OpenAI
response = apicenter.text(
    provider="openai",
    model="gpt-4",
    prompt="Write a short story about a robot learning to paint.",
    temperature=0.7,
    max_tokens=1000,
    top_p=0.9,
    frequency_penalty=0.5,
    presence_penalty=0.5
)
```

### Image Generation

```python
from apicenter import apicenter
from PIL import Image

# Minimal call with OpenAI DALL-E
image = apicenter.image(
    provider="openai",
    model="dall-e-3",
    prompt="A beautiful sunset over mountains"
)

# Detailed call with OpenAI DALL-E
image = apicenter.image(
    provider="openai",
    model="dall-e-3",
    prompt="A beautiful sunset over mountains, with snow-capped peaks and a clear lake reflection",
    size="1024x1024",
    quality="standard",
    style="vivid"
)
```

### Audio Generation

```python
from apicenter import apicenter

# Minimal call with ElevenLabs
audio = apicenter.audio(
    provider="elevenlabs",
    model="eleven_multilingual_v2",
    prompt="This is a test of text to speech."
)

# Detailed call with ElevenLabs
audio = apicenter.audio(
    provider="elevenlabs",
    model="eleven_multilingual_v2",
    prompt="This is a test of text to speech with additional parameters.",
    voice_id="JBFqnCBsd6RMkjVDRZzb",
    output_format="mp3_44100_128",
    stability=0.5,
    similarity_boost=0.8,
    style=0.5,
    use_speaker_boost=True
)
```

## Extending APICenter

To add a new provider:

1. Create a new provider class in the appropriate module under `providers/`
2. Inherit from `BaseProvider`
3. Implement the required methods: `validate_params()` and `call()`
4. Add the provider to the `_providers` dictionary in the `APICenter` class

To add a new mode:

1. Create a new module under `providers/` for the mode's providers
2. Implement the provider classes
3. Add the mode and its providers to the `_providers` dictionary in the `APICenter` class
4. Add a new method to the `APICenter` class to handle the mode

## License

MIT License 