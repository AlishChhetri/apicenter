"""
Advanced Chat Examples for APICenter

This example demonstrates how to use structured message formats with APICenter,
including system prompts and conversation history with different providers.
"""

from apicenter import apicenter
import requests
import os
from pathlib import Path
import json

# Create examples/outputs directory if it doesn't exist
OUTPUTS_DIR = Path(__file__).parent / "outputs"
OUTPUTS_DIR.mkdir(exist_ok=True)


def save_conversation(provider: str, conversation: list, responses: list) -> None:
    """Save conversation and responses to JSON file."""
    # Create a conversation record
    convo_record = {"provider": provider, "messages": conversation, "responses": responses}

    # Save to file
    with open(OUTPUTS_DIR / f"{provider}_conversation.json", "w") as f:
        json.dump(convo_record, f, indent=2)
    print(f"Conversation saved to {OUTPUTS_DIR}/{provider}_conversation.json")


def openai_advanced_chat():
    """Advanced OpenAI chat examples with system prompts."""
    print("\n=== OPENAI ADVANCED CHAT EXAMPLES ===\n")

    try:
        # Basic chat with system prompt
        prompt = [
            {
                "role": "system",
                "content": "You are a helpful assistant specialized in science. Keep answers brief.",
            },
            {"role": "user", "content": "Explain black holes in simple terms"},
        ]

        response = apicenter.text(
            provider="openai", model="gpt-4", prompt=prompt, temperature=0.7, max_tokens=250
        )
        print("OpenAI with system prompt:")
        print(response)
        print("\n" + "-" * 50 + "\n")

        # Save system prompt example
        with open(OUTPUTS_DIR / "openai_blackholes.txt", "w") as f:
            f.write(response)

        # Multi-turn conversation
        messages = [
            {
                "role": "system",
                "content": "You are a helpful coding assistant. Provide concise answers with code examples.",
            },
            {"role": "user", "content": "How do I read a file in Python?"},
        ]

        # Collect conversation for saving
        all_responses = []

        response = apicenter.text(provider="openai", model="gpt-4", prompt=messages)
        print("OpenAI first response:")
        print(response)
        all_responses.append(response)

        # Continue the conversation
        messages.append({"role": "assistant", "content": response})
        messages.append(
            {"role": "user", "content": "How would I modify this to read only the first 10 lines?"}
        )

        response = apicenter.text(provider="openai", model="gpt-4", prompt=messages)
        print("\nUser: How would I modify this to read only the first 10 lines?")
        print("OpenAI follow-up response:")
        print(response)
        all_responses.append(response)

        # Save the full conversation
        save_conversation("openai", messages, all_responses)

    except Exception as e:
        print(f"Error with OpenAI examples: {e}")


def anthropic_advanced_chat():
    """Advanced Anthropic chat examples with system prompts."""
    print("\n=== ANTHROPIC ADVANCED CHAT EXAMPLES ===\n")

    try:
        # Basic chat with system prompt
        prompt = [
            {
                "role": "system",
                "content": "You are a helpful assistant that explains complex topics simply. Your audience is 10-year-old children.",
            },
            {"role": "user", "content": "What is quantum physics?"},
        ]

        response = apicenter.text(
            provider="anthropic",
            model="claude-3-sonnet-20240229",
            prompt=prompt,
            temperature=0.3,
            max_tokens=300,
        )
        print("Anthropic with system prompt:")
        print(response)
        print("\n" + "-" * 50 + "\n")

        # Save system prompt example
        with open(OUTPUTS_DIR / "anthropic_quantum.txt", "w") as f:
            f.write(response)

        # Multi-turn conversation
        messages = [
            {
                "role": "system",
                "content": "You are a friendly history teacher. Provide engaging, accurate, and educational responses.",
            },
            {"role": "user", "content": "Tell me about Ancient Egypt."},
        ]

        # Collect conversation for saving
        all_responses = []

        response = apicenter.text(
            provider="anthropic", model="claude-3-sonnet-20240229", prompt=messages, max_tokens=350
        )
        print("Anthropic first response:")
        print(response)
        all_responses.append(response)

        # Continue the conversation
        messages = [
            {
                "role": "system",
                "content": "You are a friendly history teacher. Provide engaging, accurate, and educational responses.",
            },
            {"role": "user", "content": "Tell me about Ancient Egypt."},
            {"role": "assistant", "content": response},
            {"role": "user", "content": "What were their religious beliefs?"},
        ]

        response = apicenter.text(
            provider="anthropic", model="claude-3-sonnet-20240229", prompt=messages, max_tokens=350
        )
        print("\nUser: What were their religious beliefs?")
        print("Anthropic follow-up response:")
        print(response)
        all_responses.append(response)

        # Save the full conversation
        save_conversation("anthropic", messages, all_responses)

    except Exception as e:
        print(f"Error with Anthropic examples: {e}")


def ollama_advanced_chat():
    """Advanced Ollama chat examples with structured messages."""
    print("\n=== OLLAMA ADVANCED CHAT EXAMPLES ===\n")

    try:
        # Basic chat with system-like instruction
        # Note: Some Ollama models handle system prompts differently
        prompt = [
            {
                "role": "system",
                "content": "You are a helpful assistant specializing in computer programming.",
            },
            {"role": "user", "content": "Explain what recursion is in programming."},
        ]

        response = apicenter.text(
            provider="ollama",
            model="llama2",  # Use any model you have locally
            prompt=prompt,
        )
        print("Ollama with system instruction:")
        print(response)
        print("\n" + "-" * 50 + "\n")

        # Save system prompt example
        with open(OUTPUTS_DIR / "ollama_recursion.txt", "w") as f:
            f.write(response)

        # Multi-turn conversation
        messages = [{"role": "user", "content": "What are the three laws of robotics?"}]

        # Collect conversation for saving
        all_responses = []

        response = apicenter.text(provider="ollama", model="llama2", prompt=messages)
        print("Ollama first response:")
        print(response)
        all_responses.append(response)

        # Continue the conversation
        messages.append({"role": "assistant", "content": response})
        messages.append({"role": "user", "content": "Who created these laws?"})

        response = apicenter.text(provider="ollama", model="llama2", prompt=messages)
        print("\nUser: Who created these laws?")
        print("Ollama follow-up response:")
        print(response)
        all_responses.append(response)

        # Save the full conversation
        save_conversation("ollama", messages, all_responses)

    except Exception as e:
        print(f"Error with Ollama examples: {e}")


if __name__ == "__main__":
    print("APICenter Advanced Chat Examples")
    print("===============================")
    print("This demonstrates advanced chat capabilities with different providers.")
    print(f"All outputs will be saved to the '{OUTPUTS_DIR}' directory.")

    openai_advanced_chat()
    anthropic_advanced_chat()
    ollama_advanced_chat()

    print("\nAll examples completed!")
