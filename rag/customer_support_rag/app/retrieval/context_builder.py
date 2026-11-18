
import math

class ContextBuilder:
    """Builds LLM-ready context from retrieved documents."""

    def build_context(self, retrieved_documents):
        """Format retrieved documents and preserve source references."""

        if not isinstance(retrieved_documents, list):
            raise TypeError("retrieved_documents must be a list.")

        if not retrieved_documents:
            return {"context": "", "sources": []}

        formatted_documents = []
        sources = []

        required_keys = {"id", "document", "metadata", "distance"}

        for index, doc in enumerate(retrieved_documents, start=1):

            if not isinstance(doc, dict):
                raise TypeError(
                    "Each retrieved document must be a dictionary."
                )

            if not required_keys.issubset(doc):
                raise ValueError(
                    "Each retrieved document must contain "
                    "'id', 'document', 'metadata', and 'distance'."
                )

            doc_id = doc["id"]
            document_text = doc["document"]
            metadata = doc["metadata"]
            distance = doc["distance"]

            if not isinstance(doc_id, str) or not doc_id.strip():
                raise ValueError(
                    "Document ID must be a non-empty string."
                )

            if (
                not isinstance(document_text, str)
                or not document_text.strip()
            ):
                raise ValueError(
                    "Document text must be a non-empty string."
                )

            if not isinstance(metadata, dict):
                raise TypeError("Metadata must be a dictionary.")

            if (
                isinstance(distance, bool)
                or not isinstance(distance, (int, float))
                or not math.isfinite(distance)
                or distance < 0
            ):
                raise ValueError(
                    "Distance must be a finite, non-negative number."
                )

            formatted_doc = (
                f"[Document {index} | ID: {doc_id}]\n"
                f"{document_text.strip()}"
            )

            formatted_documents.append(formatted_doc)

            sources.append({
                "id": doc_id.strip(),
                "metadata": metadata,
                "distance": distance
            })

        context = "\n\n".join(formatted_documents)

        return {
            "context": context,
            "sources": sources
        }
