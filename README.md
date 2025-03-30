# APICenter

[![Tests](https://github.com/alishchhetri/apicenter/actions/workflows/tests.yml/badge.svg)](https://github.com/alishchhetri/apicenter/actions/workflows/tests.yml)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Universal Python interface for AI APIs. One consistent pattern for all your AI needs.

## Overview

APICenter simplifies interactions with AI services by providing a standardized interface across multiple AI providers and modalities. Instead of learning different syntax for each API, you can use one consistent pattern regardless of whether you're working with OpenAI, Anthropic, or local models through Ollama.

**Core Philosophy**: Write once, use everywhere.

```python
# Generate text with OpenAI
text = apicenter.text(
    provider="openai", 
    model="gpt-4", 
    prompt="Write a poem about birds"
)

# Switch to Anthropic with the same interface
text = apicenter.text(
    provider="anthropic", 
    model="claude-3-sonnet-20240229", 
    prompt="Write a poem about birds"
)

# Use local models with Ollama
text = apicenter.text(
    provider="ollama", 
    model="llama2", 
    prompt="Write a poem about birds"
)
```

## Features

- **Unified API**: Consistent pattern across all providers and modalities
- **Multiple Modes**:
  - Text Generation: OpenAI, Anthropic, Ollama (local models)
  - Image Generation: OpenAI DALL-E, Stability AI
  - Audio Generation: ElevenLabs
- **Local Model Support**: Integrate with locally-hosted models via Ollama
- **Flexible Design**: Pass any provider-specific parameters via kwargs
- **Simple Credential Management**: Easy API key configuration
- **Type Safety**: Full type hints for better development experience
- **Extensible**: Easily add new providers and modes

## Installation

APICenter is currently in development and not yet published to PyPI. To use it:

```bash
# Clone the repository
git clone https://github.com/alishchhetri/apicenter.git
cd apicenter

# Install using Poetry (recommended)
poetry install

# Alternatively, install in development mode with pip
pip install -e .
```

### Requirements

- Python 3.12 or higher
- Required packages are listed in pyproject.toml
- For local model support: [Ollama](https://ollama.ai/)

## Quick Start

APICenter follows a simple, consistent pattern for all API calls:

```python
from apicenter import apicenter

response = apicenter.<mode>(
    provider="<provider_name>",
    model="<model_name>",
    prompt="<your_prompt>",  # Can be a string or structured input like a list
    **kwargs  # Additional provider-specific parameters
)
```

### Text Generation

```python
from apicenter import apicenter

# OpenAI example
response = apicenter.text(
    provider="openai",
    model="gpt-4",
    prompt="Explain quantum computing in simple terms"
)
print(response)

# Anthropic example
response = apicenter.text(
    provider="anthropic",
    model="claude-3-sonnet-20240229",
    prompt="Write a short story about AI"
)
print(response)

# Ollama example (local model)
response = apicenter.text(
    provider="ollama",
    model="llama2",  # Any model you've pulled locally
    prompt="What is the capital of France?"
)
print(response)
```

### Image Generation

```python
# OpenAI DALL-E (returns a single URL string)
image_url = apicenter.image(
    provider="openai",
    model="dall-e-3",
    prompt="A serene mountain lake at sunset",
    size="1024x1024"
)

# Download and save the image
import requests
response = requests.get(image_url)
with open("generated_image.png", "wb") as f:
    f.write(response.content)

# Stability AI (returns bytes directly)
image_bytes = apicenter.image(
    provider="stability",
    model="stable-diffusion-xl-1024-v1-0",
    prompt="A cyberpunk cityscape at night"
)

# Save image bytes directly
with open("stability_image.png", "wb") as f:
    f.write(image_bytes)
```

### Audio Generation

```python
# ElevenLabs
audio_bytes = apicenter.audio(
    provider="elevenlabs",
    model="eleven_multilingual_v2",
    prompt="Hello! This is a text-to-speech test.",
    voice_id="Adam"  # Optional voice selection
)

# Save audio to file
with open("speech.mp3", "wb") as f:
    f.write(audio_bytes)
```

## Configuration

APICenter uses a `credentials.json` file to store API keys. Place it in one of these locations:

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

### Local Models

For Ollama (local model provider), no API keys are needed. Simply:

1. Install Ollama from [ollama.ai](https://ollama.ai/)
2. Pull your desired model(s): `ollama pull llama2`
3. Make sure the Ollama service is running
4. Use with APICenter: `apicenter.text(provider="ollama", model="llama2", ...)`

## Advanced Usage

### Chat Conversations

For chat-based models, use message lists:

```python
# Chat conversation with OpenAI
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the distance to the Moon?"}
]

response = apicenter.text(
    provider="openai",
    model="gpt-4",
    prompt=messages
)
print(response)

# Continue the conversation
messages.append({"role": "assistant", "content": response})
messages.append({"role": "user", "content": "How long would it take to travel there?"})

follow_up = apicenter.text(
    provider="openai",
    model="gpt-4",
    prompt=messages
)
print(follow_up)
```

#### Advanced Chat with System Prompts

APICenter automatically handles the different message formats for each provider. You can use standard chat format with system prompts for all providers:

```python
# OpenAI with system prompt
response = apicenter.text(
    provider="openai",
    model="gpt-4",
    prompt=[
        {"role": "system", "content": "You are a helpful assistant specialized in science."},
        {"role": "user", "content": "Explain the theory of relativity in simple terms."}
    ],
    temperature=0.7
)

# Anthropic with system prompt (automatically handled correctly)
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

# Ollama with conversation history
response = apicenter.text(
    provider="ollama",
    model="llama2",
    prompt=[
        {"role": "system", "content": "You are a friendly AI assistant."},
        {"role": "user", "content": "What are the three laws of robotics?"},
        {"role": "assistant", "content": "The three laws are..."},
        {"role": "user", "content": "Who created these laws?"}
    ]
)
```

### Provider-Specific Parameters

Pass any provider-specific parameters directly using kwargs:

```python
# OpenAI with specific parameters
response = apicenter.text(
    provider="openai",
    model="gpt-4",
    prompt="Generate a poem about space",
    temperature=0.8,
    max_tokens=500
)

# Image generation with specific parameters
image = apicenter.image(
    provider="stability",
    model="stable-diffusion-xl-1024-v1-0",
    prompt="A photorealistic portrait of a Viking warrior",
    steps=50,
    cfg_scale=7.0
)
```

The flexibility of `**kwargs` allows you to pass any provider-specific parameters without needing to learn special syntax for each provider.

## Documentation

For more detailed documentation, see the [docs](docs/) directory:

- [API Reference](docs/api_reference.md) - Complete API documentation
- [Configuration Guide](docs/configuration.md) - How to configure APICenter
- [Examples](examples/) - Various usage examples

## Testing

APICenter includes a comprehensive test suite to ensure reliability and stability. The tests use mock objects to simulate API calls, so you don't need actual API keys to run the tests.

### Running Tests

You can run the tests using the provided `run_tests.py` script:

```bash
# Run all tests
python tests/run_tests.py

# Run tests with coverage reporting
python tests/run_tests.py --coverage

# Run tests and show slow tests (>0.1s)
python tests/run_tests.py --show-slow

# Run only specific tests matching a pattern
python tests/run_tests.py --pattern="test_text_*.py"
```

You can also run individual test files directly:

```bash
python -m unittest tests/test_apicenter.py
```

### Testing with Ollama

Ollama tests require a local Ollama installation and are skipped in CI environments. To run these tests locally:

1. Install Ollama from [ollama.ai](https://ollama.ai/)
2. Pull the test model: `ollama pull llama2`
3. Start the Ollama service
4. Run the tests as normal

### Test Coverage

For developers contributing to the project, we aim to maintain high test coverage. You can generate a coverage report by installing the coverage package and running the tests with the `--coverage` flag:

```bash
pip install coverage
python tests/run_tests.py --coverage
```

For more information about testing, see the [tests/README.md](tests/README.md) file.

## Contributing

We welcome contributions to APICenter! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute.

## License

APICenter is licensed under the MIT License - see [LICENSE](LICENSE) for details. 