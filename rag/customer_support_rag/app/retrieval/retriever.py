
class Retriever:
    """Retrieves relevant document chunks for a user query."""

    def __init__(
        self,
        embedding_generator,
        vector_store,
        collection_name="customer_support"
    ):
        # TODO 1: Store the dependencies.
        self.embedding_generator = embedding_generator
        self.vector_store = vector_store
        self.collection_name = collection_name

        # TODO 2: Initialize the required ChromaDB collection.
        self.vector_store.get_or_create_collection(
                self.collection_name
        )

    def retrieve(self, query, top_k=3, max_distance=None):
        """
        Generate a query embedding and retrieve relevant documents.

        Returns a list of dictionaries containing:
        id, document, metadata and distance.
        """

        # TODO 3: Generate query embedding.
        query_embedding = self.embedding_generator.generate_query_embedding(
            query
        )

        # TODO 4: Search the vector store.
        results = self.vector_store.search(
            query_embedding=query_embedding,
            n_results=top_k,
            max_distance=max_distance
        )

        # TODO 5: Convert nested search results
        # into a list of dictionaries.
        retrieved_results = []

        for i in range(len(results["ids"][0])):
            retrieved_results.append(
                {
                    "id": results["ids"][0][i],
                    "document": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "distance": results["distances"][0][i]
                }
            )

        return retrieved_results
