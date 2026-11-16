from sentence_transformers import SentenceTransformer
from app.exceptions import EmbeddingError

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

            return embeddings
        
        except Exception as err:
            raise EmbeddingError("Failed to generate document embeddings.")  from err


