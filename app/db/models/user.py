from sqlalchemy import Column, Integer, String, Boolean, DateTime, Numeric, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.sessions.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
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
    host_review_count = Column(Integer, default=0)
    host_rating_average = Column(Numeric(3, 2))
    created_at = Column(DateTime, default=lambda: datetime.now())
    updated_at = Column(DateTime, default=lambda: datetime.now(), onupdate=lambda: datetime.now())

    # Relationships
    properties = relationship("Property", back_populates="host", foreign_keys="[Property.host_id]")
    wishlists = relationship("Wishlist", back_populates="user", foreign_keys="[Wishlist.user_id]")
    conversations_as_guest = relationship("Conversation", back_populates="guest", foreign_keys="[Conversation.guest_id]")
    conversations_as_host = relationship("Conversation", back_populates="host", foreign_keys="[Conversation.host_id]")
    notification = relationship("Notification", back_populates="user", foreign_keys="[Notification.user_id]")
    subscription = relationship("Subscription", back_populates="user", foreign_keys="[Subscription.user_id]")

# Imports ở cuối để tránh looped
from app.db.models.property import Property
from app.db.models.wishlist import Wishlist
from app.db.models.conversation import Conversation
from app.db.models.notification import Notification
from app.db.models.subscription import Subscription