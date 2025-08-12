"""Property related models."""

from decimal import Decimal
from typing import Optional
from uuid import UUID

from sqlmodel import SQLModel, Field, Relationship

from .base import BaseModel, TimestampMixin


class Property(BaseModel, TimestampMixin, table=False):
    """Property DTO (not a DB table)."""
    
    id: Optional[int] = Field(default=None)
    host_id: int = Field(default=None)
    title: str
    description: Optional[str] = None
    property_type: str
    category: str
    max_guests: int
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    address_line1: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None
    base_price: Decimal
    cleaning_fee: Decimal = Field(default=0)
    cancellation_policy: str
    instant_book: bool = Field(default=False)
    minimum_stay: int = Field(default=1)
    home_tier: Optional[int] = None
    is_guest_favorite: Optional[bool] = None
    language: str = Field(default="en")
    status: str = Field(default="DRAFT")


class PropertyImage(BaseModel, TimestampMixin, table=False):
    """Property image DTO (not a DB table)."""
    
    property_id: int = Field(default=None)
    image_url: str
    alt_text: Optional[str] = None
    title: Optional[str] = None
    display_order: int = Field(default=0)
    is_primary: bool = Field(default=False)


class PropertyAmenity(SQLModel, table=False):
    """Property amenity junction DTO (not a DB table)."""
    
    property_id: int = Field(default=None)
    amenity_id: UUID = Field(default=None)