
from app.embeddings.embedding_generator import EmbeddingGenerator
from app.vector_store.chroma_store import ChromaStore
from app.retrieval.retriever import Retriever


def main():

    embedding_generator = EmbeddingGenerator()

    store = ChromaStore()

    # Reuse the collection populated by your earlier
    # retrieval evaluation experiments.
    retriever = Retriever(
        embedding_generator=embedding_generator,
        vector_store=store,
        collection_name="customer_support"
    )

    query = "I forgot my password. How can I access my account?"

    results = retriever.retrieve(
        query=query,
        top_k=3
    )

    print("\nRETRIEVAL RESULTS")
    print("-" * 50)

    if not results:
        print("No relevant documents found.")

    for index, result in enumerate(results, start=1):
        print(f"\nResult {index}")
        print(f"ID: {result['id']}")
        print(f"Document: {result['document']}")
        print(f"Metadata: {result['metadata']}")
        print(f"Distance: {result['distance']:.4f}")


if __name__ == "__main__":
    main()
