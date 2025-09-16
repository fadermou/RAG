##all-MiniLM-L6-v2

from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def embed_text(text: str):
    return model.encode(text).tolist()  # return as list (Qdrant expects list[float])
