from app.generation.llm_client import LLMClient

llm = LLMClient()

prompt = """
You are a customer support assistant.
Explain how a customer can reset their password.
"""

response = llm.generate(prompt)

print("Provider:", llm.provider)
print("Model:", llm.model)
print("Response:", response)