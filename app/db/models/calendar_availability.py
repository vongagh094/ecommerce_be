from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, Boolean, DateTime, Date, String, UUID, func
from app.db.sessions.session import Base

class CalendarAvailability(Base):
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
