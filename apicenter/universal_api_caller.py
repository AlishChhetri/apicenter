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
            print(f"\nPrimary provider '{provider}' encountered an error:\n")
            print(f"{primary_error}\n")
            if fail_safe:
                fail_safe_provider, fail_safe_model = fail_safe
                print(
                    f"Attempting fail-safe with provider '{fail_safe_provider}' ({fail_safe_model})...\n"
                )
                return fail_safe_handler(
                    fail_safe_provider,
                    fail_safe_model,
                    messages,
                    max_tokens,
                    temperature,
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
            # Enhanced formatting for clearer separation of the error components
            print(f"\nPrimary provider '{provider}' encountered an error:\n")
            print(
                f"Error code: {getattr(primary_error, 'code', 'Unknown')} - {primary_error}\n"
            )

            if fail_safe:
                fail_safe_provider, fail_safe_model = fail_safe
                print(
                    f"Attempting fail-safe with provider '{fail_safe_provider}' ({fail_safe_model})...\n"
                )
                return fail_safe_handler(
                    fail_safe_provider,
                    fail_safe_model,
                    prompt=prompt,
                    size=size,
                    n=n,
                    quality=quality,
                )

            raise primary_error


# Create an instance of UniversalAPICaller
apicenter = UniversalAPICaller()
