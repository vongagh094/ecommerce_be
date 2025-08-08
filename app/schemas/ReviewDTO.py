from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class ReviewRequestDTO(BaseModel):
    user_id: int
    property_id: int
    review_text: str
    rating: int
    created_at: str


class ReviewResponseDTO(BaseModel):
    id: str
    user: dict  # Sẽ chứa name, avatar, date
    comment: str
    rating: int

    class Config:
        from_attributes = True


# Trong schemas/ReviewDTO.py
class PaginatedResponseDTO(BaseModel):
    items: List[ReviewResponseDTO]
    total: int
    limit: int
    offset: int
    has_more: bool

    class Config:
        from_attributes = True