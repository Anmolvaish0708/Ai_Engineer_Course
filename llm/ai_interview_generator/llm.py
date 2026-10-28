import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")


def ask_llm(prompt):
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model = "openai/gpt-oss-20b",
        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return response.choices[0].message.content