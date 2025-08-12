from sqlalchemy import Column, Integer, ForeignKey, BigInteger
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.sessions.session import Base

class PropertyAmenity(Base):
    __tablename__ = "property_amenities"

    property_id = Column(BigInteger, ForeignKey("properties.id"), primary_key=True)
    amenity_id = Column(UUID(as_uuid=True), ForeignKey("amenities.id"), primary_key=True)

    # Relationships
    property = relationship("Property", back_populates="property_amenities")
    amenity = relationship("Amenity", back_populates="property_amenities")

# Imports ở cuối để tránh looped
from app.db.models.property import Property
from app.db.models.amenity import Amenity