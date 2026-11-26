from dotenv import load_dotenv
import os
import json
from pathlib import Path

import faiss
import numpy as np
from groq import Groq
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from docx import Document


# ============================================================
# 1. SETTINGS
# ============================================================

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
VECTOR_STORE_DIR = BASE_DIR / "vector_store"
INDEX_PATH = VECTOR_STORE_DIR / "faiss.index"
CHUNKS_PATH = VECTOR_STORE_DIR / "chunks.json"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
TOP_K = 3

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
EMBEDDING_BATCH_SIZE = 100

# ============================================================
# 2. DOCUMENT LOADING
# ============================================================

def load_documents():
    """
    Load supported document (PDF,TXT and DOCX) files from the data directory.
    
    Returns:
        list: A list of dicionries containg the document content and metadata."""

    if not DATA_DIR.exists():
        raise FileNotFoundError(f"Data directory '{DATA_DIR}' does not exist.")
    
    documents = []

    for file_path in DATA_DIR.rglob("*"):

        if not file_path.is_file():
            print(f"skipping '{file_path}' as it is not a file.")
            continue

        if file_path.suffix.lower() not in [".pdf", ".txt", ".docx"]:
            print(f"skipping '{file_path}' as it is not a supported file type.")
            continue

        extension = file_path.suffix.lower()
        
        try:
            if extension == ".pdf":
                reader = PdfReader(str(file_path))

                # Process PDF content
                for page_number, page in enumerate(reader.pages, start=1):
                    text = page.extract_text() or ""

                    if text.strip():
                        documents.append({
                            "text": text.strip(),
                            "metadata": {
                                "source": file_path.name,
                                "page": page_number,
                                "file_type": "pdf"
                            }
                        })

            elif extension == ".txt":
                text = file_path.read_text(encoding="utf-8", errors="ignore") or ""

                if text.strip():
                    documents.append({
                        "text": text.strip(),
                        "metadata": {
                            "source": file_path.name,
                            "file_type": "txt"
                        }
                    })
            elif extension == ".docx":
                doc = Document(str(file_path))

                text = "\n".join(paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip())

                if text.strip():
                    documents.append({
                        "text": text.strip(),
                        "metadata": {
                            "source": file_path.name,
                            "file_type": "docx"
                        }
                    })
            print(f"Successfully loaded: {file_path.name}")  

        except Exception as e:
            print(f"Error loading '{file_path}': {e}")
            continue

    if not documents:
        raise ValueError(
                    "No readable text found in the data folder. Add a text-based "
                    ".txt, .pdf, or .docx file. Scanned PDFs may need OCR first."
            )

    return documents


# ============================================================
# 3. TEXT CHUNKING
# ============================================================

def chunk_documents(documents):
    """
      Chunk the documents into smaller pieces of text with overlap.
    """
    if not documents:
        raise ValueError("No documents provided for chunking.")

    chunks = []
    step_size = CHUNK_SIZE - CHUNK_OVERLAP

    for document in documents:
        text = document["text"]
        metadata = document["metadata"]

        start = 0

        while start < len(text):
            end = min(start + CHUNK_SIZE, len(text))
            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append({
                    "text": chunk_text,
                    "metadata": metadata
                })
            start += step_size  

    if not chunks:
        raise ValueError("No chunks could be generated.")   

    print(f"Created {len(chunks)} chunks.")
    return chunks       



# ============================================================
# 3. GENERATE EMBEDDINGS
# ============================================================

def generate_embeddings(chunks):
    """
    Generate embeddings for the text chunks using the specified embedding model.

    """
    if not chunks:
        raise ValueError("No chunks provided for embedding generation.")

    if EMBEDDING_BATCH_SIZE <= 0:
         raise ValueError("Batch size must be greater than zero.")

    texts = [chunk["text"] for chunk in chunks]

    for text in texts:
        if not text.strip():
            raise ValueError("chunk cannot be empty.")

    try:
        print("\nLoading embedding model...")

        model = SentenceTransformer(EMBEDDING_MODEL)   

        embeddings = model.encode(
            texts,
            batch_size=EMBEDDING_BATCH_SIZE,
            convert_to_numpy=True,
            show_progress_bar=False
        ) 

        
        embeddings = np.asarray(embeddings, dtype=np.float32)


    except Exception as err:
        raise RuntimeError(f"Embedding generation failed. {err}") from err

    if embeddings.ndim != 2:
            raise ValueError("Embeddings must be a 2-dimensional array.")

    if embeddings.shape[0] != len(chunks):
            raise ValueError("Number of embeddings does not match number of chunks.")

    if not np.isfinite(embeddings).all():
            raise ValueError("Embeddings contain invalid numerical values.")

    print(f"Successfully generated {len(embeddings)} embeddings.")
    print(f"Embedding dimensions: {embeddings.shape[1]}")

    return embeddings



# ============================================================
# 3. BUILD FAISS INDEX
# ============================================================


def build_faiss_index(embeddings: np.ndarray):

    if embeddings.size == 0:
        raise ValueError("No embeddings provided.")

    if embeddings.ndim != 2:
        raise ValueError("Embeddings must be a 2-dimensional array.")

    if not np.isfinite(embeddings).all():
        raise ValueError("Embeddings contain invalid numerical values.")

    # FAISS expects float32 vectors.
    embeddings = np.ascontiguousarray(
        embeddings,
        dtype=np.float32
    )

    # Each row represents one embedding.
    # Normalize vectors so inner product becomes cosine similarity.
    normalized_embeddings = embeddings.copy()
    faiss.normalize_L2(normalized_embeddings)

    # Get the embedding dimension.
    embedding_dimension = normalized_embeddings.shape[1]

    # Create an exact inner-product index.
    index = faiss.IndexFlatIP(embedding_dimension)

    # Add document vectors to the index.
    index.add(normalized_embeddings)

    print("\nFAISS index created successfully.")
    print(f"Total vectors indexed: {index.ntotal}")
    print(f"Vector dimensions: {index.d}")

    return index


def save_vector_store(index, chunks):

    VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)

    faiss.write_index(index, str(INDEX_PATH))

    with open(CHUNKS_PATH, "w", encoding="utf-8") as file:
        json.dump(chunks, file, ensure_ascii=False, indent=4)

    print("Vector store saved successfully.")


def load_vector_store():

    if not INDEX_PATH.exists() or not CHUNKS_PATH.exists():
        raise FileNotFoundError("Saved vector store not found.")

    index = faiss.read_index(str(INDEX_PATH))

    with open(CHUNKS_PATH, "r", encoding="utf-8") as file:
        chunks = json.load(file)

    if index.ntotal != len(chunks):
        raise ValueError("FAISS index and chunks data are inconsistent.")

    print("Vector store loaded successfully.")

    return index, chunks



def get_or_create_vector_store():

    if INDEX_PATH.exists() and CHUNKS_PATH.exists():

        print("Existing vector store found.")

        index, chunks = load_vector_store()

    else:

        print("Vector store not found. Creating a new one...")

        documents = load_documents()

        chunks = chunk_documents(documents)

        embeddings = generate_embeddings(chunks)

        index = build_faiss_index(embeddings)

        save_vector_store(index, chunks)

    return index, chunks


if __name__ == "__main__":

    index, chunks = get_or_create_vector_store()

    print("\nTotal vectors:", index.ntotal)
    print("Total chunks:", len(chunks))
