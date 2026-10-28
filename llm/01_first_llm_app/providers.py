from google import genai
from openai import OpenAI
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

PROVIDER = os.getenv("LLM_PROVIDER", "gemini")

def ask_openai(message):
    """Send one message to OpenAI and return the answer as text."""
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.responses.create(
        model="gpt-4o-mini",
        input=message,
    )
    return response.output_text

def ask_gemini(message):
    """Send one message to Google Gemini and return the answer as text."""
    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=message
    )
    return response.text  

def ask_groq(message):
    """Send one message to Groq and return the answer as text."""
    client = Groq(api_key=GROQ_API_KEY)
    response = client.chat.completions.create(
        model = "openai/gpt-oss-20b",
        messages= [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": message
            }
        ]
    )
    return response.choices[0].message.content