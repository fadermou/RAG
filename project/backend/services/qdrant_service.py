from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

# Connect to Qdrant (assuming you run it in docker-compose on service name "qdrant")
qdrant_client = QdrantClient(host="qdrant", port=6333)

# Create collection if not exists
def init_qdrant():
    qdrant_client.recreate_collection(
        collection_name="document_chunks",
        vectors_config=VectorParams(size=384, distance=Distance.COSINE)  # 384 for MiniLM embeddings
    )
