from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
import uuid

class Chat(BaseModel):
    chat_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    participants: List[str]
    created_at: datetime = Field(default_factory=datetime.now)
    last_message: Optional[str] = None
    last_message_time: Optional[datetime] = None

class Message(BaseModel):
    message_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    chat_id: str
    sender_id: str
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)
    message_type: str = "text"
