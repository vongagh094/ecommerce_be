"""User schemas."""

from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Base user schema."""
    
    email: EmailStr
    full_name: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    profile_image_url: Optional[str] = None


class UserCreate(UserBase):
    """User creation schema."""
    
    username: str
    password: Optional[str] = None
    auth0_id: Optional[str] = None


class UserUpdate(BaseModel):
    """User update schema."""
    
    full_name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    profile_image_url: Optional[str] = None
    host_about: Optional[str] = None


class UserResponse(UserBase):
    """User response schema."""
    
    id: int
    username: str
    is_active: bool
    is_super_host: bool
    host_about: Optional[str] = None
    host_review_count: Optional[int] = None
    host_rating_average: Optional[Decimal] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class HostProfile(BaseModel):
    """Host profile schema."""
    
    id: int
    full_name: str
    profile_image_url: Optional[str] = None
    is_super_host: bool
    host_about: Optional[str] = None
    host_review_count: Optional[int] = None
    host_rating_average: Optional[Decimal] = None
    created_at: datetime
    
    class Config:
        from_attributes = True