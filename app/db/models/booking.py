import uuid
from sqlalchemy import Column, Date, Integer, String, BigInteger, DateTime, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from .basic import BasicModel

class Booking(BasicModel):
	__tablename__ = "bookings"

	auction_id = Column(UUID(as_uuid=True), ForeignKey("auctions.id"), nullable=True)
	property_id = Column(BigInteger, ForeignKey("properties.id"), nullable=False)
	guest_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
	host_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
	check_in_date = Column(Date, nullable=False)
	check_out_date = Column(Date, nullable=False)
	total_nights = Column(Integer, nullable=False)
	base_amount = Column(Integer, nullable=False)
	cleaning_fee = Column(Integer, default=0)
	taxes = Column(Integer, default=0)
	total_amount = Column(Integer, nullable=False)
	booking_status = Column(String, default="PENDING")
	payment_status = Column(String, default="PENDING")
	created_at = Column(DateTime, default=lambda: datetime.now())
	updated_at = Column(DateTime, default=lambda: datetime.now(), onupdate=lambda: datetime.now()) 