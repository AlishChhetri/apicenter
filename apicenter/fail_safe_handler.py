"""Fail-safe handler to switch to an alternate provider if the primary one fails"""

from apicenter.llm import LLM
from apicenter.text_to_image import TextToImage
from apicenter.computer_vision import ComputerVision

llm = LLM()
text_to_image = TextToImage()
computer_vision = ComputerVision()


def fail_safe_handler(
    fail_safe_queue,
    messages=None,
    prompt=None,
    task_type=None,
    source=None,
    max_tokens=100,
    temperature=0.5,
    **kwargs,
):
    """Attempts to call fail-safe providers in the given priority order until one succeeds."""

    for fail_safe_provider, fail_safe_model in fail_safe_queue:
        try:
            # Text-to-image fail-safe
            if prompt is not None:
                if fail_safe_provider.lower() == "openai":
                    return text_to_image.call_openai_dalle(
                        model=fail_safe_model,
                        prompt=prompt,
                        size=kwargs.get("size", "1024x1024"),
                        n=kwargs.get("n", 1),
                        quality=kwargs.get("quality", "standard"),
                    )

            # LLM fail-safe
            elif messages is not None:
                if fail_safe_provider.lower() == "openai":
                    return llm.call_openai_api(
                        model=fail_safe_model,
                        messages=messages,
                        max_tokens=max_tokens,
                        temperature=temperature,
                    )
                elif fail_safe_provider.lower() == "anthropic":
                    return llm.call_anthropic_api(
                        model=fail_safe_model,
                        system=kwargs.get("system", "You are a helpful assistant."),
                        messages=messages,
                        max_tokens=max_tokens,
                        temperature=temperature,
                    )

            # Computer vision fail-safe
            elif task_type is not None and source is not None:
                if fail_safe_provider.lower() == "ultralytics":
                    if task_type == "image":
                        return computer_vision.process_image(
                            provider=fail_safe_provider,
                            model=fail_safe_model,
                            image_path=source,
                            **kwargs,
                        )
                    elif task_type == "video":
                        return computer_vision.process_video(
                            provider=fail_safe_provider,
                            model=fail_safe_model,
                            video_path=source,
                            output_path=kwargs.get("output_path"),
                            **kwargs,
                        )
                    elif task_type == "realtime":
                        return computer_vision.realtime_camera(
                            provider=fail_safe_provider,
                            model=fail_safe_model,
                            camera_id=kwargs.get("camera_id", 0),
                            **kwargs,
                        )

        except Exception as fail_safe_error:
            print(
                f"Fail-safe provider '{fail_safe_provider}' failed with error:\n{fail_safe_error}\n"
            )

    raise RuntimeError("All fail-safe providers have failed.")
