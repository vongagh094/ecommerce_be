from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.sessions.session import Base

class WishlistProperty(Base):
    __tablename__ = "wishlist_property"

    wishlist_id = Column(Integer, ForeignKey("wishlist.id"), primary_key=True)
    property_id = Column(Integer, ForeignKey("properties.id"), primary_key=True)
    added_at = Column(DateTime, default=lambda: datetime.now())

    # Relationships
    wishlist = relationship("Wishlist", back_populates="properties")
    property = relationship("Property")

# Imports ở cuối để tránh looped
from app.db.models.wishlist import Wishlist
from app.db.models.property import Property