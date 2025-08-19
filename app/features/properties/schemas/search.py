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
    
    

    categories: Optional[List[str]] = Field(None, description="Property categories")


class CategoryParams(PaginationParams):
    """Category browsing parameters."""
    
    category_name: str = Field(..., description="Category name")
    location: Optional[str] = Field(None, description="Location filter")
    check_in: Optional[date] = Field(None, description="Check-in date")
    check_out: Optional[date] = Field(None, description="Check-out date")
    guests: Optional[int] = Field(None, ge=1, description="Number of guests")