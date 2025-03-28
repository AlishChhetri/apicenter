# Extending APICenter

This guide explains how to extend APICenter with new modes and providers.

## Adding a New Mode

A mode in APICenter represents a type of AI operation (e.g., text, image, audio). To add a new mode:

1. Create a new module under `apicenter/`:
```bash
mkdir apicenter/new_mode
touch apicenter/new_mode/__init__.py
```

2. Create a base provider class for the mode:
```python
# apicenter/new_mode/provider.py
from typing import Any, Dict, Optional
from ..core.base import BaseProvider

class NewModeProvider(BaseProvider[Any]):
    """Base provider for the new mode."""
    
    def _get_mode(self) -> str:
        return "new_mode"
    
    def validate_params(self) -> None:
        """Validate mode-specific parameters."""
        pass
    
    def call(self) -> Any:
        """Make the API call."""
        pass
```

3. Add the mode to the APICenter class:
```python
# apicenter/apicenter.py
from .new_mode.provider import NewModeProvider

class APICenter:
    def __init__(self):
        self._providers = {
            # ... existing modes ...
            "new_mode": {
                "provider1": NewModeProvider,
                "provider2": NewModeProvider,
            }
        }
    
    def new_mode(
        self,
        provider: str,
        model: str,
        prompt: str,
        **kwargs: Any
    ) -> Any:
        """
        Universal function for new mode operations.
        
        Args:
            provider: The AI service provider
            model: The specific model to use
            prompt: The input prompt
            **kwargs: Additional parameters specific to the provider
            
        Returns:
            The response from the provider
        """
        provider_class = self._get_provider_class("new_mode", provider)
        return provider_class(provider, model, prompt, **kwargs).get_response()
```

4. Add mode-specific documentation in `docs/modes/new_mode.md`

## Adding a New Provider to an Existing Mode

To add a new provider to an existing mode (e.g., adding a new text generation provider):

1. Create a new provider class in the mode's module:
```python
# apicenter/text/providers/new_provider.py
from typing import Any
from ...core.base import BaseProvider

class NewTextProvider(BaseProvider[str]):
    """Provider for text generation using NewService."""
    
    def _get_mode(self) -> str:
        return "text"
    
    def validate_params(self) -> None:
        """Validate provider-specific parameters."""
        if not self.model.startswith(("model-", "text-")):
            raise ValueError(f"Invalid model: {self.model}")
        if "temperature" in self.kwargs and not 0 <= self.kwargs["temperature"] <= 1:
            raise ValueError("Temperature must be between 0 and 1")
    
    def call(self) -> str:
        """Make the API call to NewService."""
        # Implementation here
        pass
```

2. Add the provider to the mode's `__init__.py`:
```python
# apicenter/text/__init__.py
from .providers.new_provider import NewTextProvider

__all__ = ["NewTextProvider"]
```

3. Add the provider to the APICenter class:
```python
# apicenter/apicenter.py
from .text.providers.new_provider import NewTextProvider

class APICenter:
    def __init__(self):
        self._providers = {
            "text": {
                # ... existing providers ...
                "new_provider": NewTextProvider,
            }
        }
```

4. Add provider-specific documentation in `docs/providers/new_provider.md`

## Provider Implementation Guidelines

### Required Methods

Every provider must implement:
1. `_get_mode()`: Return the mode this provider handles
2. `validate_params()`: Validate provider-specific parameters
3. `call()`: Make the actual API call

### Best Practices

1. **Type Safety**:
   - Use proper type hints
   - Validate input parameters
   - Handle API-specific error types

2. **Error Handling**:
   - Validate parameters before making API calls
   - Handle API-specific errors
   - Provide meaningful error messages

3. **Documentation**:
   - Add docstrings for all methods
   - Document provider-specific parameters
   - Include usage examples

4. **Testing**:
   - Add unit tests for the provider
   - Add integration tests
   - Test error cases

## Example: Adding a New Video Generation Mode

Here's a complete example of adding a new video generation mode:

1. Create the mode structure:
```bash
mkdir -p apicenter/video/providers
touch apicenter/video/__init__.py
touch apicenter/video/provider.py
touch apicenter/video/providers/__init__.py
```

2. Implement the base provider:
```python
# apicenter/video/provider.py
from typing import Any, Dict, Optional
from ..core.base import BaseProvider

class VideoProvider(BaseProvider[bytes]):
    """Base provider for video generation."""
    
    def _get_mode(self) -> str:
        return "video"
    
    def validate_params(self) -> None:
        """Validate video-specific parameters."""
        pass
    
    def call(self) -> bytes:
        """Make the API call."""
        pass
```

3. Implement a specific provider:
```python
# apicenter/video/providers/example.py
from typing import Any
from ...core.base import BaseProvider

class ExampleVideoProvider(BaseProvider[bytes]):
    """Provider for video generation using ExampleService."""
    
    def _get_mode(self) -> str:
        return "video"
    
    def validate_params(self) -> None:
        if not self.model.startswith(("video-", "gen-")):
            raise ValueError(f"Invalid model: {self.model}")
        if "duration" in self.kwargs and not 1 <= self.kwargs["duration"] <= 60:
            raise ValueError("Duration must be between 1 and 60 seconds")
    
    def call(self) -> bytes:
        # Implementation here
        pass
```

4. Add the mode to APICenter:
```python
# apicenter/apicenter.py
from .video.provider import VideoProvider
from .video.providers.example import ExampleVideoProvider

class APICenter:
    def __init__(self):
        self._providers = {
            # ... existing modes ...
            "video": {
                "example": ExampleVideoProvider,
            }
        }
    
    def video(
        self,
        provider: str,
        model: str,
        prompt: str,
        **kwargs: Any
    ) -> bytes:
        """Generate video using the specified provider."""
        provider_class = self._get_provider_class("video", provider)
        return provider_class(provider, model, prompt, **kwargs).get_response()
```

5. Add documentation:
```markdown
# docs/modes/video.md
# Video Generation Mode

This mode handles video generation using various AI providers.

## Supported Providers

- ExampleService: Generate videos from text descriptions

## Usage

```python
from apicenter import apicenter

video = apicenter.video(
    provider="example",
    model="video-1",
    prompt="A beautiful sunset timelapse",
    duration=10,
    resolution="1080p"
)
```

## Provider-Specific Parameters

### ExampleService
- `duration`: Video duration in seconds (1-60)
- `resolution`: Output resolution ("720p", "1080p", "4k")
``` 