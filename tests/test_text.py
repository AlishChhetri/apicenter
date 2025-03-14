import sys
import os

# Add the project root directory to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from apicenter.text.text import text


def main():
    """Main function to test text providers."""
    response = text(
        provider="anthropic",
        model="claude-3-sonnet-20240229",
        prompt="Give me a list of 5 animals.",
    )
    print("Final Response (Minimal anthropic):\n", response)


if __name__ == "__main__":
    main()
