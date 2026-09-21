"""
Configuration module for the Day 1 Assessment project.
Configures the OpenAI-compatible client to connect to Groq API.
Loads credentials strictly from environment variables or a local .env file.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables from local .env file if present
load_dotenv()

# Groq API Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_BASE_URL = os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1")

# Configurable Groq model (defaults to llama-3.3-70b-versatile, which natively supports tool calling)
MODEL = os.getenv("MODEL", "llama-3.3-70b-versatile")


def get_groq_client():
    """
    Initializes and returns an OpenAI client configured for the Groq endpoint.
    Raises a clean, descriptive RuntimeError if GROQ_API_KEY is not set.
    """
    try:
        from openai import OpenAI
    except ImportError:
        raise ImportError("The 'openai' package is not installed. Please run: pip install -r requirements.txt")

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or not api_key.strip():
        print("\n" + "=" * 60)
        print("ERROR: GROQ_API_KEY is missing or empty!")
        print("=" * 60)
        print("Please set your GROQ_API_KEY in a local .env file:")
        print("    GROQ_API_KEY=your_actual_groq_api_key_here")
        print("Or set it as an environment variable in your terminal:")
        print("    $env:GROQ_API_KEY='your_actual_groq_api_key_here' (PowerShell)")
        print("=" * 60 + "\n")
        raise RuntimeError("Missing GROQ_API_KEY environment variable.")

    client = OpenAI(
        api_key=api_key.strip(),
        base_url=GROQ_BASE_URL,
    )
    return client
