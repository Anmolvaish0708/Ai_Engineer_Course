from app.embeddings.embedding_generator import EmbeddingGenerator
import numpy as np

generator = EmbeddingGenerator()

documents = [
    "Customers can reset their password through account settings.",
    "Orders can be tracked using the tracking link.",
    "Refunds are processed within five to seven business days."
]

embeddings = generator.generate_embeddings(documents)

print("Embedding shape:", embeddings.shape)
print("Number of embeddings:", len(embeddings))
print("Dimensions per embedding:", embeddings.shape[1])
print("Output type:", type(embeddings))
print("All values finite:", np.isfinite(embeddings).all())

query = "How can I get a refund?"

query_embedding = generator.generate_query_embedding(query)

print("\n--- Query Embedding Results ---")
print("Output type:", type(query_embedding))
print("Query embedding shape:", query_embedding.shape)
print("Query dimensions:", len(query_embedding))
print("All values finite:", np.isfinite(query_embedding).all())