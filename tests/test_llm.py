import sys
sys.path.append("/home/alishchhetri/comp/apicenter")

from apicenter.new_llm import llm


def main():
    """Main function to test universal_api_caller with multiple fail-safe providers."""

    # Minimal prompt format
    response = llm(
        provider="openai",
        model="gpt-4",  # Invalid model to trigger primary provider error
        prompt="Give me a list of 10 animals.",
    )
    print("Final Response (Minimal):\n", response)

    # Detailed prompt format
    response = llm(
        provider="openai",
        model="gpt-4",
        prompt=[{"role": "user", "content": "Give me a list of 10 animals."}],
    )
    print("Final Response (Detailed):\n", response)


if __name__ == "__main__":
    main()
