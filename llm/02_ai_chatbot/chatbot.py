import os
from dotenv import load_dotenv

from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)
while True:
    user_input = input("You: ")

    if user_input.lower() in ["exit", "quit", "bye"]:
        print("Good Bye!")
        break

    if not user_input:
        print("Kindly Enter the prompt...")
        continue

    response = client.chat.completions.create(
        model= "openai/gpt-oss-20b",

        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },

            {
                "role": "user",
                "content": user_input
            }
        ]
    )

    print("AI: ", response.choices[0].message.content)