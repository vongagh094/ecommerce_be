from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict

class MessageCreateDTO(BaseModel):
    conversation_id: int
    sender_id: int
    message_text: str
    mark_as_read: Optional[bool] = False

class MessageUpdateDTO(BaseModel):
    is_read: Optional[bool] = None

class MessageResponseDTO(BaseModel):
    id: int
    conversation_id: int
    sender_id: int
    message_text: str
    is_read: bool
    sent_at: datetime
    sender: Dict

    class Config:
        from_attributes = True