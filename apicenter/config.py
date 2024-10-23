"""Loads environment variables for API keys"""

import os
from dotenv import load_dotenv
import openai

# Explicitly load .env file
load_dotenv()

# Retrieve OpenAI and Anthropic credentials from environment variables
OPENAI_KEY = os.getenv("OPENAI_KEY")  # OpenAI API key
OPENAI_ORG = os.getenv("OPENAI_ORG")  # OpenAI organization ID
ANTHROPIC_KEY = os.getenv("ANTHROPIC_KEY")  # Anthropic API key

# Set up OpenAI credentials
openai.api_key = OPENAI_KEY
openai.organization = OPENAI_ORG

# Debug print statements to verify
# print("OpenAI Key:", OPENAI_KEY)
# print("OpenAI Org:", OPENAI_ORG)
# print("Anthropic Key:", ANTHROPIC_KEY)
