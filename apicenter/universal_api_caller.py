"""Universal API caller for OpenAI, Anthropic, and image generation models"""

from apicenter.llm import LLM
from apicenter.text_to_image import TextToImage
from apicenter.fail_safe_handler import fail_safe_handler


class UniversalAPICaller:
    """Handles both LLM and text-to-image API calls"""

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
        """Calls the specified LLM API (OpenAI or Anthropic) with the given configuration."""

        llm = LLM()

        try:
            if provider.lower() == "openai":
                response = llm.call_openai_api(
                    model=model,
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=temperature,
                )
                return response

            elif provider.lower() == "anthropic":
                system_prompt = kwargs.get("system", "You are a helpful assistant.")
                response = llm.call_anthropic_api(
                    model=model,
                    system=system_prompt,
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=temperature,
                )

                return (
                    response[0].text
                    if isinstance(response, list) and hasattr(response[0], "text")
                    else response
                )

        except Exception as primary_error:
            print(
                f"\nPrimary provider '{provider}' encountered an error:\n{primary_error}\n"
            )

            # Convert fail_safe parameter into a queue of providers to try
            if fail_safe:
                fail_safe_queue = (
                    fail_safe if isinstance(fail_safe, list) else [fail_safe]
                )
                print("Attempting fail-safe providers in priority order...\n")
                # Pass down all relevant parameters to fail_safe_handler
                return fail_safe_handler(
                    fail_safe_queue,
                    messages,
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
        """Calls the specified text-to-image API (like DALL-E) with the given configuration."""

        text_to_image = TextToImage()

        try:
            if provider.lower() == "openai":
                return text_to_image.call_openai_dalle(
                    model=model, prompt=prompt, size=size, n=n, quality=quality
                )

        except Exception as primary_error:
            print(
                f"\nPrimary provider '{provider}' encountered an error:\n{primary_error}\n"
            )

            if fail_safe:
                fail_safe_queue = (
                    fail_safe if isinstance(fail_safe, list) else [fail_safe]
                )
                print("Attempting fail-safe providers in priority order...\n")
                return fail_safe_handler(
                    fail_safe_queue,
                    prompt=prompt,
                    size=size,
                    n=n,
                    quality=quality,
                )

            raise primary_error


# Create an instance of UniversalAPICaller
apicenter = UniversalAPICaller()
