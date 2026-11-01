import chromadb

# create a persistent chromadb client
client = chromadb.PersistentClient(
    path = "./chroma_db"
)

# create a collection
collection = client.get_or_create_collection(
    name = "customer_support"
)

print("ChromaDB initialized successfully!")
print("Collection:", collection.name)
