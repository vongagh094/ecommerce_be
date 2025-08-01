from enum import Enum
from .basic import BasicModel
from sqlalchemy import Column, DateTime, Integer, String, Boolean,ForeignKey, Enum as SqlEnum
from sqlalchemy.orm import relationship

class Auction_object(str, Enum):
    highest_total = "HIGHEST_TOTAL"
    highest_per_night = "HIGHEST_PER_NIGHT"
    hybrid = "HYBRID"
class Auction(BasicModel):
    __tablename__ = "auctions"

    property_id = Column(Integer, nullable=False)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    min_nights = Column(Integer)
    max_nights = Column(Integer)
    starting_price =Column(Integer,nullable=False)
    current_highest_bid = Column(Integer, nullable=False)
    bid_increment = Column(Integer)
    minimum_bid =Column(Integer)
    auction_start_time = Column(DateTime)
    auction_end_time =Column(DateTime)
    objective =Column(
        SqlEnum(Auction_object),
        default=Auction_object.highest_total,
        nullable=False
    )
    status = Column(String,default="activate")
    winner_user_id = Column(String)
    total_bids  = Column(Integer)

    #relationship
    bids = relationship("Bids",back_populates="auction")