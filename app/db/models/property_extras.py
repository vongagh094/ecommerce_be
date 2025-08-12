from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, BigInteger, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.sessions.session import Base

class PropertyHighlight(Base):
    __tablename__ = "property_highlights"

    id = Column(BigInteger, primary_key=True, index=True)
    property_id = Column(BigInteger, ForeignKey("properties.id"), nullable=False)
    title = Column(String(255))
    subtitle = Column(String(255))
    icon = Column(String(100))
    created_at = Column(DateTime, default=lambda: datetime.now())

    property = relationship("Property", back_populates="highlights")


class HouseRule(Base):
    __tablename__ = "house_rules"

    id = Column(BigInteger, primary_key=True, index=True)
    property_id = Column(BigInteger, ForeignKey("properties.id"), nullable=False)
    rule_type = Column(String(50), default="general")
    title = Column(String(255))
    description = Column(Text)
    created_at = Column(DateTime, default=lambda: datetime.now())

    property = relationship("Property", back_populates="house_rules")


class LocationDescription(Base):
    __tablename__ = "location_descriptions"

    id = Column(BigInteger, primary_key=True, index=True)
    property_id = Column(BigInteger, ForeignKey("properties.id"), nullable=False)
    description_type = Column(String(50), default="general")
    title = Column(String(255))
    description = Column(Text)
    created_at = Column(DateTime, default=lambda: datetime.now())

    property = relationship("Property", back_populates="location_descriptions") 