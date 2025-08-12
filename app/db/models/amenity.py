from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.sessions.session import Base

class Amenity(Base):
    __tablename__ = "amenities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now())

    # Relationship
    property_amenities = relationship("PropertyAmenity", back_populates="amenity")
    # Direct many-to-many to properties for convenience
    properties = relationship("Property", secondary="property_amenities", back_populates="amenities")

# Imports ở cuối để tránh looped
from app.db.models.property_amenity import PropertyAmenity