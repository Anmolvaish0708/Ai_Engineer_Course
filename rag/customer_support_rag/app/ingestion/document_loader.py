
class DocumentLoader:
    """Loads and validates documents for a RAG ingestion pipeline."""

    def load_documents(self, documents):

        results = []

        if not isinstance(documents,list):
            raise TypeError("Documents should be a list.")
        
        if not documents:
            raise ValueError("Documents can not be empty.")

        for doc in documents:

            if not isinstance(doc,str):
                raise TypeError("each element must be a string.")
        
            cleaned_document = doc.strip()

            if cleaned_document:
                results.append(cleaned_document)

        if not results:
            raise ValueError(
                "No valid documents were found after processing."
            )

        return results       

loader = DocumentLoader()    
documents = loader.load_documents(["hello", "   "])

print(documents)