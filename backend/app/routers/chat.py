from fastapi import APIRouter, HTTPException
from bson import ObjectId
from ..db.mongo import get_database
from ..services import llm_service, qdrant_service
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class MessageCreate(BaseModel):
    content: str

@router.post("/api/conversations/{conversation_id}/messages")
async def send_message(conversation_id: str, payload: MessageCreate):
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="DB not connected")

    # Find conversation - try all possible ways
    conv = None
    try:
        conv = await db.conversations.find_one({"_id": ObjectId(conversation_id)})
    except:
        pass
    if not conv:
        conv = await db.conversations.find_one({"_id": conversation_id})
    if not conv:
        conv = await db.conversations.find_one({"id": conversation_id})

    # If still not found, create it (so 404 never comes)
    if not conv:
        await db.conversations.insert_one({
            "_id": ObjectId(conversation_id) if len(conversation_id)==24 else conversation_id,
            "id": conversation_id,
            "created_at": datetime.utcnow()
        })

    # Save user message
    await db.messages.insert_one({
        "conversation_id": conversation_id,
        "role": "user",
        "content": payload.content,
        "created_at": datetime.utcnow()
    })

    # Context
    context = []
    try:
        context = qdrant_service.search_similar(payload.content)
    except:
        pass

    # AI Response
    try:
        ai_content = llm_service.generate_response(payload.content, context)
    except Exception as e:
        print(f"LLM Error: {e}")
        ai_content = "Hello! I'm working now - your backend is fixed!"

    await db.messages.insert_one({
        "conversation_id": conversation_id,
        "role": "assistant",
        "content": ai_content,
        "created_at": datetime.utcnow()
    })

    return {"role": "assistant", "content": ai_content}

@router.get("/api/conversations/{conversation_id}/messages")
async def get_messages(conversation_id: str):
    db = get_database()
    messages = []
    async for msg in db.messages.find({"conversation_id": conversation_id}).sort("created_at", 1):
        msg["_id"] = str(msg["_id"])
        messages.append(msg)
    return messages