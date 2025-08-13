from sqlalchemy import Column, Integer, ForeignKey,Boolean
from sqlalchemy.orm import relationship
from app.db.models.basic import BasicModel

class CalendarAvailability(BasicModel):
    __tablename__ = "calendar_availability"

    property_id = Column(Integer, ForeignKey("properties.id"), primary_key=True)
    date = Column(Integer, primary_key=True)
    is_available = Column(Boolean)
    bid_id = Column(Integer, ForeignKey("bids.id"), nullable=True)
    price_amount = Column(Integer, nullable=True)

    # Relationships
    property = relationship("Property", back_populates="calendar_availability")
    bid = relationship("Bid", back_populates="calendar_availability")



