from pathlib import Path

class Settings:
    BASE_DIR = Path(__file__).resolve().parent.parent

    DATA_DIR = BASE_DIR/"data"

    CHROMA_DB_PATH = BASE_DIR/"chrom_db"
    
    COLLECTION_NAME = "customer_support"

    EMBEDDING_MODEL = "all-MiniLM-L6-v2"

    TOP_K = 3

 