from qdrant_client import QdrantClient  # type: ignore
from qdrant_client.models import Distance, VectorParams  # type: ignore
from app.core.config import settings
from typing import Any

qdrant_client: Any = None

def connect_to_qdrant():
    global qdrant_client
    qdrant_client = QdrantClient(
        url=settings.QDRANT_URL,
        api_key=settings.QDRANT_API_KEY or None,
    )
    collections = [c.name for c in qdrant_client.get_collections().collections]
    if settings.QDRANT_COLLECTION not in collections:
        qdrant_client.create_collection(
            collection_name=settings.QDRANT_COLLECTION,
            vectors_config=VectorParams(size=3072, distance=Distance.COSINE),
        )
        print(f"Created collection: {settings.QDRANT_COLLECTION} (3072 dim)")
    else:
        print(f"Qdrant connected, collection: {settings.QDRANT_COLLECTION}")

def get_qdrant():
    return qdrant_client