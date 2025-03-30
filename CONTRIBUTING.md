# Contributing to APICenter

Thank you for your interest in contributing to APICenter! This guide explains how to set up your development environment and contribute to the project.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
   ```bash
   git clone https://github.com/your-username/apicenter.git
   cd apicenter
   ```
3. **Set up the upstream remote**
   ```bash
   git remote add upstream https://github.com/alishchhetri/apicenter.git
   ```
4. **Create a new branch** for your changes
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Environment

### Using Poetry (Recommended)

```bash
# Install Poetry if you haven't already
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Activate the virtual environment
poetry env activate
```

### Using Pip

```bash
# Install the package in development mode
pip install -e .

# Install development dependencies
pip install -r requirements-dev.txt
```

## Project Structure

```
apicenter/
├── apicenter/                # Main package
│   ├── __init__.py           # Package initialization
│   ├── apicenter.py          # Main APICenter class
│   ├── core/                 # Core functionality
│   │   ├── base.py           # Base provider classes
│   │   └── credentials.py    # Credentials management
│   ├── text/                 # Text generation mode
│   │   ├── text.py           # Text provider implementation
│   │   └── providers/        # Text provider implementations
│   ├── image/                # Image generation mode
│   │   ├── image.py          # Image provider implementation
│   │   └── providers/        # Image provider implementations
│   └── audio/                # Audio generation mode
│       ├── audio.py          # Audio provider implementation
│       └── providers/        # Audio provider implementations
├── examples/                 # Example usage scripts
├── docs/                     # Documentation
├── tests/                    # Tests
└── pyproject.toml            # Project configuration
```

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- A clear, descriptive title
- Steps to reproduce the bug
- Expected vs. actual behavior
- Environment details (Python version, OS, etc.)

### Feature Requests

When suggesting a feature:
- Describe the problem you're trying to solve
- Explain how your suggestion would help
- Provide examples of how the feature would work

### Code Contributions

1. **Check existing issues and pull requests** to avoid duplication
2. **Create a focused branch** for your work
3. **Write clean, documented code** following our coding standards
4. **Add tests** for new functionality
5. **Update documentation** as needed
6. **Submit a pull request** with a clear description of your changes

## Adding a New Provider

To add a new provider to an existing mode (e.g., text, image, audio):

1. **Create a provider file** in the appropriate directory:
   ```
   apicenter/<mode>/providers/<provider_name>.py
   ```

2. **Implement the provider function** following this pattern:
   ```python
   def call_<provider_name>(model: str, prompt: Union[str, List[Dict[str, str]]], 
                           credentials: Dict[str, Any], **kwargs: Any) -> ReturnType:
       """Provider implementation.
       
       Args:
           model: The model to use
           prompt: The input prompt
           credentials: API credentials
           **kwargs: Additional parameters
           
       Returns:
           The provider response
       """
       try:
           # Initialize client
           client = ProviderClient(**credentials)
           
           # Process prompt if needed
           
           # Make API call
           response = client.method(
               model=model,
               prompt=prompt,
               **kwargs
           )
           
           # Return response
           return response.result
       except Exception as e:
           raise ValueError(f"{provider_name} error: {str(e)}")
   ```

3. **Update the Provider class** in the appropriate mode file:
   - Import your function (`from .providers.<provider_name> import call_<provider_name>`)
   - Add your provider to the provider_methods dictionary
   - Add a provider-specific call method if needed

4. **Register the provider** in the APICenter class in `apicenter.py`

5. **Add an example** showing how to use your new provider

## Adding a New Mode

To add an entirely new mode beyond text, image, and audio:

1. **Create a new mode directory**:
   ```
   apicenter/<new_mode>/
   ```

2. **Implement the following files**:
   - `<new_mode>.py` with a class extending BaseProvider
   - A `providers/` directory with provider implementations

3. **Update core files**:
   - Add your mode to the `providers` dictionary in `apicenter.py`
   - Add a new method in the `APICenter` class for your mode

4. **Add examples and documentation** for the new mode

## Coding Standards

- **Follow PEP 8** for code style
- **Use type hints** for all function parameters and return values
- **Write descriptive docstrings** with Args, Returns, and Raises sections
- **Naming conventions**:
  - Functions and variables: `snake_case`
  - Classes: `PascalCase`
  - Constants: `UPPER_CASE`
- **Use Black** for code formatting (88 character line limit)

## Testing

- Write tests for new features and bug fixes
- Run tests before submitting a pull request:
  ```bash
  pytest
  ```
- Ensure code passes style checks:
  ```bash
  black .
  flake8
  ```

## Documentation

- Update docstrings for any modified code
- Update or add examples for new functionality
- Update relevant documentation files in the docs/ directory
- Keep the README up-to-date with major changes

## Pull Request Process

1. **Update your fork** with the latest upstream changes
2. **Ensure your code passes all tests**
3. **Submit a pull request** to the main repository
4. **Respond to reviewer feedback** and make necessary changes
5. **Wait for approval** and merge

Thank you for contributing to APICenter! 