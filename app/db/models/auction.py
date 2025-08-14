from sqlalchemy import UUID, BigInteger, Column, Integer, ForeignKey, Date, Numeric, String, Float, DateTime, Enum
from sqlalchemy.orm import relationship
from app.db.sessions.session import Base
from datetime import datetime
import enum

class AuctionStatus(str, enum.Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    ENDED = "ENDED"
    CANCELLED = "CANCELLED"

class AuctionObjective(str, enum.Enum):
    HIGHEST_TOTAL = "HIGHEST_TOTAL"
    HIGHEST_PER_NIGHT = "HIGHEST_PER_NIGHT"

class Auction(Base):
    __tablename__ = "auctions"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default="uuid_generate_v4()")
    property_id = Column(BigInteger, ForeignKey("properties.id"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    min_nights = Column(BigInteger, nullable=False, default=1)
    max_nights = Column(BigInteger, nullable=True)
    starting_price = Column(Numeric(10, 2), nullable=False)
    bid_increment = Column(Numeric(10, 2), nullable=False, default=1.00)
    minimum_bid = Column(Numeric(10, 2), nullable=False)
    auction_start_time = Column(DateTime, nullable=False)
    auction_end_time = Column(DateTime, nullable=False)
    objective = Column(String, nullable=False, default="HIGHEST_TOTAL")
    status = Column(String(50), nullable=False, default="PENDING")
    total_bids = Column(BigInteger, nullable=False, default=0)
    current_highest_bid = Column(Numeric(10, 2), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    property = relationship("Property", back_populates="auctions")
    bids = relationship("Bids", back_populates="auction")