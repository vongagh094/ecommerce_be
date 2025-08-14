from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.sessions.session import Base

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    host_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(String)
    property_type = Column(String(50), ForeignKey("property_types.name"), nullable=False)
    category = Column(String(50), ForeignKey("property_categories.name"), nullable=False)
    max_guests = Column(Integer, nullable=False)
    bedrooms = Column(Integer)
    bathrooms = Column(Integer)
    address_line1 = Column(String(255))
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)
    postal_code = Column(String(20), nullable=False)
    latitude = Column(Numeric(precision=10, scale=8))
    longitude = Column(Numeric(precision=11, scale=8))
    base_price = Column(Numeric(10, 2), nullable=False)
    cleaning_fee = Column(Numeric(10, 2), default=0)
    cancellation_policy = Column(String(50), nullable=False)
    instant_book = Column(Boolean, default=False)
    minimum_stay = Column(Integer, default=1)
    home_tier = Column(Integer)
    is_guest_favorite = Column(Boolean, default=None)
    language = Column(String(10), default="en")
    status = Column(String(50), default="DRAFT")
    created_at = Column(DateTime, default=lambda: datetime.now())
    updated_at = Column(DateTime, default=lambda: datetime.now(), onupdate=lambda: datetime.now())

    # Relationships
    host = relationship("User", back_populates="properties")
    images = relationship("PropertyImage", back_populates="property", foreign_keys="[PropertyImage.property_id]")
    amenities = relationship("PropertyAmenity", back_populates="property", foreign_keys="[PropertyAmenity.property_id]")
    conversations = relationship("Conversation", back_populates="property", foreign_keys="[Conversation.property_id]")
    auctions = relationship("Auction", back_populates="property", foreign_keys="[Auction.property_id]")

# Imports ở cuối để tránh looped
from app.db.models.user import User
from app.db.models.property_image import PropertyImage
from app.db.models.property_amenity import PropertyAmenity
from app.db.models.conversation import Conversation
# from app.db.models.auction import Auction