import os
from dotenv import load_dotenv

from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)

conversation_history = []

while True:
    user_input = input("You: ")

    if user_input.lower() in ["exit", "quit", "bye"]:
        print("Good Bye!")
        break

    if not user_input:
        print("Kindly Enter the prompt...")
        continue

    conversation_history.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model= "openai/gpt-oss-20b",

        messages=conversation_history
    )

    assistant_response = response.choices[0].message.content
    conversation_history.append({"role": "assistant", "content": assistant_response})

    print("AI: ", assistant_response)