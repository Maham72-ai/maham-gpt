from app.db.qdrant_client import get_qdrant  # type: ignore
from app.core.config import settings
from app.services.llm_service import create_embedding
from qdrant_client.models import PointStruct  # type: ignore
import uuid

def search_knowledge_base(query: str, top_k: int = 4):
    try:
        client = get_qdrant()
        query_vector = create_embedding(query)
        
        results = client.query_points(
            collection_name=settings.QDRANT_COLLECTION,
            query=query_vector,
            limit=top_k,
            with_payload=True
        ).points
        
        relevant = [hit.payload.get('text','') for hit in results if hit.score > 0.65]
        return relevant
    except Exception as e:
        print(f"Qdrant search failed (fallback): {e}")
        return []

def index_sample_knowledge(texts: list, source: str = "sample"):
    client = get_qdrant()
    points = []
    for chunk in texts:
        vec = create_embedding(chunk)
        points.append(PointStruct(
            id=str(uuid.uuid4()),
            vector=vec,
            payload={"text": chunk, "source": source}
        ))
    client.upsert(collection_name=settings.QDRANT_COLLECTION, points=points)
    return len(points)