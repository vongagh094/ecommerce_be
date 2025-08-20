from .basic import BasicModel
from sqlalchemy import Column, DateTime, Integer, String, Boolean, ForeignKey, Computed
from sqlalchemy.orm import relationship

class Bids(BasicModel):
    __tablename__= "bids"

    auction_id = Column(String, ForeignKey("auctions.id"), nullable=False)
    user_id = Column(Integer, nullable=False)
    check_in = Column(DateTime, nullable=False)
    check_out = Column(DateTime, nullable=False)
    nights = Column(Integer, Computed("GREATEST(1, check_out - check_in)"), nullable=False)
    total_amount = Column(Integer, nullable=False)
    price_per_night = Column(Integer, Computed("total_amount / GREATEST(1, check_out - check_in)"), nullable=False)
    allow_partial = Column(Boolean, nullable=False)
    partial_awarded = Column(Boolean, nullable=False)
    bid_time = Column(DateTime)
    status = Column(String, default="ACTIVE")

    # relationship
    auction = relationship("Auction", back_populates="bids")