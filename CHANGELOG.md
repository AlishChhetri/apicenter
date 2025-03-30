# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project structure
- Support for text generation with OpenAI, Anthropic, and Ollama
- Support for image generation with OpenAI DALL-E and Stability AI
- Support for audio generation with ElevenLabs
- Unified API interface across all providers
- Comprehensive test suite with mock providers
- Detailed documentation
- GitHub Actions workflow for testing
- GitHub Actions workflow for automated releases

### Changed
- Fixed OpenAI DALL-E image provider to return a single URL string instead of a list
- Updated prompt parameter to accept flexible input types
- Improved error handling across all providers

### Fixed
- Corrected credential handling for various providers
- Fixed bare except issues in stability provider
- Resolved unused variable issues in Ollama provider

## [0.1.0] - Initial Release (Coming Soon)

- First public release
- Basic functionality for text, image, and audio generation

[Unreleased]: https://github.com/alishchhetri/apicenter/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/alishchhetri/apicenter/releases/tag/v0.1.0 