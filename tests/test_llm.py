from apicenter.universal_api_caller import apicenter


def main():
    """Main function to test universal_api_caller with OpenAI and Anthropic as fail-safe."""

    # Test with error_message=False (default)
    response = apicenter.llm(
        provider="openai",
        model="gpt-4",  # Invalid model to trigger primary provider error
        messages=[{"role": "user", "content": "Give me a list of 10 animals."}],
        fail_safe=("anthropic", "claude-3-5-konnet-20240620"),  # Fail-safe provider
    )

    print("Final Response:\n", response)


if __name__ == "__main__":
    main()
