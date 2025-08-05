from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.sessions.session import Base

class Wishlist(Base):
    __tablename__ = "wishlist"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_private = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now())
    updated_at = Column(DateTime, default=lambda: datetime.now(), onupdate=lambda: datetime.now())

    # Relationship
    user = relationship("User", back_populates="wishlists")
    properties = relationship("WishlistProperty", back_populates="wishlist", foreign_keys="[WishlistProperty.wishlist_id]")

# Imports ở cuối để tránh looped
from app.db.models.user import User
from app.db.models.wishlist_property import WishlistProperty