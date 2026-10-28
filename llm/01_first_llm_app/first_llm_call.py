from providers import ask_gemini, ask_openai, ask_groq, PROVIDER


def ask_llm(prompt):
    if PROVIDER == "openai":
        print(f"Provider: {PROVIDER}")
        return ask_openai(prompt)
    elif PROVIDER == "gemini":
        print(f"Provider: {PROVIDER}")
        return ask_gemini(prompt)
    elif PROVIDER == "groq":
        print(f"Provider: {PROVIDER}")
        return ask_groq(prompt)

answer = ask_llm("Hello, how are you?") 
print("Assistant:", answer)   


