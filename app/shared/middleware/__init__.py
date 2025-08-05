"""Middleware module."""

from .error_handler import add_error_handlers
from .cors import setup_cors

__all__ = ["add_error_handlers", "setup_cors"]