"""
Configuration settings for Agent Court MCP.

Centralizes Azure OpenAI, Tavily, and model settings.
"""

from dotenv import load_dotenv
import os
from openai import AzureOpenAI

# Load environment variables
load_dotenv()

# Azure OpenAI settings
AZURE_OPENAI_KEY = os.getenv("OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_VERSION = "2025-01-01-preview"
AZURE_OPENAI_DEPLOYMENT = "gpt-4o-mini"

# Tavily settings
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Model parameters
MODEL_MAX_TOKENS = 1000
MODEL_TEMPERATURE = 0.7
MODEL_TOP_P = 1.0

# Initialize Azure OpenAI client
client = AzureOpenAI(
    api_version=AZURE_OPENAI_API_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_KEY,
)
