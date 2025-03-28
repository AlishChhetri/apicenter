# Contributing to APICenter

Thank you for your interest in contributing to APICenter! This document provides guidelines and instructions for contributing.

## Development Setup

1. Fork and clone the repository:
```bash
git clone https://github.com/yourusername/apicenter.git
cd apicenter
```

2. Install development dependencies:
```bash
poetry install
```

3. Create a virtual environment and activate it:
```bash
poetry shell
```

## Project Structure

```
apicenter/
├── apicenter/           # Main package directory
│   ├── __init__.py
│   ├── apicenter.py     # Main APICenter class
│   ├── core/           # Core functionality
│   ├── text/           # Text generation providers
│   ├── image/          # Image generation providers
│   └── audio/          # Audio generation providers
├── examples/           # Example code
├── tests/             # Test files
├── docs/              # Documentation
│   ├── extending.md   # Guide for extending APICenter
│   ├── modes/         # Mode-specific documentation
│   └── providers/     # Provider-specific documentation
└── pyproject.toml     # Project configuration
```

## Extending APICenter

For detailed instructions on extending APICenter with new modes and providers, see [Extending APICenter](docs/extending.md). This guide covers:

- Adding new modes (e.g., video generation)
- Adding new providers to existing modes
- Provider implementation guidelines
- Best practices for implementation
- Complete examples

## Testing

1. Write tests for your new provider:
```python
def test_new_provider():
    response = apicenter.text(
        provider="new_provider",
        model="test-model",
        prompt="Test prompt"
    )
    assert response is not None
```

2. Run tests:
```bash
poetry run pytest
```

## Code Style

- Follow PEP 8 guidelines
- Use type hints
- Add docstrings for all public functions and classes
- Keep functions focused and small
- Use meaningful variable names

## Documentation

1. Update the README.md if adding new features
2. Add docstrings to new functions and classes
3. Update examples if needed
4. Add provider-specific documentation in docs/providers/
5. Add mode-specific documentation in docs/modes/

## Pull Request Process

1. Create a new branch for your feature:
```bash
git checkout -b feature/new-provider
```

2. Make your changes and commit them:
```bash
git add .
git commit -m "Add new provider: X"
```

3. Push to your fork:
```bash
git push origin feature/new-provider
```

4. Create a Pull Request on GitHub

## Code Review Guidelines

- Ensure all tests pass
- Check code style and formatting
- Verify documentation is complete
- Test with different providers and modes
- Consider edge cases and error handling

## Release Process

1. Update version in pyproject.toml
2. Update CHANGELOG.md
3. Create a new release on GitHub
4. Tag the release

## Questions?

If you have any questions, feel free to:
1. Open an issue
2. Join our discussions
3. Contact the maintainers

Thank you for contributing to APICenter! 