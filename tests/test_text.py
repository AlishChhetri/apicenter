from apicenter import apicenter


def main():
    """Main function to test text providers."""
    response = apicenter.text(
        provider="anthropic",
        model="claude-3-sonnet-20240229",
        prompt="Give me a list of 5 animals.",
    )
    print("Final Response (Minimal anthropic):\n", response)


if __name__ == "__main__":
    main()
