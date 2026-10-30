
# AI Chatbot - Final Test (FastAPI + Gemini + MongoDB + Qdrant)

## Setup
1. Create venv: python -m venv venv && source venv/bin/activate
2. pip install -r requirements.txt
3. Copy .env.example to .env and add GEMINI_API_KEY
4. Run MongoDB and Qdrant via Docker:
   docker run -d -p 27017:27017 --name mongo mongo
   docker run -d -p 6333:6333 --name qdrant qdrant/qdrant
5. Seed KB: python scripts/seed_qdrant.py
6. Run API: uvicorn app.main:app --reload --port 8000
Docs: http://localhost:8000/docs
