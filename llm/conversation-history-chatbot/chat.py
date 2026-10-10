import config
import llm_client
import memory

EXIT_COMMANDS = ["exit", "quit"]

def build_messages(user_input: str) -> list[dict]:
    messages = [{"role": "system", "content": config.SYSTEM_PROMPT}]    
    messages.extend(memory.get_history())
    messages.append({"role": "user", "content": user_input})

    return messages

def main() -> None:
    """Run the chat loop until the user types 'exit' or 'quit'."""
    print("Chatbot WITH memory")
    print(f"Provider: {config.LLM_PROVIDER}")
    print("Type 'exit' or 'quit' to stop.\n")

    configuration_error = config.get_configuration_error()
    if configuration_error:
        print(f"Configuration problem: {configuration_error}")
        return

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            return

        if not user_input:
            print("Please type a question.\n")
            continue

        if user_input.lower() in EXIT_COMMANDS:
            print("Goodbye!")
            return

        try:
            reply = llm_client.get_llm_response(build_messages(user_input))
        except Exception as error:
            # Nothing is saved when the call fails, so the stored conversation
            # never contains a question without its answer.
            print(f"Sorry, something went wrong: {error}\n")
            continue

        # Only now, after a successful reply, do we remember this exchange.
        memory.add_user_message(user_input)
        memory.add_assistant_message(reply)

        print(f"Assistant: {reply}\n")


if __name__ == "__main__":
    main()