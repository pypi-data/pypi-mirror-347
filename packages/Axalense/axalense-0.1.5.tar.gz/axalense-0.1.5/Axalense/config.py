import os

def get_groq_api_key():
    key = os.getenv("GROQ_API_KEY")
    if not key:
        raise ValueError("GROQ_API_KEY is not set. Please set it as an environment variable.")
    return key
