"""Review model."""

from decimal import Decimal
from typing import Optional
from uuid import UUID

from sqlmodel import SQLModel, Field

from .base import BaseModel, TimestampMixin


class Review(BaseModel, TimestampMixin, table=True):
    """Review model."""
    
    __tablename__ = "reviews"
    
    booking_id: Optional[UUID] = Field(foreign_key="bookings.id")
    reviewer_id: int = Field(foreign_key="users.id")
    reviewee_id: int = Field(foreign_key="users.id")
    property_id: int = Field(foreign_key="properties.id")
    rating: Decimal
    review_text: Optional[str] = None
    review_type: str
    response_text: Optional[str] = None
    is_visible: bool = Field(default=True)
    accuracy_rating: Optional[Decimal] = None
    checking_rating: Optional[Decimal] = None
    cleanliness_rating: Optional[Decimal] = None
    communication_rating: Optional[Decimal] = None
    location_rating: Optional[Decimal] = None
    value_rating: Optional[Decimal] = None