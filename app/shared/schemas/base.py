"""Base schema classes."""

from typing import Any, Dict, Generic, List, Optional, TypeVar
from pydantic import BaseModel

T = TypeVar('T')


class BaseResponse(BaseModel):
    """Base response schema."""
    
    message: str = "Success"
    status_code: int = 200


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response schema."""
    
    data: List[T]
    pagination: Dict[str, Any]
    status_code: int = 200


class ErrorResponse(BaseModel):
    """Error response schema."""
    
    error: Dict[str, Any]
    status_code: int