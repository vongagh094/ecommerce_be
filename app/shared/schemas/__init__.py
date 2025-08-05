"""Shared Pydantic schemas for API contracts."""

from .base import BaseResponse, PaginatedResponse, ErrorResponse
from .user import UserResponse, UserCreate, UserUpdate
from .property import PropertyCard, PropertyResponse, PropertyCreate, PropertyUpdate
from .pagination import PaginationParams

__all__ = [
    "BaseResponse",
    "PaginatedResponse", 
    "ErrorResponse",
    "UserResponse",
    "UserCreate",
    "UserUpdate",
    "PropertyCard",
    "PropertyResponse",
    "PropertyCreate",
    "PropertyUpdate",
    "PaginationParams"
]