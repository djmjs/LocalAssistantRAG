from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams

# Connect to Qdrant container
client = QdrantClient(url="http://localhost:6333")

# Create a collection (vector DB)
collection_name = "ollama_vectors"


client.recreate_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(
        size=1024,       
        # typical embedding size for LLMs, adjust if needed
        distance="Cosine"
    )
)

print(f"Collection '{collection_name}' created successfully.")

# this is the Initialize Qdrant from Python script