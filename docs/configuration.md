# Configuration Guide

This document explains how to configure APICenter to work with various AI providers.

## Table of Contents

- [Credentials File](#credentials-file)
  - [Location](#location)
  - [Structure](#structure)
  - [Example](#example)
- [Environment Variables](#environment-variables)
- [Per-Provider Configuration](#per-provider-configuration)
  - [OpenAI](#openai)
  - [Anthropic](#anthropic)
  - [Stability AI](#stability-ai)
  - [ElevenLabs](#elevenlabs)
  - [Ollama](#ollama)
- [Default Parameters](#default-parameters)
- [Troubleshooting](#troubleshooting)

## Credentials File

APICenter uses a JSON file to store API keys and other provider-specific configuration. This keeps your credentials separate from your code and allows for different configurations in different environments.

### File Location

APICenter will look for a `credentials.json` file in the following locations (in order):

1. Custom path specified by the `APICENTER_CREDENTIALS_PATH` environment variable
2. Current working directory (`./credentials.json`)
3. Project root directory
4. User's home directory (`~/.apicenter/credentials.json`)
5. System config directory (`~/.config/apicenter/credentials.json`)

### File Structure

The credentials file follows this structure:

```json
{
    "modes": {
        "<mode>": {
            "providers": {
                "<provider>": {
                    "api_key": "your-api-key",
                    "additional_params": {}
                }
            }
        }
    }
}
```

Where:
- `<mode>` is one of: `text`, `image`, `audio`
- `<provider>` is a supported provider for that mode (e.g., `openai`, `anthropic`)

### Example Credentials File

Here's a complete example of a credentials.json file:

```json
{
    "modes": {
        "text": {
            "providers": {
                "openai": {
                    "api_key": "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                    "organization": "org-xxxxxxxxxxxxxxxx"
                },
                "anthropic": {
                    "api_key": "sk-ant-apixx-xxxxxxxxxxxxxxxxxxxx"
                }
            }
        },
        "image": {
            "providers": {
                "openai": {
                    "api_key": "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                    "organization": "org-xxxxxxxxxxxxxxxx"
                },
                "stability": {
                    "api_key": "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
                }
            }
        },
        "audio": {
            "providers": {
                "elevenlabs": {
                    "api_key": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
                }
            }
        }
    }
}
```

## Provider Configuration

### OpenAI

**Required fields:**
- `api_key`: Your OpenAI API key

**Optional fields:**
- `organization`: Your OpenAI organization ID

**How to get keys:**
Create an account at [platform.openai.com](https://platform.openai.com/) and generate an API key.

### Anthropic

**Required fields:**
- `api_key`: Your Anthropic API key

**How to get keys:**
Create an account at [console.anthropic.com](https://console.anthropic.com/) and generate an API key.

### Stability AI

**Required fields:**
- `api_key`: Your Stability AI API key

**How to get keys:**
Create an account at [platform.stability.ai](https://platform.stability.ai/) and generate an API key.

### ElevenLabs

**Required fields:**
- `api_key`: Your ElevenLabs API key

**How to get keys:**
Create an account at [elevenlabs.io](https://elevenlabs.io/) and find your API key in your profile settings.

### Ollama (Local Models)

Ollama doesn't require API keys in the credentials file as it runs locally.

**Setup:**
1. Install Ollama from [ollama.ai](https://ollama.ai/)
2. Pull your desired model: `ollama pull llama2`
3. Run the Ollama service
4. Use APICenter with `provider="ollama"`

## Environment Variables

APICenter supports the following environment variables:

- `APICENTER_CREDENTIALS_PATH`: Custom path to the credentials file
  ```bash
  export APICENTER_CREDENTIALS_PATH="/path/to/your/credentials.json"
  ```

- `OLLAMA_HOST`: Host address for Ollama (default: `http://localhost:11434`)
  ```bash
  export OLLAMA_HOST="http://localhost:11434"
  ```

## Security Best Practices

When working with API keys:

1. **Never commit credentials to version control**
   - Add `credentials.json` to your `.gitignore` file
   
2. **Use environment-specific credential files**
   - Use different files for development, testing, and production
   
3. **Limit API key permissions**
   - Create keys with the minimum necessary permissions
   
4. **Rotate keys periodically**
   - Change your API keys regularly

5. **Use environment variables for CI/CD**
   - In CI/CD pipelines, inject credentials as environment variables

## Troubleshooting

### Common Issues

#### Credentials Not Found
- Verify the file exists at one of the expected locations
- Check file permissions
- Set the `APICENTER_CREDENTIALS_PATH` environment variable

#### API Key Errors
- Ensure the key is correct and active
- Check for typos or extra whitespace
- Verify the key has sufficient permissions

#### Local Model Errors
- Verify Ollama is installed and running
- Ensure the model is pulled (`ollama pull <model>`)
- Check if Ollama is running on a custom host/port and set `OLLAMA_HOST` accordingly

### Debug Mode

For detailed debug information, you can use Python's logging system:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Getting Help

If you encounter issues not covered here:
1. Check the [GitHub repository](https://github.com/alishchhetri/apicenter) for open issues
2. Submit a new issue with detailed information about your problem
3. Join community discussions 