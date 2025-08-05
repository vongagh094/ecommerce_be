"""Property models using SQLAlchemy to match existing database."""

from decimal import Decimal
from sqlalchemy import Column, Integer, String, Text, Boolean, Numeric, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from ...db.sessions.session import Base


class Property(Base):
    """Property model matching the database schema."""
    
    __tablename__ = "properties"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    host_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
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
    latitude = Column(Numeric(10, 8))
    longitude = Column(Numeric(11, 8))
    base_price = Column(Numeric(10, 2), nullable=False)
    cleaning_fee = Column(Numeric(10, 2), default=0)
    cancellation_policy = Column(String(50), nullable=False)
    instant_book = Column(Boolean, default=False)
    minimum_stay = Column(Integer, default=1)
    home_tier = Column(Integer)
    is_guest_favorite = Column(Boolean)
    language = Column(String(10), default="en")
    status = Column(String(50), default="DRAFT")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    images = relationship("PropertyImage", back_populates="property")
    amenities = relationship("Amenity", secondary="property_amenities", back_populates="properties")
    highlights = relationship("PropertyHighlight", back_populates="property")
    house_rules = relationship("HouseRule", back_populates="property")
    location_descriptions = relationship("LocationDescription", back_populates="property")
    host = relationship("User", back_populates="properties")
    reviews = relationship("Review", back_populates="property")
    auctions = relationship("Auction", back_populates="property")


class PropertyImage(Base):
    """Property image model."""
    
    __tablename__ = "property_images"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    image_url = Column(Text, nullable=False)
    alt_text = Column(String(255))
    title = Column(String(255))
    display_order = Column(Integer, default=0)
    is_primary = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    property = relationship("Property", back_populates="images")


class PropertyAmenity(Base):
    """Property amenity junction table."""
    
    __tablename__ = "property_amenities"
    
    property_id = Column(Integer, ForeignKey("properties.id"), primary_key=True)
    amenity_id = Column(UUID(as_uuid=True), ForeignKey("amenities.id"), primary_key=True)


class Amenity(Base):
    """Amenity model."""
    
    __tablename__ = "amenities"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(Text, nullable=False)
    category = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    properties = relationship("Property", secondary="property_amenities", back_populates="amenities")


class PropertyHighlight(Base):
    """Property highlight model."""
    
    __tablename__ = "property_highlights"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    title = Column(String(255))
    subtitle = Column(String(255))
    icon = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    property = relationship("Property", back_populates="highlights")


class HouseRule(Base):
    """House rule model."""
    
    __tablename__ = "house_rules"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    rule_type = Column(String(50), default="general")
    title = Column(String(255))
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    property = relationship("Property", back_populates="house_rules")


class LocationDescription(Base):
    """Location description model."""
    
    __tablename__ = "location_descriptions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    description_type = Column(String(50), default="general")
    title = Column(String(255))
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    property = relationship("Property", back_populates="location_descriptions")


class User(Base):
    """User model."""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    username = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255))
    full_name = Column(String(255), nullable=False)
    first_name = Column(String(255))
    last_name = Column(String(255))
    profile_image_url = Column(Text)
    verification_status = Column(String(50))
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    is_super_host = Column(Boolean, default=False)
    host_about = Column(Text)
    host_review_count = Column(Integer)
    host_rating_average = Column(Numeric(3, 2))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Auth0 integration
    auth0_id = Column(String(255), unique=True)
    
    # Relationships
    properties = relationship("Property", back_populates="host")


class Review(Base):
    """Review model."""
    
    __tablename__ = "reviews"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    booking_id = Column(UUID(as_uuid=True), ForeignKey("bookings.id"))
    reviewer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    reviewee_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    rating = Column(Numeric(3, 2), nullable=False)
    review_text = Column(Text)
    review_type = Column(String(50), nullable=False)
    response_text = Column(Text)
    is_visible = Column(Boolean, default=True)
    accuracy_rating = Column(Numeric(3, 2))
    checking_rating = Column(Numeric(3, 2))
    cleanliness_rating = Column(Numeric(3, 2))
    communication_rating = Column(Numeric(3, 2))
    location_rating = Column(Numeric(3, 2))
    value_rating = Column(Numeric(3, 2))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    property = relationship("Property", back_populates="reviews")


class Auction(Base):
    """Auction model."""
    
    __tablename__ = "auctions"
    __table_args__ = {'extend_existing': True}
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    min_nights = Column(Integer, default=1)
    max_nights = Column(Integer)
    starting_price = Column(Numeric(10, 2), nullable=False)
    current_highest_bid = Column(Numeric(10, 2))
    bid_increment = Column(Numeric(10, 2), default=1.00)
    minimum_bid = Column(Numeric(10, 2), nullable=False)
    auction_start_time = Column(DateTime, nullable=False)
    auction_end_time = Column(DateTime, nullable=False)
    objective = Column(String(50), default="HIGHEST_TOTAL")
    status = Column(String(50), default="PENDING")
    winner_user_id = Column(Integer, ForeignKey("users.id"))
    total_bids = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    property = relationship("Property", back_populates="auctions")