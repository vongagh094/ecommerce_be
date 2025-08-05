from pydantic import BaseModel
from datetime import datetime
from uuid import UUID as UUIDType
from typing import Optional

class PropertyImageDTO(BaseModel):
    id: Optional[UUIDType] = None
    image_url: str
    alt_text: Optional[str] = None
    title: Optional[str] = None
    display_order: int = 0
    is_primary: bool = False
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True