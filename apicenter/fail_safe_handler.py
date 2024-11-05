"""Fail-safe handler to switch to an alternate provider if the primary one fails"""

from apicenter.llm import LLM
from apicenter.text_to_image import TextToImage

llm = LLM()
text_to_image = TextToImage()


def fail_safe_handler(
    fail_safe_queue,
    messages=None,
    prompt=None,
    max_tokens=100,
    temperature=0.5,
    **kwargs,
):
    """Attempts to call fail-safe providers in the given priority order until one succeeds.

    Args:
        fail_safe_queue: List of tuples containing (provider, model) pairs to try
        messages: Messages for LLM API calls
        prompt: Prompt for text-to-image API calls
        max_tokens: Maximum tokens for LLM responses
        temperature: Temperature parameter for LLM responses
        **kwargs: Additional parameters including:
            - size: Image size for text-to-image (default: "1024x1024")
            - n: Number of images to generate (default: 1)
            - quality: Image quality setting (default: "standard")
            - system: System prompt for Anthropic
    """

    for fail_safe_provider, fail_safe_model in fail_safe_queue:
        try:
            # Handle text-to-image fail-safe if prompt is provided
            if prompt is not None:
                if fail_safe_provider.lower() == "openai":
                    response = text_to_image.call_openai_dalle(
                        model=fail_safe_model,
                        prompt=prompt,
                        size=kwargs.get("size", "1024x1024"),
                        n=kwargs.get("n", 1),
                        quality=kwargs.get("quality", "standard"),
                    )
                    return response  # Return the image URLs if successful
                else:
                    raise ValueError(
                        f"Unsupported text-to-image fail-safe provider: {fail_safe_provider}"
                    )

            # Handle LLM fail-safe if messages is provided
            elif messages is not None:
                if fail_safe_provider.lower() == "openai":
                    response = llm.call_openai_api(
                        model=fail_safe_model,
                        messages=messages,
                        max_tokens=max_tokens,
                        temperature=temperature,
                    )
                    return response  # Return the full response if successful

                elif fail_safe_provider.lower() == "anthropic":
                    system_prompt = kwargs.get("system", "You are a helpful assistant.")
                    response = llm.call_anthropic_api(
                        model=fail_safe_model,
                        system=system_prompt,
                        messages=messages,
                        max_tokens=max_tokens,
                        temperature=temperature,
                    )
                    return (
                        response[0].text
                        if isinstance(response, list)
                        and response
                        and hasattr(response[0], "text")
                        else response
                    )

                else:
                    raise ValueError(
                        f"Unsupported LLM fail-safe provider: {fail_safe_provider}"
                    )

            else:
                raise ValueError(
                    "Either 'messages' (for LLM) or 'prompt' (for text-to-image) must be provided"
                )

        except Exception as fail_safe_error:
            # Log the error and move to the next fail-safe provider in the queue
            print(
                f"\nFail-safe provider '{fail_safe_provider}' failed with error:\n{fail_safe_error}\n"
            )

    # If all fail-safes fail, raise a RuntimeError
    raise RuntimeError("All fail-safe providers have failed.")
