"""Fail-safe handler to switch to an alternate provider if the primary one fails"""

from apicenter.llm import LLM

llm = LLM()


def fail_safe_handler(
    fail_safe_queue, messages, max_tokens=100, temperature=0.5, **kwargs
):
    """Attempts to call fail-safe providers in the given priority order until one succeeds."""

    for fail_safe_provider, fail_safe_model in fail_safe_queue:
        try:
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
                    f"Unsupported fail-safe provider: {fail_safe_provider}"
                )

        except Exception as fail_safe_error:
            # Log the error and move to the next fail-safe provider in the queue
            print(
                f"\nFail-safe provider '{fail_safe_provider}' failed with error:\n{fail_safe_error}\n"
            )

    # If all fail-safes fail, raise a RuntimeError
    raise RuntimeError("All fail-safe providers have failed.")
