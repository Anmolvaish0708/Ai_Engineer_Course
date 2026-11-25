from dotenv import load_dotenv
import os
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


if __name__ == "__main__":

    documents = load_documents()

    print("\nTotal document records:", len(documents))

    for index, document in enumerate(documents, start=1):

        print(f"\nRecord {index}")
        print("Metadata:", document["metadata"])
        print("Text:", document["text"][:200])