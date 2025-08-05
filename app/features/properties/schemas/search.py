"""Property search schemas."""

from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field

from ....shared.schemas.pagination import PaginationParams


class PropertySearchParams(PaginationParams):
    """Property search parameters."""
    
    location: Optional[str] = Field(None, description="City, state, or address")
    check_in: Optional[date] = Field(None, description="Check-in date")
    check_out: Optional[date] = Field(None, description="Check-out date")
    guests: Optional[int] = Field(None, ge=1, description="Number of guests")


class PropertyFilterParams(PropertySearchParams):
    """Advanced property filter parameters."""
    
    min_price: Optional[float] = Field(None, ge=0, description="Minimum price")
    max_price: Optional[float] = Field(None, ge=0, description="Maximum price")
    property_types: Optional[List[str]] = Field(None, description="Property types")
    amenities: Optional[List[str]] = Field(None, description="Amenity IDs")
    cancellation_policy: Optional[List[str]] = Field(None, description="Cancellation policies")
    instant_book: Optional[bool] = Field(None, description="Instant book only")
    min_rating: Optional[float] = Field(None, ge=0, le=5, description="Minimum rating")
    bedrooms: Optional[int] = Field(None, ge=0, description="Number of bedrooms")
    bathrooms: Optional[int] = Field(None, ge=0, description="Number of bathrooms")
    categories: Optional[List[str]] = Field(None, description="Property categories")


class CategoryParams(PaginationParams):
    """Category browsing parameters."""
    
    category_name: str = Field(..., description="Category name")
    location: Optional[str] = Field(None, description="Location filter")
    check_in: Optional[date] = Field(None, description="Check-in date")
    check_out: Optional[date] = Field(None, description="Check-out date")
    guests: Optional[int] = Field(None, ge=1, description="Number of guests")