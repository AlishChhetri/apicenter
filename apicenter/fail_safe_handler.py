"""Fail-safe handler to switch to an alternate provider if the primary one fails"""

from apicenter.llm import LLM

llm = LLM()


def fail_safe_handler(
    fail_safe_provider, fail_safe_model, messages, max_tokens, temperature, **kwargs
):
    """Attempts to call the fail-safe provider if the primary provider fails."""

    try:
        if fail_safe_provider.lower() == "openai":
            response = llm.call_openai_api(
                model=fail_safe_model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
            )
            return response  # Return the full response from fail-safe

        elif fail_safe_provider.lower() == "anthropic":
            system_prompt = kwargs.get("system", "You are a helpful assistant.")
            response = llm.call_anthropic_api(
                model=fail_safe_model,
                system=system_prompt,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
            )

            # Return the text of the first item if response is a list
            return (
                response[0].text
                if isinstance(response, list)
                and response
                and hasattr(response[0], "text")
                else response
            )

        else:
            raise ValueError(f"Unsupported fail-safe provider: {fail_safe_provider}")

    except Exception as fail_safe_error:
        # Print the error from fail-safe provider before raising the RuntimeError
        print(
            f"\nFail-safe provider '{fail_safe_provider}' also encountered an error:\n"
        )
        print(
            f"{fail_safe_error}\n"
        )  # This will print the error message (e.g., `anthropic.NotFoundError`)

        # Raise the exception with the error message
        raise RuntimeError(
            f"Fail-safe provider '{fail_safe_provider}' also failed with error: {fail_safe_error}"
        )
