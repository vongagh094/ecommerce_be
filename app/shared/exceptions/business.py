"""Business logic exceptions."""

from .base import AppException


class BusinessLogicError(AppException):
    """Raised when business logic validation fails."""
    
    def __init__(self, message: str):
        super().__init__(message, "BUSINESS_LOGIC_ERROR", 400)


class DuplicateError(AppException):
    """Raised when trying to create a duplicate resource."""
    
    def __init__(self, resource: str, field: str, value: str):
        message = f"{resource} with {field} '{value}' already exists"
        super().__init__(message, "DUPLICATE_ERROR", 409, {
            "resource": resource,
            "field": field,
            "value": value
        })