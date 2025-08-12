# subscription.py
from sqlalchemy import Column, BigInteger, ForeignKey, String, Text
from sqlalchemy.orm import relationship
from app.db.sessions.session import Base

class Subscription(Base):
    __tablename__ = "subscription"

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False, index=True)
    endpoint = Column(Text, nullable=False)
    p256dh = Column(String(255), nullable=False)
    auth = Column(String(255), nullable=False)

    # Sửa relationship
    user = relationship("User", back_populates="subscription")

# Import ở cuối
from app.db.models.user import User