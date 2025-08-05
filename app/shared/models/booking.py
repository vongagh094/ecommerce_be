"""Booking model."""

from datetime import date
from decimal import Decimal
from typing import Optional
from uuid import UUID

from sqlmodel import SQLModel, Field

from .base import BaseModel, TimestampMixin
from ..constants import BookingStatus, PaymentStatus


class Booking(BaseModel, TimestampMixin, table=True):
    """Booking model."""
    
    __tablename__ = "bookings"
    
    auction_id: Optional[UUID] = Field(foreign_key="auctions.id")
    property_id: int = Field(foreign_key="properties.id")
    guest_id: int = Field(foreign_key="users.id")
    host_id: int = Field(foreign_key="users.id")
    check_in_date: date
    check_out_date: date
    total_nights: int
    base_amount: Decimal
    cleaning_fee: Decimal = Field(default=0)
    taxes: Decimal = Field(default=0)
    total_amount: Decimal
    booking_status: str = Field(default="PENDING")
    payment_status: str = Field(default="PENDING")