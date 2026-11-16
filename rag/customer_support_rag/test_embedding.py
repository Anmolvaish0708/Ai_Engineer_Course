from app.embeddings.embedding_generator import EmbeddingGenerator

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
print("First embedding:", embeddings[0])
