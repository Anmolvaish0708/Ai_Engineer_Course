
from uuid import uuid4
from pathlib import Path

from app.ingestion.document_loader import DocumentLoader
from app.ingestion.document_chunker import DocumentChunker
from app.ingestion.ingestion_pipeline import IngestionPipeline
from app.embeddings.embedding_generator import EmbeddingGenerator
from app.vector_store.chroma_store import ChromaStore


def main():

    # 1. Initialize components
    loader = DocumentLoader()

    chunker = DocumentChunker(
        chunk_size=100,
        chunk_overlap=20
    )

    embedding_generator = EmbeddingGenerator()

    # Use a separate database directory for integration tests
    db_path = Path("chroma_db") / "integration_tests"
    store = ChromaStore(db_path=db_path)

    # Create a unique collection for this test run
    collection_name = f"ingestion_test_{uuid4().hex[:8]}"

    pipeline = IngestionPipeline(
        document_loader=loader,
        document_chunker=chunker,
        embedding_generator=embedding_generator,
        vector_store=store,
        collection_name=collection_name
    )

    try:
        # 2. Prepare sample documents
        raw_documents = [
            "Customers can reset their password through account settings.",
            "Customers can track their orders through the order history page.",
            "Refunds are generally processed within five to seven business days."
        ]

        # 3. Run the complete ingestion pipeline
        result = pipeline.ingest(raw_documents)

        print("\nINGESTION SUMMARY")
        print("-" * 40)

        for key, value in result.items():
            print(f"{key}: {value}")

        # 4. Verify the ingestion results
        assert result["document_count"] == len(raw_documents)
        assert result["chunk_count"] > 0
        assert result["embedding_count"] == result["chunk_count"]
        assert len(result["ids"]) == result["chunk_count"]
        assert len(set(result["ids"])) == len(result["ids"])

        # 5. Verify that documents were actually stored
        stored_data = store.get_documents(result["ids"])

        assert stored_data["ids"] == result["ids"]
        assert len(stored_data["documents"]) == result["chunk_count"]

        print("\nVERIFICATION")
        print("-" * 40)
        print("Document count verified.")
        print("Chunk count verified.")
        print("Embedding count verified.")
        print("Unique IDs verified.")
        print("Stored documents verified.")

        # 6. Test retrieval using a real query
        query = "How can I reset my password?"

        query_embedding = embedding_generator.generate_query_embedding(
            query
        )

        search_results = store.search(
            query_embedding=query_embedding,
            n_results=3
        )

        print("\nRETRIEVAL TEST")
        print("-" * 40)

        for document_id, document, distance in zip(
            search_results["ids"][0],
            search_results["documents"][0],
            search_results["distances"][0]
        ):
            print(f"ID: {document_id}")
            print(f"Document: {document}")
            print(f"Distance: {distance:.4f}")
            print("-" * 30)

        assert search_results["ids"][0], "No documents were retrieved."

        print("\nEND-TO-END INGESTION TEST PASSED!")

    finally:
        # Remove the temporary collection after the test
        try:
            store.client.delete_collection(name=collection_name)
        except Exception:
            pass


if __name__ == "__main__":
    main()
