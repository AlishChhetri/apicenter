import sys

sys.path.append("/home/alishchhetri/comp/apicenter")

from apicenter.new_text_to_image import text_to_image


def main():
    """Main function to test universal_api_caller with multiple fail-safe providers."""

    # Minimal prompt format
    response = text_to_image(
        provider="openai",
        model="dall-e-3",
        prompt="a cute puppy",
    )
    print("Generated Image URL(s):\n", response)


if __name__ == "__main__":
    main()
