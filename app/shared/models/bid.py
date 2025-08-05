"""Bid model."""

from datetime import datetime, date
from decimal import Decimal
from typing import Optional
from uuid import UUID

from sqlmodel import SQLModel, Field

from .base import BaseModel, TimestampMixin


class Bid(BaseModel, TimestampMixin, table=True):
    """Bid model."""
    
    __tablename__ = "bids"
    
    auction_id: UUID = Field(foreign_key="auctions.id")
    user_id: int = Field(foreign_key="users.id")
    check_in: date
    check_out: date
    total_amount: Decimal
    allow_partial: bool = Field(default=True)
    partial_awarded: bool = Field(default=False)
    bid_time: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(default="ACTIVE")