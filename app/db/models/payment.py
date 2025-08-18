import uuid
from datetime import datetime, timedelta
from sqlalchemy import Column, DateTime, String, BigInteger, Integer, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID, JSONB
from .basic import BasicModel

class PaymentSession(BasicModel):
	__tablename__ = "payment_sessions"

	user_id = Column(BigInteger, nullable=False)
	auction_id = Column(UUID(as_uuid=True), nullable=False)
	bid_id = Column(UUID(as_uuid=True), nullable=False)
	app_trans_id = Column(String, unique=True, nullable=False, index=True)
	amount = Column(Integer, nullable=False)
	selected_nights = Column(JSONB, nullable=False)
	status = Column(String, default="PENDING")
	idempotency_key = Column(String, unique=True, nullable=True)
	expires_at = Column(DateTime, nullable=True)
	order_url = Column(String, nullable=True)

class PaymentTransaction(BasicModel):
	__tablename__ = "payment_transactions"

	session_id = Column(UUID(as_uuid=True), ForeignKey("payment_sessions.id"), nullable=False, index=True)
	app_trans_id = Column(String, nullable=False, index=True)
	zp_trans_id = Column(String, nullable=True)
	amount = Column(Integer, nullable=False)
	status = Column(String, default="PENDING")
	paid_at = Column(DateTime, nullable=True)
	raw = Column(JSONB, nullable=True) 