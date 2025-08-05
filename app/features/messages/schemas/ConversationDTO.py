from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict

class ConversationCreateDTO(BaseModel):
    property_id: Optional[int]
    guest_id: int
    host_id: int

class ConversationResponseDTO(BaseModel):
    id: int
    name: Optional[str] = None
    property_id: Optional[int]
    guest_id: int
    host_id: int
    last_message_at: Optional[datetime]
    is_archived: bool
    created_at: datetime
    property_title: Optional[str] = None
    other_user: Optional[Dict] = None

    class Config:
        from_attributes = True