
from uuid import uuid4


class IngestionPipeline:
    """Orchestrates the complete document ingestion workflow."""

    def __init__(
        self,
        document_loader,
        document_chunker,
        embedding_generator,
        vector_store,
        collection_name="customer_support"
    ):
        self.document_loader = document_loader
        self.document_chunker = document_chunker
        self.embedding_generator = embedding_generator
        self.vector_store = vector_store
        self.collection_name = collection_name

    def ingest(self, raw_documents):
        """Load, chunk, embed and store documents."""

        # 1. Load and clean documents
        documents = self.document_loader.load_documents(
            raw_documents
        )

        # 2. Split documents into chunks
        chunks = self.document_chunker.chunk_documents(
            documents
        )

        # 3. Generate unique IDs
        ids = [
            f"chunk_{uuid4().hex}"
            for _ in chunks
        ]

        # 4. Generate embeddings
        embeddings = self.embedding_generator.generate_embeddings(
            chunks
        )

        # 5. Generate metadata
        metadatas = [
            {
                "source": "manual_input",
                "chunk_index": index
            }
            for index in range(len(chunks))
        ]

        # 6. Initialize the collection
        self.vector_store.get_or_create_collection(
            self.collection_name
        )

        # 7. Store documents, embeddings and metadata
        self.vector_store.add_documents(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas
        )

        # 8. Return ingestion summary
        return {
            "document_count": len(documents),
            "chunk_count": len(chunks),
            "embedding_count": len(embeddings),
            "collection_name": self.collection_name,
            "ids": ids
        }
