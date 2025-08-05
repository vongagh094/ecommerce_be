"""Auction type constants."""

from enum import Enum


class AuctionObjective(str, Enum):
    """Auction objective enumeration."""
    HIGHEST_TOTAL = "HIGHEST_TOTAL"
    HIGHEST_PER_NIGHT = "HIGHEST_PER_NIGHT"
    HYBRID = "HYBRID"


class AuctionStatus(str, Enum):
    """Auction status enumeration."""
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"