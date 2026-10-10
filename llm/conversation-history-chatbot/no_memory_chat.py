import config
import llm_client

EXIT_COMMANDS = ["exit", "quit"]


def build_messages(user_input: str) -> list[dict]:
    """Build the message list for a single question.

    Notice what is missing: the previous questions and answers. Only the
    system instruction and the current question are sent.

    Args:
        user_input: The question the user just typed.

    Returns:
        A list with exactly two messages.

    Example:
        >>> build_messages("Hello")[-1]
        {'role': 'user', 'content': 'Hello'}
    """
    return [
        {"role": "system", "content": config.SYSTEM_PROMPT},
        {"role": "user", "content": user_input},
    ]


def main() -> None:
    """Run the chat loop until the user types 'exit' or 'quit'."""
    print("Chatbot WITHOUT memory")
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
            print(f"Sorry, something went wrong: {error}\n")
            continue

        print(f"Assistant: {reply}\n")


if __name__ == "__main__":
    main()