from pydantic import BaseModel
from typing import List

class WishlistResponseDTO(BaseModel):
    property_ids: List[int]

    class Config:
        orm_mode = True