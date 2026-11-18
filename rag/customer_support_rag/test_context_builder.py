
from app.retrieval.context_builder import ContextBuilder


def main():

    builder = ContextBuilder()

    retrieved_documents = [
        {
            "id": "faq_001",
            "document": (
                "Customers can reset their password "
                "through account settings."
            ),
            "metadata": {
                "category": "account",
                "source": "account_faq"
            },
            "distance": 0.3719
        },
        {
            "id": "faq_002",
            "document": "Orders can be tracked using the tracking link.",
            "metadata": {
                "category": "orders",
                "source": "order_faq"
            },
            "distance": 0.8778
        }
    ]

    result = builder.build_context(retrieved_documents)

    print("\nFORMATTED CONTEXT")
    print("-" * 50)
    print(result["context"])

    print("\nSOURCE REFERENCES")
    print("-" * 50)
    for source in result["sources"]:
        print(source)

    # Basic assertions
    assert len(result["sources"]) == 2
    assert "Document 1" in result["context"]
    assert "Document 2" in result["context"]
    assert result["sources"][0]["id"] == "faq_001"

    # Empty input test
    empty_result = builder.build_context([])

    assert empty_result == {
        "context": "",
        "sources": []
    }

    print("\nALL CONTEXT BUILDER TESTS PASSED!")


if __name__ == "__main__":
    main()
