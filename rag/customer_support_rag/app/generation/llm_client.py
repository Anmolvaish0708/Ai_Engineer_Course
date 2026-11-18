import os

from dotenv import load_dotenv
from openai import OpenAI
from google import genai
from groq import Groq

class LLMClient:
    """Client for interacting with different LLM providers."""

    def __init__(self):
        load_dotenv()

        self.provider = os.getenv("LLM_PROVIDER", "openai").lower().strip()

        self.providers = {
            "openai": {
                "api_key": os.getenv("OPENAI_API_KEY"),
                "model":  os.getenv("OPENAI_MODEL")
            },
            "gemini": {
                "api_key": os.getenv("GEMINI_API_KEY"),
                "model":  os.getenv("GEMINI_MODEL")
            },
            "groq": {
                "api_key": os.getenv("GROQ_API_KEY"),
                "model":  os.getenv("GROQ_MODEL")
            },
            "mistral": {
                "api_key": os.getenv("MISTRAL_API_KEY"),
                "model":  os.getenv("MISTRAL_MODEL")
            }
        }

        if self.provider not in self.providers:
            raise ValueError(
                f"Unsupported provider: {self.provider}"
                f"Supported providers: {list(self.providers.keys())}"
         )

        config = self.providers[self.provider]

        self.api_key = config["api_key"]
        self.model = config["model"]

        if not self.api_key:
            raise ValueError(f"{self.provider.upper()}_API_KEY is missing in .env")

        if not self.model:
            raise ValueError(f"{self.provider.upper()}_MODEL is missing in .env")

        self.client = self._initialize_client()

    def _initialize_client(self):

        try:
            if self.provider == "openai":
                return OpenAI(api_key=self.api_key)

            elif self.provider == "gemini":
                return genai.Client(api_key=self.api_key)

            elif self.provider == "groq":
                return Groq(api_key=self.api_key)

            elif self.provider == "mistral":
                # Placeholder for Mistral client initialization
                pass

        except Exception as e:
            raise RuntimeError(f"Failed to initialize {self.provider} client: {e}")

    def generate(self, prompt):
        """Generate a response from the selected LLM provider."""    

        if not isinstance(prompt, str):
            raise ValueError("Prompt must be a string.")

        if not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        try:
            if self.provider == "openai":
                response = self.client.chat.completions.create(
                    model = self.model,
                    messages = [
                        {"role": "user", "content": prompt}
                    ]
                )

                answer = response.choices[0].message.content 

            elif self.provider == "gemini":
                response = self.client.models.generate_content(
                    model = self.model,
                    contents = prompt
                ) 

                answer = response.text

            elif self.provider == "groq":
                response = self.client.chat.completions.create(
                    model = self.model,
                    messages = [
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens = 500,
                    temperature = 0.2
                ) 

                answer = response.choices[0].message.content  

            if not isinstance(answer, str) or not answer.strip():
                raise ValueError("Received an invalid or empty response from the LLM.")

            return answer.strip()

        except Exception as e:
            raise RuntimeError(f"Failed to generate response from {self.provider}: {e}")           


