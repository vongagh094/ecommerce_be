"""Not found exceptions."""

from .base import AppException


class NotFoundError(AppException):
    """Raised when a resource is not found."""
    
    def __init__(self, resource: str, identifier: str):
        message = f"{resource} not found"
        super().__init__(message, "NOT_FOUND", 404, {
            "resource": resource,
            "identifier": identifier
        })