import chromadb
from sentence_transformers import SentenceTransformer

# create a persistent chromadb client
client = chromadb.PersistentClient(
    path = "./chroma_db"
)

# create a collection
collection = client.get_or_create_collection(
    name = "customer_support"
)

# 3. Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# 4. Prepare documents
documents = [
    "Refund Policy: Customers can request a full refund within 30 days of purchasing a product.",
    "Customer Support: Our customer support team is available 24 hours a day, 7 days a week to help customers.",
    "Programming Guide: Python is a popular programming language used for artificial intelligence and data science.",
    "Exchange Policy: Customers can exchange purchased products within 15 days of delivery.",
    "Order Tracking: Customers can track their package delivery status using the tracking ID provided after purchase."
]

# 5. Create unique IDs
ids = ["doc_1", "doc_2", "doc_3", "doc_4", "doc_5"]

# 6. Add metadata
metadatas = [
    {"category": "refund"},
    {"category": "support"},
    {"category": "programming"},
    {"category": "exchange"},
    {"category": "tracking"}
]

# 7. Generate embeddings
embeddings = model.encode(documents).tolist()

# 8. Insert data into ChromaDB
collection.add(
    ids=ids,
    documents=documents,
    embeddings=embeddings,
    metadatas=metadatas
)

print("Documents successfully added!")

# 9. Verify stored records
print("Total records:", collection.count())

stored_data = collection.get(
    include=["documents", "metadatas", "embeddings"]
)

print(stored_data)
print("Number of embeddings:", len(stored_data["embeddings"]))
print("Embedding dimensions:", len(stored_data["embeddings"][0]))