"""Property schemas."""

from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel

from .user import HostProfile


class PropertyImageResponse(BaseModel):
    """Property image response schema."""
    
    id: UUID
    image_url: str
    alt_text: Optional[str] = None
    is_primary: bool
    display_order: int
    
    class Config:
        from_attributes = True


class PropertyLocation(BaseModel):
    """Property location schema."""
    
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    address_line1: Optional[str] = None
    postal_code: Optional[str] = None
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None


class PropertyRating(BaseModel):
    """Property rating schema."""
    
    average: Decimal
    count: int


class PropertyCard(BaseModel):
    """Property card schema for search results."""
    # increase the id to 10 digits
    id: str
    title: str
    images: List[PropertyImageResponse]
    base_price: Decimal
    location: PropertyLocation
    rating: PropertyRating
    property_type: str
    max_guests: int
    is_guest_favorite: Optional[bool] = None
    host: HostProfile
    
    class Config:
        from_attributes = True


class PropertyBase(BaseModel):
    """Base property schema."""
    
    title: str
    description: Optional[str] = None
    property_type: str
    category: str
    max_guests: int
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    base_price: Decimal
    cleaning_fee: Decimal = Decimal("0")
    cancellation_policy: str
    instant_book: bool = False
    minimum_stay: int = 1


class PropertyCreate(PropertyBase):
    """Property creation schema."""
    
    host_id: int
    address_line1: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None


class PropertyUpdate(BaseModel):
    """Property update schema."""
    
    title: Optional[str] = None
    description: Optional[str] = None
    property_type: Optional[str] = None
    category: Optional[str] = None
    max_guests: Optional[int] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    base_price: Optional[Decimal] = None
    cleaning_fee: Optional[Decimal] = None
    cancellation_policy: Optional[str] = None
    instant_book: Optional[bool] = None
    minimum_stay: Optional[int] = None


class PropertyResponse(PropertyBase):
    """Property response schema."""
    
    id: int
    host_id: int
    location: PropertyLocation
    home_tier: Optional[int] = None
    is_guest_favorite: Optional[bool] = None
    language: str
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True