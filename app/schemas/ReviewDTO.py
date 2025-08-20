from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class ReviewRequestDTO(BaseModel):
    reviewer_id: int
    reviewee_id: int
    property_id: int
    booking_id: str
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


class CompleteReviewRequestDTO(BaseModel):
    # Foreign keys - theo model mới
    booking_id: Optional[str] = None
    reviewer_id: Optional[int] = None
    reviewee_id: Optional[int] = None
    property_id: Optional[int] = None

    # Main review fields
    rating: Optional[int] = Field(None, ge=1, le=5)
    review_text: str  # Required field
    review_type: Optional[str] = "GUEST_TO_HOST"
    response_text: Optional[str] = None
    is_visible: Optional[bool] = True


# Complete Response DTO với tất cả fields
class CompleteReviewResponseDTO(BaseModel):
    # Primary key
    id: str

    # Foreign keys
    booking_id: Optional[str] = None
    reviewer_id: Optional[int] = None
    reviewee_id: Optional[int] = None
    property_id: Optional[int] = None

    # Main review fields
    rating: Optional[int] = None
    review_text: str
    review_type: Optional[str] = None
    response_text: Optional[str] = None
    is_visible: bool
# Response khi tạo thành công
class CreateReviewResponseDTO(BaseModel):
    success: bool
    message: str
    review_id: str
    data: CompleteReviewResponseDTO

    class Config:
        from_attributes = True
