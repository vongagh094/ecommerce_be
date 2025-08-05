"""User model."""

from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlmodel import SQLModel, Field

from .base import TimestampMixin


class User(TimestampMixin, SQLModel, table=True):
    """User model."""
    
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    username: str = Field(unique=True, index=True)
    password_hash: Optional[str] = None
    full_name: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    profile_image_url: Optional[str] = None
    verification_status: Optional[str] = None
    is_active: bool = Field(default=True)
    is_admin: bool = Field(default=False)
    is_super_host: bool = Field(default=False)
    host_about: Optional[str] = None
    host_review_count: Optional[int] = None
    host_rating_average: Optional[Decimal] = None
    
    # Auth0 integration
    auth0_id: Optional[str] = Field(unique=True, index=True)