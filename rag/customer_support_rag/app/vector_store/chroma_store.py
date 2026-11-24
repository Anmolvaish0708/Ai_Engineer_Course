import chromadb
from pathlib import Path
import numpy as np

from app.config import CHROMA_DB_PATH
from app.config import COLLECTION_NAME
from app.exceptions import VectorStoreError

class ChromaStore:
    """Manages persistent vector storage using ChromaDB."""

    def __init__(self, db_path: Path = CHROMA_DB_PATH):
        """Initialize a persistent ChromaDB client."""

        if not isinstance(db_path, (str,Path)):
            raise TypeError("Database path must be a string or Path.")

        self.db_path = Path(db_path).expanduser().resolve()

        try:
            self.client = chromadb.PersistentClient(
                path = str(self.db_path)
            )
        except Exception as err:
            raise VectorStoreError(
                f"Failed to initialize ChromaDB at '{self.db_path}'."
            )  from err

    def get_or_create_collection(self, collection_name: str = COLLECTION_NAME):
        """Create a collection or retrieve it if it already exists."""

        if not isinstance(collection_name,str) or not collection_name.strip():
            raise ValueError("Collection name must be a non-empty string.")  

        self.collection_name = collection_name.strip()

        try:
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"},
                embedding_function=None
            )

            return self.collection
        
        except Exception as err:
            raise VectorStoreError(
            f"Failed to create or retrieve collection '{collection_name}'."
        ) from err  

    
    def add_documents(self, ids, documents, embeddings, metadatas=None):
        """Store document chunks, embeddings, and metadata in ChromaDB."""

        # 1. Check whether a collection has been initialized
        if not hasattr(self, "collection"):
            raise VectorStoreError(
                "Collection is not initialized. "
                "Call get_or_create_collection() first."
            )

        # 2. Validate IDs
        if not isinstance(ids, list) or not ids:
            raise ValueError("IDs must be a non-empty list.")

        if any(not isinstance(item, str) or not item.strip() for item in ids):
            raise ValueError("Every ID must be a non-empty string.")

        ids = [item.strip() for item in ids]

        if len(ids) != len(set(ids)):
            raise ValueError("Document IDs must be unique.")

        if len(ids) != len(documents):
            raise ValueError(
                "Number of IDs must match number of documents."
            )    

        # 3. Validate documents
        if not isinstance(documents, list) or not documents:
            raise ValueError("Documents must be a non-empty list.")

        for index, document in enumerate(documents):
            if not isinstance(document, str):
                raise TypeError(
                    f"Document at index {index} must be a string."
                )

            if not document.strip():
                raise ValueError(
                    f"Document at index {index} cannot be empty."
                )

        # 4. Validate and prepare embeddings
        try:
            embeddings = np.asarray(embeddings, dtype=np.float32)
        except (TypeError, ValueError) as exc:
            raise ValueError("Embeddings must contain numerical values.") from exc

        if embeddings.ndim != 2:
            raise ValueError("Embeddings must be a 2D array.")

        if embeddings.shape[0] != len(documents):
            raise ValueError(
                "Number of embeddings must match number of documents."
            )

        if embeddings.shape[1] == 0:
            raise ValueError("Embedding vectors cannot be empty.")

        if not np.isfinite(embeddings).all():
            raise ValueError("Embeddings contain invalid numerical values.")

        # 5. Validate metadata
        if metadatas is None:
            metadatas = [{} for _ in documents]

        if not isinstance(metadatas, list):
            raise TypeError("Metadata must be provided as a list.")

        if len(metadatas) != len(documents):
            raise ValueError(
                "Number of metadata records must match number of documents."
            )

        for index, metadata in enumerate(metadatas):
            if not isinstance(metadata, dict):
                raise TypeError(
                    f"Metadata at index {index} must be a dictionary."
                )

        # 6. Store records in ChromaDB
        try:
            self.collection.add(
                ids=ids,
                documents=documents,
                embeddings=embeddings.tolist(),
                metadatas=metadatas
            )

            return ids

        except Exception as exc:
            raise VectorStoreError(
                "Failed to add documents to ChromaDB."
            ) from exc
        
    def get_documents(self, ids):
        """"Retrieve documents and metadata from chromadb based on their unique IDs."""    

        if not hasattr(self, "collection"):
            raise VectorStoreError(
                "Collection is not initialized. "
                "Call get_or_create_collection() first."
        ) 
        
        if not isinstance(ids, list) or not ids:
            raise ValueError("Ids must be a non-empty list")

        if any(not isinstance(item,str) or not item.strip() for item in ids):
            raise ValueError("Each item must be a non empty string.")

        ids = [item.strip() for item in ids]

        if len(ids) != len(set(ids)):
            raise ValueError("Document IDs must be unique.")
        
        try:
            results = self.collection.get(
                ids = ids,
                include= ["documents", "metadatas"]
            )

            return results
        
        except Exception as err:
            raise VectorStoreError(
                "failed to fetch the results from chromadb."
            )  from err  


    def search(self, query_embedding, n_results=3, max_distance=None):
        """Retrieve the most relevant documents using vector similarity."""

        if not hasattr(self, "collection"):
            raise VectorStoreError(
                "Collection is not initialized. "
                "Call get_or_create_collection() first."
            )
        
        try:
            query_embedding = np.asarray(query_embedding, dtype = np.float32)
        except (TypeError,ValueError) as err:
            raise ValueError("query embedding must conatain numerical values.") from err

        if query_embedding.ndim != 1:
            raise ValueError("query embedding must be 1D array.")

        if query_embedding.size == 0:
            raise ValueError("Query embedding cannot be empty.")

        if not np.isfinite(query_embedding).all():
            raise ValueError("Query Embeddings contain invalid numerical values.")

        if isinstance(n_results, bool) or not isinstance(n_results, int):
            raise TypeError("n_results must be an integer.")
        
        if n_results <= 0:
            raise ValueError("n_results must be a positive integer.")

        if max_distance is not None:

            if isinstance(max_distance,bool) or not isinstance(max_distance, (int,float)):
                raise TypeError("max_distance must be int or float.")
            
            if not np.isfinite(max_distance):
                raise ValueError("max_distance must be finite.")
            
            if max_distance < 0:
                raise ValueError("max_distance must be a non-negative number.")

            max_distance = float(max_distance)
            
        try:
            results = self.collection.query(
                query_embeddings = [query_embedding.tolist()],
                n_results = n_results,
                include = ["documents", "metadatas", "distances"]
            )   

            if max_distance is None:
                return results

            filtered_indices = [i for i, distance in enumerate(results["distances"][0]) if distance <= max_distance]

            filtered_results = {
                "ids": [[results["ids"][0][i]for i in filtered_indices]],
                "documents": [[results["documents"][0][i] for i in filtered_indices]],
                "metadatas": [[results["metadatas"][0][i] for i in filtered_indices]],
                "distances": [[results["distances"][0][i] for i in filtered_indices]]
            }

            return filtered_results
        
        except Exception as err:
            raise VectorStoreError(
                "failed to retrieve to relevant reuslts."
            ) from err 



      