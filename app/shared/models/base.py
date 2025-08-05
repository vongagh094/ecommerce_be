"""Base model classes."""

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field


class BaseModel(SQLModel):
    """Base model with common fields."""
    
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)


class TimestampMixin(SQLModel):
    """Mixin for timestamp fields."""
    
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)