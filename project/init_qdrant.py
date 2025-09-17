from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from qdrant_client.http.exceptions import UnexpectedResponse

qdrant_client = QdrantClient(host="qdrant", port=6333)

def init_qdrant():
    try:
        # Check if collection already exists
        collections = qdrant_client.get_collections()
        existing_collections = [col.name for col in collections.collections]
        
        if "document_chunks" not in existing_collections:
            qdrant_client.create_collection(
                collection_name="document_chunks",
                vectors_config=VectorParams(size=384, distance=Distance.COSINE)
            )
            print("Created new Qdrant collection")
        else:
            print("Qdrant collection already exists, skipping creation")
    except Exception as e:
        print(f"Qdrant init error: {e}")