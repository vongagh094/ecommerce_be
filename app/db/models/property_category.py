from sqlalchemy import Column, String, Text, DateTime
from datetime import datetime
from app.db.sessions.session import Base

class PropertyCategory(Base):
    __tablename__ = "property_categories"

    name = Column(String(50), primary_key=True)
    description = Column(Text)
    created_at = Column(DateTime, default=lambda: datetime.now())