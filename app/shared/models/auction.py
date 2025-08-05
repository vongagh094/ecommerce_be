"""Auction model."""

from datetime import datetime, date
from decimal import Decimal
from typing import Optional
from uuid import UUID

from sqlmodel import SQLModel, Field

from .base import BaseModel, TimestampMixin
from ..constants import AuctionObjective, AuctionStatus


class Auction(BaseModel, TimestampMixin, table=True):
    """Auction model."""
    
    __tablename__ = "auctions"
    
    property_id: int = Field(foreign_key="properties.id")
    start_date: date
    end_date: date
    min_nights: Optional[int] = Field(default=1)
    max_nights: Optional[int] = None
    starting_price: Decimal
    current_highest_bid: Optional[Decimal] = None
    bid_increment: Decimal = Field(default=Decimal("1.00"))
    minimum_bid: Decimal
    auction_start_time: datetime
    auction_end_time: datetime
    objective: AuctionObjective = Field(default=AuctionObjective.HIGHEST_TOTAL)
    status: str = Field(default="PENDING")
    winner_user_id: Optional[int] = Field(foreign_key="users.id")
    total_bids: int = Field(default=0)