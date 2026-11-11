class RAGApplicationError(Exception):
    """
    Base exception for all application-specific RAG errors.
    """


class DocumentProcessingError(RAGApplicationError):
    """
    Raised when document loading or processing fails.
    """


class EmbeddingError(RAGApplicationError):
    """
    Raised when embedding generation fails.
    """


class RetrievalError(RAGApplicationError):
    """
    Raised when document retrieval fails.
    """