# Used once to create embedding collection in Qdrant
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams

COLLECTION = "ollama_vectors"
client = QdrantClient(url="http://localhost:6333")

# Delete if exists
existing_collections = [c.name for c in client.get_collections().collections]
if COLLECTION in existing_collections:
    client.delete_collection(collection_name=COLLECTION)
    print(f"Deleted existing collection '{COLLECTION}'.")

# Recreate with VectorParams
client.recreate_collection(
    collection_name=COLLECTION,
    vectors_config=VectorParams(
        size=1024,       # Qwen3-Embedding-0.6B embedding dimension
        distance="Cosine"
    )
)

print(f"Collection '{COLLECTION}' created successfully.")



# Embedding model (local)
MODEL_NAME = "Qwen/Qwen3-Embedding-0.6B"
embed_model = SentenceTransformer(MODEL_NAME)

# Qdrant setup
COLLECTION = "ollama_vectors"
client = QdrantClient(url="http://localhost:6333")

# Ensure collection exists
existing_collections = [c.name for c in client.get_collections().collections]
if COLLECTION not in existing_collections:
    # 1024 is Qwen3 embedding dim
    client.recreate_collection(collection_name=COLLECTION, vector_size=1024, distance="Cosine")

def get_embedding(text: str):
    """Return embedding vector for a given text"""
    return embed_model.encode(text).tolist()

def add_to_db(id: int, text: str):
    """Add text and embedding to Qdrant"""
    vector = get_embedding(text)
    client.upsert(
        collection_name=COLLECTION,
        points=[{
            "id": id,
            "vector": vector,
            "payload": {
                "page_content": text,
                "metadata": {}
            }
        }]
    )
    print(f"Added '{text}' with id {id}")

# Example usage (run once to populate Qdrant)
if __name__ == "__main__":
    add_to_db(1, "Hello world!")
    add_to_db(2, "Ollama is great for local LLMs.")
    add_to_db(3, "The current president of the USA is Trump as of 2025.")

