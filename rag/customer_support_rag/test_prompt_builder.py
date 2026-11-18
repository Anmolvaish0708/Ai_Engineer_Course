
from app.generation.prompt_builder import PromptBuilder


def main():

    builder = PromptBuilder()

    query = "How can I reset my password?"

    context = """
[Document 1 | ID: faq_001]
Customers can reset their password through account settings.
"""

    sources = [
        {
            "id": "faq_001",
            "metadata": {
                "category": "account",
                "source": "account_faq"
            },
            "distance": 0.3719
        }
    ]

    prompt = builder.build_prompt(
        query=query,
        context=context,
        sources=sources
    )

    print("\nGENERATED PROMPT")
    print("-" * 60)
    print(prompt)

    # Basic assertions
    assert query in prompt
    assert "faq_001" in prompt
    assert "account settings" in prompt
    assert "Do not invent facts" in prompt

    print("\nPROMPT VALIDATION PASSED!")

    # Empty context test
    try:
        builder.build_prompt(
            query=query,
            context="",
            sources=[]
        )
    except ValueError as exc:
        print("\nEMPTY CONTEXT TEST PASSED!")
        print(f"Expected error: {exc}")


if __name__ == "__main__":
    main()
