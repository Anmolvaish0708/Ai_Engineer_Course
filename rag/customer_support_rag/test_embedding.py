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