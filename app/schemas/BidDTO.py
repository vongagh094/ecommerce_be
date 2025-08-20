from pydantic import BaseModel
from datetime import datetime
class BidsDTO(BaseModel):
    user_id: int
    property_id: int
    auction_id: str
    bid_amount: int
    bid_time: str
    check_in: str
    check_out: str
    allow_partial: bool
    partial_awarded: bool
    created_at: str

class BidRecord(BaseModel):
    id: str
    user_id: int
    property_id: int
    auction_id: str
    bid_amount: int
    bid_time: datetime
    check_in: datetime
    check_out: datetime