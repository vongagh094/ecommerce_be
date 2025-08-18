from sqlalchemy import Column, Date, Boolean, BigInteger, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app.db.sessions.session import Base

class CalendarAvailability(Base):
	__tablename__ = "calendar_availability"

	id = Column(BigInteger, primary_key=True)
	property_id = Column(BigInteger, ForeignKey("properties.id"), nullable=False)
	date = Column(Date, nullable=False)
	is_available = Column(Boolean, default=True)
	bid_id = Column(UUID(as_uuid=True), ForeignKey("bids.id"), nullable=True)
	price_amount = Column(Integer, nullable=True)
	created_at = Column(DateTime, default=lambda: datetime.now())
	updated_at = Column(DateTime, default=lambda: datetime.now(), onupdate=lambda: datetime.now()) 