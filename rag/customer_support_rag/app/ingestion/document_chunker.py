
class DocumentChunker:
    """Splits documents into smaller chunks for RAG ingestion."""

    def __init__(self, chunk_size, chunk_overlap):
        # Validate and store configuration
        if chunk_size <=0:
            raise ValueError("chunk size should be greate than zero")
        
        if chunk_overlap < 0:
            raise ValueError("chunk overlap should be greater than equal to zero")

        if chunk_overlap >= chunk_size:
            raise ValueError("chunk overlap cannot be greater than or equal to chunk size.")
        
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_documents(self, documents):

        # Validate input
        if not isinstance(documents,list):
            raise TypeError("documents must be a list")
        
        # Chunk the documents
        chunks = []
        step_size = self.chunk_size - self.chunk_overlap

        for doc in documents:
            start = 0
            while start < len(doc):
                chunk = doc[start:start + self.chunk_size]
                chunks.append(chunk)
                start += step_size
            

        # Return the chunks
        return chunks



chunker = DocumentChunker(10,2)
chunks =  chunker.chunk_documents(
    ["Refund Policy: Customers can request a full refund within 30 days of purchasing a product.",
    
        "Customer Support: Our customer support team is available 24 hours a day, 7 days a week to help customers.",
    
        "Programming Guide: Python is a popular programming language used for artificial intelligence and data science.",
    
        "Exchange Policy: Customers can exchange purchased products within 15 days of delivery."]
)

print(chunks)