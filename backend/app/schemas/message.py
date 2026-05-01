from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class MessageBase(BaseModel):
    content: str
    type: str = "text"
    file_url: Optional[str] = None

class MessageCreate(MessageBase):
    conversation_id: int

class MessageResponse(MessageBase):
    id: int
    conversation_id: int
    sender_id: int
    is_read: bool
    read_at: Optional[datetime] = None
    created_at: datetime
    sender: Optional[dict] = None
    
    class Config:
        from_attributes = True

class ConversationResponse(BaseModel):
    id: int
    participants: List[dict]
    last_message: Optional[dict] = None
    unread_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True
