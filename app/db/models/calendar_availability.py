<<<<<<< HEAD
from sqlalchemy import Column, Date, Boolean, BigInteger, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
=======
from pydantic import BaseModel
from sqlalchemy import Column, Integer, ForeignKey, Boolean, DateTime, Date, String, UUID
>>>>>>> 3519f739512297b0b4af42920c89cf4f736e1bad
from app.db.sessions.session import Base

class CalendarAvailability(Base):
<<<<<<< HEAD
	__tablename__ = "calendar_availability"
=======
    __tablename__ = "calendar_availability"
    id = Column(Integer, primary_key=True, index=True,nullable=False,autoincrement=True)
    auction_id = Column(UUID, ForeignKey("auctions.id"), nullable=False)
    property_id = Column(Integer, ForeignKey("properties.id"), primary_key=True)
    date = Column(Date, primary_key=True)
    is_available = Column(Boolean)
    bid_id = Column(String, ForeignKey("bids.id"), nullable=True)
    price_amount = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())


>>>>>>> 3519f739512297b0b4af42920c89cf4f736e1bad

	id = Column(BigInteger, primary_key=True)
	property_id = Column(BigInteger, ForeignKey("properties.id"), nullable=False)
	date = Column(Date, nullable=False)
	is_available = Column(Boolean, default=True)
	bid_id = Column(UUID(as_uuid=True), ForeignKey("bids.id"), nullable=True)
	price_amount = Column(Integer, nullable=True)
	created_at = Column(DateTime, default=lambda: datetime.now())
	updated_at = Column(DateTime, default=lambda: datetime.now(), onupdate=lambda: datetime.now()) 
