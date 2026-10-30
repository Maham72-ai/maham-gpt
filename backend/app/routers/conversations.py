
from fastapi import APIRouter, Depends, HTTPException
from app.routers.auth import get_current_user
from app.schemas.conversation import CreateConversationRequest, RenameConversationRequest, ConversationResponse, ConversationDetailResponse, MessageResponse
from app.db.mongo import get_db
from bson import ObjectId
from datetime import datetime, timezone

router = APIRouter(prefix="/api/conversations", tags=["Conversations"])

def to_resp(doc):
    return ConversationResponse(
        id=str(doc["_id"]),
        user_id=str(doc["user_id"]),
        title=doc["title"],
        created_at=doc["created_at"],
        updated_at=doc["updated_at"],
        last_message_at=doc["last_message_at"],
        message_count=doc.get("message_count",0)
    )

@router.post("", response_model=ConversationResponse)
async def create_conversation(data: CreateConversationRequest, current_user=Depends(get_current_user)):
    db = get_db()
    now = datetime.now(timezone.utc)
    doc = {
        "user_id": current_user["_id"],
        "title": data.title,
        "created_at": now,
        "updated_at": now,
        "last_message_at": now,
        "message_count": 0
    }
    res = await db["conversations"].insert_one(doc)
    doc["_id"] = res.inserted_id
    return to_resp(doc)

@router.get("", response_model=list[ConversationResponse])
async def list_conversations(current_user=Depends(get_current_user)):
    db = get_db()
    cursor = db["conversations"].find({"user_id": current_user["_id"]}).sort("last_message_at", -1).limit(100)
    convs = await cursor.to_list(length=100)
    return [to_resp(c) for c in convs]

@router.get("/{conversation_id}", response_model=ConversationDetailResponse)
async def get_conversation(conversation_id: str, current_user=Depends(get_current_user)):
    db = get_db()
    try:
        oid = ObjectId(conversation_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid conversation ID")
    
    conv = await db["conversations"].find_one({"_id": oid, "user_id": current_user["_id"]})
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found or access denied")
    
    msgs_cursor = db["messages"].find({"conversation_id": oid}).sort("created_at", 1).limit(200)
    msgs = await msgs_cursor.to_list(length=200)
    msg_resps = [MessageResponse(id=str(m["_id"]), conversation_id=str(m["conversation_id"]), role=m["role"], content=m["content"], created_at=m["created_at"]) for m in msgs]
    
    detail = to_resp(conv).model_dump()
    detail["messages"] = msg_resps
    return ConversationDetailResponse(**detail)

@router.patch("/{conversation_id}", response_model=ConversationResponse)
async def rename_conversation(conversation_id: str, data: RenameConversationRequest, current_user=Depends(get_current_user)):
    db = get_db()
    try: oid = ObjectId(conversation_id)
    except: raise HTTPException(status_code=400, detail="Invalid ID")
    
    res = await db["conversations"].find_one_and_update(
        {"_id": oid, "user_id": current_user["_id"]},
        {"$set": {"title": data.title, "updated_at": datetime.now(timezone.utc)}},
        return_document=True
    )
    if not res:
        raise HTTPException(status_code=404, detail="Not found")
    return to_resp(res)

@router.delete("/{conversation_id}")
async def delete_conversation(conversation_id: str, current_user=Depends(get_current_user)):
    db = get_db()
    try: oid = ObjectId(conversation_id)
    except: raise HTTPException(status_code=400, detail="Invalid ID")
    
    conv = await db["conversations"].find_one({"_id": oid, "user_id": current_user["_id"]})
    if not conv:
        raise HTTPException(status_code=404, detail="Not found")
    
    await db["conversations"].delete_one({"_id": oid})
    await db["messages"].delete_many({"conversation_id": oid})
    return {"message": "Conversation deleted"}
