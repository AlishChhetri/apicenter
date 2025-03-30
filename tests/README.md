# APICenter Test Suite

This directory contains the test suite for the APICenter project. The tests are designed to verify the functionality of APICenter without requiring actual API keys or making real API calls.

## Running the Tests

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

## Test Structure

The test suite is organized as follows:

- **Provider Tests**: Tests for each provider implementation (OpenAI, Anthropic, etc.)
- **Main Class Tests**: Tests for the main APICenter class
- **Error Handling Tests**: Tests for error handling scenarios

### Provider Tests

- `test_text_openai.py`: Tests for OpenAI text provider (includes different prompt formats)
- `test_text_anthropic.py`: Tests for Anthropic text provider (includes different prompt formats)
- `test_text_ollama.py`: Tests for Ollama text provider
- `test_image_openai.py`: Tests for OpenAI image provider (returns single URL string)
- `test_image_stability.py`: Tests for Stability AI image provider
- `test_audio_elevenlabs.py`: Tests for ElevenLabs audio provider

### Main Class Tests

- `test_apicenter.py`: Tests for the main APICenter class

### Error Handling Tests

- `test_error_handling.py`: Tests for error handling in various scenarios

## Implementation Notes

- The prompt parameter for all providers accepts flexible types (`Any`), allowing for string prompts, lists, or other structures as needed.
- OpenAI DALL-E image provider returns a single URL string rather than a list of URLs.
- All provider functions are designed to handle various input formats appropriate for that specific provider.

## Mock Testing

All tests use Python's `unittest.mock` to mock API calls to external services. This ensures that:

1. Tests run quickly without needing to make real API calls
2. Tests don't require actual API keys
3. Tests can simulate various response scenarios and error conditions

## Coverage Reporting

To run tests with coverage reporting:

```bash
# Install coverage package
pip install coverage

# Run tests with coverage
python tests/run_tests.py --coverage
```

This will generate a coverage report in the terminal and an HTML report in the `tests/coverage_html` directory.

## Contributing

When adding new features to APICenter, please add corresponding tests. This ensures that:

1. Your implementation works as expected
2. Future changes don't break your implementation
3. The test suite remains comprehensive 