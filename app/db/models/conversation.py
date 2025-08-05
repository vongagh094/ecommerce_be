from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.sessions.session import Base

class Conversation(Base):
    __tablename__ = "conversation"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"))
    guest_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    host_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    last_message_at = Column(DateTime)
    is_archived = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now())

    # Relationships
    property = relationship("Property", back_populates="conversations")
    guest = relationship("User", back_populates="conversations_as_guest", foreign_keys="[Conversation.guest_id]")
    host = relationship("User", back_populates="conversations_as_host", foreign_keys="[Conversation.host_id]")
    messages = relationship("Message", back_populates="conversation")

# Imports ở cuối để tránh looped
from app.db.models.property import Property
from app.db.models.user import User
from app.db.models.message import Message