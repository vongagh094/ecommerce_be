import uuid
from datetime import datetime

from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, UUID, DateTime, Numeric
from sqlalchemy.orm import relationship
from .basic import BasicModel
class Booking(BasicModel):
    __tablename__ = "bookings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    auction_id = Column(UUID(as_uuid=True), ForeignKey("auctions.id"), nullable=True)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    guest_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    host_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    check_in_date = Column(DateTime, nullable=False)
    check_out_date = Column(DateTime, nullable=False)
    total_nights = Column(Integer, nullable=False)
    base_amount = Column(Numeric(10, 2), nullable=False)
    cleaning_fee = Column(Numeric(10, 2), default=0)
    taxes = Column(Numeric(10, 2), default=0)
    total_amount = Column(Numeric(10, 2), nullable=False)
    booking_status = Column(String(50), default="PENDING")
    payment_status = Column(String(50), default="PENDING")
    created_at = Column(DateTime, default=lambda: datetime.now())
    updated_at = Column(DateTime, default=lambda: datetime.now(), onupdate=lambda: datetime.now())

    # relationships
    guest = relationship("User", foreign_keys=[guest_id])
    host = relationship("User", foreign_keys=[host_id])
    auction = relationship("Auction", back_populates="bookings")
    property = relationship("Property", back_populates="bookings")