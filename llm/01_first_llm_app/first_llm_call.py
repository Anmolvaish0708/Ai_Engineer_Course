import os

from dotenv import load_dotenv
from openai import OpenAI
from groq import Groq

# Load variables from .env file so the API key stays out of the source code.
load_dotenv()

# openai sdk

# API_KEY = os.getenv("OPENAI_API_KEY")

# # create an OpenAI client using the API key from the .env file
# client = OpenAI(api_key=API_KEY)

# # Make a call to the OpenAI API using the Responses API.
# response = client.responses.create(
#     model = "gpt-4o-mini",
#     input = "Write a short poem about a cat who loves to play with yarn."
# )

# # Print the output text from the response.
# print(response.output_text)

# groq sdk
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# create a Groq client using the API key from the .env file
# client = Groq(api_key=GROQ_API_KEY)

# response = client.chat.completions.create(
#     model = "openai/gpt-oss-20b",

#     messages = [
#          {
#              "role": "system",
#              "content": "You are a senior Python engineer. Explain concepts using production examples."
#          },
#          {
#              "role" : "user",
#              "content": "Explain python decorators with examples."
#          }
#     ]
# )

# max_completion_tokens is the maximum number of tokens that can be generated in the response. It limits the length of the output. If you set it too low, you might get incomplete answers. If you set it too high, you might get unnecessarily long responses.

# response = client.chat.completions.create(
#     model="openai/gpt-oss-20b",
#     max_completion_tokens=200,
#     messages=[
#         {
#             "role": "user",
#             "content": "explain python decorators with examples."
#         }
#     ]
# )

# print(response.choices[0].message.content)

# google-genai sdk

from google import genai

client = genai.Client()

response = client.models.generate_content(
    model = "gemini-3.1-flash-lite",
    contents = "Explain python decorators with examples."
)

print(response.text)