from pydantic import BaseModel
from uuid import UUID as UUIDType
from typing import Optional

class PropertyImageDTO(BaseModel):
    id: Optional[UUIDType] = None
    image_url: Optional[str] = None
    alt_text: Optional[str] = None
    title: Optional[str] = None
    display_order: int = 0
    is_primary: bool = False

    class Config:
        from_attributes = True