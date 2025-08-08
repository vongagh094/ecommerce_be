from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class NotificationDTO(BaseModel):
    user_id: int
    title: str
    message: str
    is_pushed: bool
    link: Optional[str] = None
    type: str

    class Config:
        from_attributes = True

class NotificationResponse(BaseModel):
    id: int
    user_id: int
    type: str
    title: str
    message: str
    link: Optional[str]
    is_read: bool
    is_pushed: bool
    created_at: datetime

    class Config:
        from_attributes = True