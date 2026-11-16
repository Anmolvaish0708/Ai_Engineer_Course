from sentence_transformers import SentenceTransformer
from app.exceptions import EmbeddingError
import numpy as np

class EmbeddingGenerator:

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """Initialize the embedding generator with a specified model."""

        if not isinstance(model_name, str) or not model_name.strip():
            raise ValueError("model name must be a non-empty string.")

        self.model_name = model_name

        try:
            self.model = SentenceTransformer(self.model_name)
            self.embedding_dimension = (
                self.model.get_embedding_dimension()
            )
        except Exception as e:
            raise EmbeddingError(f"Failed to load embedding model '{self.model_name}': {e}") from e

    def generate_embeddings(self, documents): 
        """Generate embeddings for multiple documents."""

        if not isinstance(documents, list):
            raise TypeError("Documents must be provided as a list.")     

        if not documents:
            raise ValueError("Documents list cannot be empty.")

        for index, document in enumerate(documents):

            if not isinstance(document, str):
                raise TypeError(f"Document at index {index} must be a string.")

            if not document.strip():
                raise ValueError(f"Document at index {index} cannot be empty.")

        try:

            embeddings = self.model.encode(
                documents,
                convert_to_numpy=True,
                show_progress_bar=False
            )  

        
        except Exception as err:
            raise EmbeddingError("Failed to generate document embeddings.")  from err

        # 3. Validate embedding output

        if not isinstance(embeddings, np.ndarray):
            raise EmbeddingError(
                "Embedding model did not return a NumPy array."
            )

        if embeddings.ndim != 2:
            raise EmbeddingError(
                f"Expected a 2D embedding array, got {embeddings.ndim}D."
            )

        if embeddings.shape[0] != len(documents):
            raise EmbeddingError(
                "Number of generated embeddings does not match "
                "the number of input documents."
            )

        if embeddings.shape[1] != self.embedding_dimension:
            raise EmbeddingError(
                f"Expected embedding dimension {self.embedding_dimension}, "
                f"got {embeddings.shape[1]}."
            )

        if not np.isfinite(embeddings).all():
            raise EmbeddingError(
                "Embeddings contain invalid numerical values."
            )

        return embeddings

    
    def generate_query_embedding(self, query):
        """Generate an embedding for a single user query."""

        if not isinstance(query, str):
            raise TypeError("Query must be a string.")

        if not query.strip():
            raise ValueError("Query cannot be empty.")

        embeddings = self.generate_embeddings([query])

        return embeddings[0]
        



