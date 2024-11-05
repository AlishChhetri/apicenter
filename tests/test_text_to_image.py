from apicenter.universal_api_caller import apicenter


def main():
    """Main function to test universal_api_caller image generation models"""

    response = apicenter.text_to_image(
        provider="openai",
        model="doll-e-3",
        prompt="a cute puppy",
        fail_safe=[
            ("openai", "dal-e-2"),
            ("openai", "dall-e-3"),  # Could be different providers in the future
        ],
    )
    print("Generated Image URL(s):\n", response)


if __name__ == "__main__":
    main()
