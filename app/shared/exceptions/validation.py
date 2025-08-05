"""Validation exceptions."""

from typing import Any, Dict, Optional
from .base import AppException


class ValidationError(AppException):
    """Raised when input validation fails."""
    
    def __init__(
        self, 
        message: str = "Validation failed", 
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, "VALIDATION_ERROR", 400, details)