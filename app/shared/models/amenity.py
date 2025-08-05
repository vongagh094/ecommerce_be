"""Amenity model."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlmodel import SQLModel, Field

from .base import BaseModel


class Amenity(BaseModel, table=True):
    """Amenity model."""
    
    __tablename__ = "amenities"
    
    name: str
    category: str
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)