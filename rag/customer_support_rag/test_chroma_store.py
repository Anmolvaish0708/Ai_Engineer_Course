
from app.embeddings.embedding_generator import EmbeddingGenerator
from app.vector_store.chroma_store import ChromaStore

# Sample customer-support documents
documents = [
    "Customers can reset their password through account settings.",
    "Orders can be tracked using the tracking link.",
    "Refunds are processed within five to seven business days."
]

# Generate unique IDs
ids = [
    "faq_001",
    "faq_002",
    "faq_003"
]

# Sample metadata
metadatas = [
    {"source": "account_faq", "category": "account"},
    {"source": "order_faq", "category": "orders"},
    {"source": "refund_faq", "category": "refund"}
]

# Generate embeddings
embedding_generator = EmbeddingGenerator()
embeddings = embedding_generator.generate_embeddings(documents)

# Initialize vector store and collection
store = ChromaStore()
collection = store.get_or_create_collection()

# Store documents
stored_ids = store.add_documents(
    ids=ids,
    documents=documents,
    embeddings=embeddings,
    metadatas=metadatas
)

print("Stored IDs:", stored_ids)
print("Collection count:", collection.count())
