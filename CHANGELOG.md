# Changelog

All notable changes to the APICenter project will be documented in this file.

## [Unreleased]

### Added
- **Universal parameter handling** for all providers
  - Automatic routing of parameters to provider-specific implementations
  - Proper handling of system messages for text providers
  - Support for voice settings parameters in ElevenLabs
  - Support for negative prompts in Stability AI
  - Support for model options in Ollama
- **Comprehensive test suite**
  - Unit tests for all providers and functionality
  - Integration tests for end-to-end flows
  - Error handling tests
  - Test runner with coverage reporting
  - 85%+ code coverage

### Fixed
- Improved Anthropic implementation to correctly handle system prompts
- Updated Stability AI endpoint to match current API structure
- Fixed Ollama parameter handling to use options dictionary for temperature, etc.
- Fixed ElevenLabs implementation to properly handle voice settings parameters

### Changed
- Updated documentation with comprehensive examples of provider-specific parameters
- Added detailed API reference for provider-specific parameters
- Added examples demonstrating advanced usage with structured messages and parameters
- Added unit tests for all provider implementations

## [0.1.0] - Initial Release

### Added
- Initial framework for unified AI API interface
- Support for text generation with OpenAI, Anthropic, and Ollama
- Support for image generation with OpenAI and Stability AI
- Support for audio generation with ElevenLabs
- Basic credential management system 