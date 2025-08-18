from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Numeric, BigInteger
from sqlalchemy.orm import relationship, foreign
from datetime import datetime
from app.db.sessions.session import Base

class Property(Base):
    __tablename__ = "properties"
    __table_args__ = {'extend_existing': True}

    id = Column(BigInteger, primary_key=True, index=True)
    host_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(String)
    # Schema uses plain varchar(50) without FK tables
    property_type = Column(String(50), nullable=False)
    category = Column(String(50), nullable=False)
    max_guests = Column(Integer, nullable=False)
    bedrooms = Column(Integer)
    bathrooms = Column(Integer)
    address_line1 = Column(String(255))
    city = Column(String(100))
    state = Column(String(100))
    country = Column(String(100))
    postal_code = Column(String(20))
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

    # Relationships - using string references to avoid circular imports
    host = relationship("User", back_populates="properties")
    images = relationship("PropertyImage", back_populates="property")
    # Association table collection (write path)
    property_amenities = relationship("PropertyAmenity", back_populates="property", cascade="all, delete-orphan")
    # Direct many-to-many to amenities for convenience (read-only to avoid overlap writes)
    amenities = relationship("Amenity", secondary="property_amenities", back_populates="properties", viewonly=True, overlaps="property_amenities,amenity,properties")
    conversations = relationship("Conversation", back_populates="property")

    # Property extras per schema
    highlights = relationship("PropertyHighlight", back_populates="property")
    house_rules = relationship("HouseRule", back_populates="property")
    location_descriptions = relationship("LocationDescription", back_populates="property")

    # Read-only link to auctions without touching auction model
    auctions = relationship(
        "AuctionDB",
        primaryjoin="Property.id == foreign(AuctionDB.property_id)",
        viewonly=True,
        lazy="selectin",
    )

# Remove circular imports - use string references in relationships instead