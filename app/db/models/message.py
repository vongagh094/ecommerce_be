from sqlalchemy import Column, BigInteger, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.sessions.session import Base

class Message(Base):
    __tablename__ = "message"

    id = Column(BigInteger, primary_key=True, index=True)
    conversation_id = Column(BigInteger, ForeignKey("conversation.id"), nullable=False)
    sender_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    message_text = Column(Text)
    sent_at = Column(DateTime, default=lambda: datetime.now())
    is_read = Column(Boolean, default=False)

    # Relationships
    conversation = relationship("Conversation", back_populates="messages")
    sender = relationship("User")

from app.db.models.conversation import Conversation
from app.db.models.user import User