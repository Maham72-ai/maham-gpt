
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class CreateConversationRequest(BaseModel):
    title: str = Field(default="New Chat", max_length=100)

class RenameConversationRequest(BaseModel):
    title: str = Field(min_length=1, max_length=100)

class MessageResponse(BaseModel):
    id: str
    conversation_id: str
    role: str
    content: str
    created_at: datetime

class ConversationResponse(BaseModel):
    id: str
    user_id: str
    title: str
    created_at: datetime
    updated_at: datetime
    last_message_at: datetime
    message_count: Optional[int] = 0

class ConversationDetailResponse(ConversationResponse):
    messages: List[MessageResponse] = []

class SendMessageRequest(BaseModel):
    content: str = Field(min_length=1, max_length=5000)
