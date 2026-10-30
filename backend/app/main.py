
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.mongo import connect_to_mongo, close_mongo_connection
from app.db.qdrant_client import connect_to_qdrant
from app.routers import auth, conversations, chat

app = FastAPI(title="AI Chatbot API - Final Test", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()
    connect_to_qdrant()

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()

app.include_router(auth.router)
app.include_router(conversations.router)
app.include_router(chat.router)

@app.get("/")
async def root():
    return {"message": "AI Chatbot API Running", "docs": "/docs"}

@app.get("/health")
async def health():
    return {"status": "ok"}
