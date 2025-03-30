# APICenter Configuration Guide

This guide explains how to configure APICenter for use with various AI providers.

## Table of Contents

- [Credentials Configuration](#credentials-configuration)
  - [Credentials File Location](#credentials-file-location)
  - [Credentials File Format](#credentials-file-format)
- [Provider-Specific Configuration](#provider-specific-configuration)
  - [OpenAI](#openai)
  - [Anthropic](#anthropic)
  - [Stability AI](#stability-ai)
  - [ElevenLabs](#elevenlabs)
  - [Ollama](#ollama)
- [Environment Variables](#environment-variables)
- [Using Multiple Configurations](#using-multiple-configurations)
- [Securing Your Credentials](#securing-your-credentials)
- [Troubleshooting](#troubleshooting)

## Credentials Configuration

APICenter uses a credentials file to store API keys and other authentication information for the various AI services it interacts with.

### Credentials File Location

APICenter will look for credentials in the following locations (in order):

1. Custom path specified by `APICENTER_CREDENTIALS_PATH` environment variable
2. Current working directory: `./credentials.json`
3. Project root directory: `<project_root>/credentials.json`
4. User's home directory: `~/.apicenter/credentials.json`
5. System config directory: `~/.config/apicenter/credentials.json`

### Credentials File Format

The credentials file uses a JSON structure organized by mode and provider:

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

You only need to include configurations for the providers you plan to use.

## Provider-Specific Configuration

### OpenAI

OpenAI requires an API key and optionally an organization ID:

```json
"openai": {
    "api_key": "your-openai-api-key",
    "organization": "your-organization-id"  // Optional
}
```

You can obtain an API key from the [OpenAI API Keys page](https://platform.openai.com/api-keys).

### Anthropic

Anthropic requires an API key:

```json
"anthropic": {
    "api_key": "your-anthropic-api-key"
}
```

You can obtain an API key from the [Anthropic Console](https://console.anthropic.com/).

### Stability AI

Stability AI requires an API key:

```json
"stability": {
    "api_key": "your-stability-api-key"
}
```

You can obtain an API key from the [Stability AI Dashboard](https://platform.stability.ai/account/keys).

### ElevenLabs

ElevenLabs requires an API key:

```json
"elevenlabs": {
    "api_key": "your-elevenlabs-api-key"
}
```

You can obtain an API key from the [ElevenLabs Dashboard](https://elevenlabs.io/app/profile).

### Ollama (Local Models)

Ollama doesn't require an API key since it runs locally. However, you can configure the host if needed:

```bash
# Set Ollama host environment variable (optional)
export OLLAMA_HOST="http://localhost:11434"
```

By default, APICenter will connect to Ollama at `http://localhost:11434`.

## Environment Variables

APICenter supports the following environment variables:

- `APICENTER_CREDENTIALS_PATH`: Path to credentials file
- `OLLAMA_HOST`: Host for Ollama API (default: `http://localhost:11434`)

## Using Multiple Configurations

You can maintain multiple configuration files for different projects or environments:

1. Create separate credential files (e.g., `credentials-dev.json`, `credentials-prod.json`)
2. Set the environment variable to use a specific configuration:

```bash
export APICENTER_CREDENTIALS_PATH="/path/to/credentials-prod.json"
```

## Securing Your Credentials

To keep your API keys secure:

1. Never commit your credentials.json file to version control
2. Add credentials.json to your .gitignore file
3. Consider using environment variables or a secret management system for production use
4. Set appropriate file permissions (e.g., `chmod 600 credentials.json`)

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