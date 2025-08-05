"""Pagination schemas."""

from typing import Optional
from pydantic import BaseModel, Field

from ..constants import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE


class PaginationParams(BaseModel):
    """Pagination parameters."""
    
    page: int = Field(default=1, ge=1, description="Page number")
    limit: int = Field(
        default=DEFAULT_PAGE_SIZE, 
        ge=1, 
        le=MAX_PAGE_SIZE, 
        description="Items per page"
    )


class PaginationInfo(BaseModel):
    """Pagination information."""
    
    page: int
    limit: int
    total: int
    has_more: bool