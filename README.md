# Final Test - Full Stack AI Chatbot
React + Tailwind | FastAPI + Pydantic | MongoDB + Qdrant | Gemini LLM

This project fulfills ALL acceptance criteria from assignment brief.

## Architecture
Frontend (Node.js/React) -> FastAPI Backend -> MongoDB (users/conversations/messages) + Qdrant (RAG) + Gemini

## Quick Start

### Backend
```
cd backend
python -m venv venv
venv\Scripts\activate (Windows) or source venv/bin/activate
pip install -r requirements.txt
copy .env.example .env  -> add GEMINI_API_KEY and JWT_SECRET_KEY
docker run -d -p 27017:27017 mongo
docker run -d -p 6333:6333 qdrant/qdrant
uvicorn app.main:app --reload --port 8000
```
Seed knowledge base:
```
python scripts/seed_qdrant.py
```
API Docs: http://localhost:8000/docs

### Frontend (Node.js)
```
cd frontend
npm install
copy .env.example .env
npm run dev
```
App: http://localhost:5173

## Features Implemented
- Register / Login / Logout with JWT + bcrypt
- New Chat, persistent history, refresh-safe
- Grouped sidebar: Today, Yesterday, Previous 7 Days, Older (derived from last_message_at)
- Rename / Delete with ownership check
- RAG: embedding query with Gemini text-embedding-004, search Qdrant, generate with gemini-1.5-flash, fallback message if no context
- Ownership enforcement on all conversation/message endpoints
- Loading states, error handling, mobile drawer

## Acceptance Checklist
[x] Register/login/logout
[x] Unauthenticated blocked
[x] Multiple independent chats
[x] Persistence in MongoDB
[x] Grouped history
[x] Rename/delete own only
[x] No IDOR leak
[x] RAG via Qdrant
[x] Pydantic validation + responsive UI
[x] No hard-coded secrets

## Demo Screenshots To Take
1. Register page
2. Login page
3. Empty New Chat
4. Sending message + AI thinking state
5. Grouped history sidebar
6. Rename + Delete
