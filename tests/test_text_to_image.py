from apicenter.universal_api_caller import apicenter


def main():
    """Main function to test universal_api_caller image generation models"""

    image_response = apicenter.text_to_image(
        provider="openai",
        model="doll-e-3",  # DALL-E model
        prompt="A cute corgi playing with a cat",
    )
    print("Generated Image URL(s):\n", image_response)


if __name__ == "__main__":
    main()
