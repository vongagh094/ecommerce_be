import datetime
from sqlalchemy import Column, BigInteger, ForeignKey, String, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.sessions.session import Base

class Notification(Base):
    __tablename__ = "notification"

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    type = Column(String(50), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    link = Column(Text)
    is_read = Column(Boolean, default=False)
    is_pushed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now())

    # Sửa relationship - dùng tham chiếu chuỗi và khớp back_populates
    user = relationship("User", back_populates="notification")

# Import ở cuối để tránh circular imports
from app.db.models.user import User