"""Authentication and authorization exceptions."""

from .base import AppException


class AuthenticationError(AppException):
    """Raised when authentication fails."""
    
    def __init__(self, message: str = "Authentication required"):
        super().__init__(message, "AUTH_REQUIRED", 401)


class AuthorizationError(AppException):
    """Raised when user lacks required permissions."""
    
    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(message, "INSUFFICIENT_PERMISSIONS", 403)


class TokenExpiredError(AppException):
    """Raised when JWT token is expired."""
    
    def __init__(self, message: str = "Token expired"):
        super().__init__(message, "TOKEN_EXPIRED", 401)


class InvalidTokenError(AppException):
    """Raised when JWT token is invalid."""
    
    def __init__(self, message: str = "Invalid token"):
        super().__init__(message, "INVALID_TOKEN", 401)