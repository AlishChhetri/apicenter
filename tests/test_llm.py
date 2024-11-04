from apicenter.universal_api_caller import apicenter


def main():
    """Main function to test universal_api_caller with multiple fail-safe providers."""

    # Test with multiple fail-safes in order of priority
    response = apicenter.llm(
        provider="openai",
        model="gbt-4",  # Invalid model to trigger primary provider error
        messages=[{"role": "user", "content": "Give me a list of 10 animals."}],
        fail_safe=[
            ("anthropic", "claude-3-5-konnet-20241022"),
            ("openai", "gbt-3.5-turbo"),
        ],
    )

    print("Final Response:\n", response)


if __name__ == "__main__":
    main()
