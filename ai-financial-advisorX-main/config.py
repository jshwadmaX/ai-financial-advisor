import os
import google.generativeai as genai
from dotenv import load_dotenv

def configure_gemini():
    """
    In config.py, implement environment configuration logic to load the Gemini API key.
    Ensure that API keys are never hardcoded and are always retrieved via environment variables.
    """
    load_dotenv()
    
    # Retrieve API key from environment variable
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        # Set OS environment variable
        os.environ["GEMINI_API_KEY"] = api_key
        # Configure Gemini
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        return True
    return False

# Automatically configure on module import
configure_gemini()
