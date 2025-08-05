"""Property related models."""

from decimal import Decimal
from typing import Optional
from uuid import UUID

from sqlmodel import SQLModel, Field, Relationship

from .base import BaseModel, TimestampMixin


class Property(BaseModel, TimestampMixin, table=True):
    """Property model."""
    
    __tablename__ = "properties"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    host_id: int = Field(foreign_key="users.id")
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


class PropertyImage(BaseModel, TimestampMixin, table=True):
    """Property image model."""
    
    __tablename__ = "property_images"
    
    property_id: int = Field(foreign_key="properties.id")
    image_url: str
    alt_text: Optional[str] = None
    title: Optional[str] = None
    display_order: int = Field(default=0)
    is_primary: bool = Field(default=False)


class PropertyAmenity(SQLModel, table=True):
    """Property amenity junction table."""
    
    __tablename__ = "property_amenities"
    
    property_id: int = Field(foreign_key="properties.id", primary_key=True)
    amenity_id: UUID = Field(foreign_key="amenities.id", primary_key=True)