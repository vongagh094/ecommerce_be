from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.sessions.session import Base

class PropertyImage(Base):
    __tablename__ = "property_images"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    image_url = Column(Text, nullable=False)
    alt_text = Column(String(255))
    title = Column(String(255))
    display_order = Column(Integer, default=0)
    is_primary = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now())

    # Relationship
    property = relationship("Property", back_populates="images")

from app.db.models.property import Property