# back_end/services/document_service.py
import uuid
from typing import List
from .qdrant_service import qdrant_client
from .embedding_service import embed_text
from documents.models import DocumentChunk, Document

# -------------------------
# 1️⃣ Save a single chunk to Qdrant
# -------------------------
def save_chunk_to_qdrant(chunk: DocumentChunk):
    """
    takes chunk of text, converts it to embeddings using your embedding service, then stores both the vector and metadata in Qdrant vector database
    """
    embedding = embed_text(chunk.text)

    qdrant_client.upsert(
        collection_name="document_chunks",
        points=[
            {
                "id": str(chunk.id),  # use chunk UUID
                "vector": embedding,
                "payload": {
                    "document_id": str(chunk.document.id),
                    "chunk_index": chunk.chunk_index,
                    "text": chunk.text,
                }
            }
        ]
    )

    # store Qdrant ID back in Django
    chunk.qdrant_id = str(chunk.id)
    chunk.save()


# -------------------------
# 2️⃣ Split document text into chunks
# -------------------------
def split_text_into_chunks(text: str, chunk_size: int = 500) -> List[str]:
    """
    Splits text into chunks of approximately `chunk_size` (500-word) words.
    """
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk_text = " ".join(words[i:i+chunk_size])
        chunks.append(chunk_text)
    return chunks


# -------------------------
# 3️⃣ Process a document (create chunks, save to DB + Qdrant)
# -------------------------
def process_document(document: Document, text: str, chunk_size: int = 500):
    """
    Given a Document instance and full text, split it into chunks,
    create DocumentChunk objects, and save embeddings to Qdrant.
    """
    chunks_text = split_text_into_chunks(text, chunk_size)
    
    for index, chunk_text in enumerate(chunks_text):
        chunk = DocumentChunk.objects.create(
            document=document,
            text=chunk_text,
            chunk_index=index
        )
        save_chunk_to_qdrant(chunk)


# -------------------------
# 4️⃣ Search for similar chunks
# -------------------------
def search_similar_chunks(query: str, top_k: int = 5):
    """
    Embeds the query, searches Qdrant, and returns top-k relevant chunks.
    """
    query_vector = embed_text(query)
    results = qdrant_client.search(
        collection_name="document_chunks",
        query_vector=query_vector,
        limit=top_k
    )

    # Return simplified info
    simplified_results = [
        {
            "chunk_id": point.id,
            "document_id": point.payload.get("document_id"),
            "chunk_index": point.payload.get("chunk_index"),
            "text": point.payload.get("text")
        }
        for point in results
    ]
    return simplified_results
