"""
Basic usage examples for APICenter.

This example demonstrates the universal API pattern for different AI providers.
The key concept is that all providers follow the same basic structure:
    apicenter.<mode>(
        provider="provider_name",
        model="model_name",
        prompt="your prompt",
        **kwargs  # Provider-specific parameters
    )
"""

from apicenter import apicenter
import json
import time


def basic_examples():
    """Basic text generation examples."""
    print("\n=== BASIC TEXT GENERATION EXAMPLES ===")
    
    # # OpenAI example
    # try:
    #     response = apicenter.text(
    #         provider="openai",
    #         model="gpt-3.5-turbo",
    #         prompt="Explain what a neural network is in one paragraph."
    #     )
    #     print("\nOpenAI Basic Response:")
    #     print(response)
    # except Exception as e:
    #     print(f"\nError with OpenAI: {e}")
    
    # # Anthropic example
    # try:
    #     response = apicenter.text(
    #         provider="anthropic",
    #         model="claude-3-haiku-20240307",
    #         prompt="List 5 interesting facts about dolphins."
    #     )
    #     print("\nAnthropic Basic Response:")
    #     print(response)
    # except Exception as e:
    #     print(f"\nError with Anthropic: {e}")
    
    # Ollama example (local model)
    try:
        response = apicenter.text(
            provider="ollama",
            model="deepseek-r1",  # Change to any model you've pulled locally
            prompt="List 5 animals"
        )
        print("\nOllama Basic Response:")
        print(response)
    except Exception as e:
        print(f"\nError with Ollama: {e}")
        print("Note: Make sure Ollama is installed and running locally.")
        print("You can install it from https://ollama.ai/ and pull models with 'ollama pull <model>'")


def chat_conversation_example():
    """Example of having a multi-turn conversation."""
    print("\n=== CHAT CONVERSATION EXAMPLE ===")
    
    # Example conversation with OpenAI
    try:
        messages = [
            {"role": "system", "content": "You are a helpful assistant that specializes in science."},
            {"role": "user", "content": "What is the difference between fusion and fission?"}
        ]
        
        # First response
        response = apicenter.text(
            provider="openai",
            model="gpt-4",
            prompt=messages
        )
        print("\nAssistant:", response)
        
        # Add response to messages and continue conversation
        messages.append({"role": "assistant", "content": response})
        messages.append({"role": "user", "content": "Which one is used in nuclear power plants?"})
        
        # Second response
        response = apicenter.text(
            provider="openai",
            model="gpt-4",
            prompt=messages
        )
        print("\nUser: Which one is used in nuclear power plants?")
        print("Assistant:", response)
    except Exception as e:
        print(f"\nError with chat conversation: {e}")


def ollama_examples():
    """Examples showcasing Ollama local models."""
    print("\n=== OLLAMA LOCAL MODEL EXAMPLES ===")
    
    # Basic Ollama example
    try:
        # List available models (requires Ollama to be running)
        print("\nTo list available Ollama models, run in terminal: 'ollama list'")
        
        # Simple prompt with deepseek-r1
        response = apicenter.text(
            provider="ollama",
            model="deepseek-r1",  # Change to any model you have locally
            prompt="Explain the concept of recursion in programming."
        )
        print("\ndeepseek-r1 Response:")
        print(response)
        
        # With custom parameters
        response = apicenter.text(
            provider="ollama",
            model="deepseek-r1",
            prompt="Write a short poem about AI.",
            temperature=0.9,  # Higher temperature for more creative output
            num_predict=150,  # Control response length
        )
        print("\ndeepseek-r1 Creative Response (with custom params):")
        print(response)
        
        # Chat conversation with Ollama
        messages = [
            {"role": "user", "content": "What are the three laws of robotics?"}
        ]
        response = apicenter.text(
            provider="ollama",
            model="deepseek-r1",
            prompt=messages
        )
        print("\nOllama Chat Response:")
        print(response)
        
        # Continue the conversation
        messages.append({"role": "assistant", "content": response})
        messages.append({"role": "user", "content": "Who created these laws?"})
        response = apicenter.text(
            provider="ollama",
            model="deepseek-r1",
            prompt=messages
        )
        print("\nUser: Who created these laws?")
        print("Assistant:", response)
    except Exception as e:
        print(f"\nError with Ollama: {e}")
        print("Note: Make sure Ollama is installed and running.")
        print("You can install it from https://ollama.ai/")
        print("Then pull the model with: 'ollama pull deepseek-r1'")


def structured_output_example():
    """Example of generating structured output from LLMs."""
    print("\n=== STRUCTURED OUTPUT EXAMPLE ===")
    
    try:
        # Request JSON response
        prompt = """
        Generate a JSON object representing a fictional person with the following fields:
        - name
        - age
        - occupation
        - skills (array)
        - contact (object with email and phone)
        
        Respond with only the JSON object, no additional text.
        """
        
        response = apicenter.text(
            provider="openai",
            model="gpt-3.5-turbo",
            prompt=prompt
        )
        
        # Parse the response as JSON
        try:
            parsed = json.loads(response)
            print("\nStructured JSON output:")
            print(json.dumps(parsed, indent=2))
        except json.JSONDecodeError:
            print("\nResponse couldn't be parsed as JSON:")
            print(response)
    except Exception as e:
        print(f"\nError with structured output: {e}")


def main():
    """Run all LLM examples."""
    print("APICenter LLM Examples")
    print("======================")
    
    # Run examples
    basic_examples()
    # chat_conversation_example()
    # ollama_examples()
    # structured_output_example()
    
    print("\nAll LLM examples completed!")


if __name__ == "__main__":
    main() 