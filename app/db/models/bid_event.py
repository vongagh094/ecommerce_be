import uuid
from sqlalchemy import Column, DateTime, String, BigInteger, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime
from app.db.sessions.session import Base

class BidEvent(Base):
	__tablename__ = "bid_events"

	id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
	auction_id = Column(UUID(as_uuid=True), ForeignKey("auctions.id"), nullable=False)
	event_type = Column(String, nullable=False)
	user_id = Column(BigInteger, nullable=True)
	bid_id = Column(UUID(as_uuid=True), ForeignKey("bids.id"), nullable=True)
	event_data = Column(JSONB, nullable=True)
	event_time = Column(DateTime, default=lambda: datetime.now())
	created_at = Column(DateTime, default=lambda: datetime.now())
	updated_at = Column(DateTime, default=lambda: datetime.now(), onupdate=lambda: datetime.now()) 