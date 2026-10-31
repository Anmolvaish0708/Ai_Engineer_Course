from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# 1. Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# 2. Prepare our knowledge base
documents = [
    "Refund Policy: Customers can request a full refund within 30 days of purchasing a product.",

    "Customer Support: Our customer support team is available 24 hours a day, 7 days a week to help customers.",

    "Programming Guide: Python is a popular programming language used for artificial intelligence and data science.",

    "Exchange Policy: Customers can exchange purchased products within 15 days of delivery.",

    "Order Tracking: Customers can track their package delivery status using the tracking ID provided after purchase."
]

# 3. Generate embeddings for all documents
document_embeddings = model.encode(documents)


print("Number of documents:", len(documents))
print("Document embeddings shape:", document_embeddings.shape)

# 4. Take a query from the user
query = "I want to replace an item I purchased."

# 5. Generate embedding for the query
query_embedding = model.encode(query)

print("Query embedding shape:", query_embedding.shape)


# 6. Calculate similarity between query and documents
similarity_scores = cosine_similarity(
    [query_embedding],                   
    document_embeddings
)

print("Similarity scores:", similarity_scores)

# # 7. Find the documents with the highest similarity
# best_match_index = similarity_scores.argmax()

# best_document = documents[best_match_index]
# best_score = similarity_scores[0][best_match_index]

# print("\nBest matching document:")
# print(best_document)

# print("Similarity score:", best_score)

# Get similarity scores
scores = similarity_scores[0]

# Get indices of top 3 documents
top_k = 3

top_indices = np.argsort(scores)[::-1][:top_k]

# Similarity threshold
threshold = 0.30

print("\nRelevant documents:\n")

found_match = False

for index in top_indices:
    score = scores[index]

    if score >= threshold:
        found_match = True
        print(f"Document: {documents[index]}")
        print(f"Similarity: {scores[index]:.4f}")
        print("-" * 50)

if not found_match:
    print("No sufficiently relevant document found.")
    
# Display results
# print("\nTop 3 matching documents:\n")

# for rank, index in enumerate(top_indices, start=1):
#     print(f"Rank: {rank}")
#     print(f"Document: {documents[index]}")
#     print(f"Similarity: {scores[index]:.4f}")
#     print("-" * 50)