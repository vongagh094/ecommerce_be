from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID as UUIDType

class AmenityDTO(BaseModel):
    id: UUIDType
    name: str
    icon: Optional[str] = None
    category: str
    created_at: datetime

    class Config:
        from_attributes = True