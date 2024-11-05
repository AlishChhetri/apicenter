"""Universal API caller for OpenAI, Anthropic, and image generation models"""

from apicenter.llm import LLM
from apicenter.text_to_image import TextToImage
from apicenter.computer_vision import ComputerVision
from apicenter.fail_safe_handler import fail_safe_handler


class UniversalAPICaller:
    """Handles both LLM, text-to-image, and computer vision API calls"""

    def __init__(self):
        self._cv = ComputerVision()

    def llm(
        self,
        provider,
        model,
        messages,
        max_tokens=100,
        temperature=0.5,
        fail_safe=None,
        **kwargs,
    ):
        """Calls the specified LLM API with the given configuration."""

        llm = LLM()
        try:
            if provider.lower() == "openai":
                return llm.call_openai_api(
                    model=model,
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=temperature,
                )
            elif provider.lower() == "anthropic":
                return llm.call_anthropic_api(
                    model=model,
                    system=kwargs.get("system", "You are a helpful assistant."),
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=temperature,
                )
        except Exception as primary_error:
            print(
                f"Primary provider '{provider}' encountered an error:\n{primary_error}\n"
            )

            if fail_safe:
                fail_safe_queue = (
                    fail_safe if isinstance(fail_safe, list) else [fail_safe]
                )
                return fail_safe_handler(
                    fail_safe_queue,
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    **kwargs,
                )

            raise primary_error

    def text_to_image(
        self,
        provider,
        model,
        prompt,
        size="1024x1024",
        n=1,
        quality="standard",
        fail_safe=None,
    ):
        """Calls the specified text-to-image API with the given configuration."""

        text_to_image = TextToImage()
        try:
            if provider.lower() == "openai":
                return text_to_image.call_openai_dalle(
                    model=model, prompt=prompt, size=size, n=n, quality=quality
                )
        except Exception as primary_error:
            print(
                f"Primary provider '{provider}' encountered an error:\n{primary_error}\n"
            )

            if fail_safe:
                fail_safe_queue = (
                    fail_safe if isinstance(fail_safe, list) else [fail_safe]
                )
                return fail_safe_handler(
                    fail_safe_queue, prompt=prompt, size=size, n=n, quality=quality
                )

            raise primary_error

    def computer_vision(self, provider, model, prompt, fail_safe=None, **kwargs):
        """Processes computer vision tasks using the specified provider and model."""

        try:
            task_type = prompt.get("task_type", "image")
            source = prompt.get("source")

            if task_type == "image":
                return self._cv.process_image(provider, model, source, **kwargs)
            elif task_type == "video":
                return self._cv.process_video(
                    provider,
                    model,
                    source,
                    output_path=prompt.get("output_path"),
                    **kwargs,
                )
            elif task_type == "realtime":
                return self._cv.realtime_camera(
                    provider, model, camera_id=prompt.get("camera_id", 0), **kwargs
                )
            else:
                raise ValueError(f"Unsupported task type: {task_type}")

        except Exception as primary_error:
            print(
                f"Primary provider '{provider}' encountered an error:\n{primary_error}\n"
            )

            if fail_safe:
                fail_safe_queue = (
                    fail_safe if isinstance(fail_safe, list) else [fail_safe]
                )
                return fail_safe_handler(
                    fail_safe_queue, task_type=task_type, source=source, **kwargs
                )

            raise primary_error


# Create an instance of UniversalAPICaller
apicenter = UniversalAPICaller()
