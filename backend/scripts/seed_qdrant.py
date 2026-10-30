
# Run this once to index sample KB into Qdrant
from app.db.qdrant_client import connect_to_qdrant
from app.services.qdrant_service import index_sample_knowledge

connect_to_qdrant()
with open("knowledge_base/sample_kb.txt", "r") as f:
    content = f.read()
    chunks = [c.strip() for c in content.split("\n") if len(c.strip()) > 30]
    count = index_sample_knowledge(chunks, source="sample_kb.txt")
    print(f"Indexed {count} chunks")
