import uuid
from sqlalchemy import Column, Date, DateTime, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from .basic import BasicModel

class SecondChanceOffer(BasicModel):
	__tablename__ = "second_chance_offers"

	bid_id = Column(UUID(as_uuid=True), ForeignKey("bids.id"), nullable=False)
	offered_check_in = Column(Date, nullable=False)
	offered_check_out = Column(Date, nullable=False)
	response_deadline = Column(DateTime, nullable=False)
	status = Column(String, default="WAITING")
	responded_at = Column(DateTime, nullable=True) 