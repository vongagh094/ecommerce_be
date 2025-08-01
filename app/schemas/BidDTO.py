from pydantic import BaseModel

class BidsDTO(BaseModel):
    user_id: str
    auction_id:str
    bid_amount: float
    bid_time: str
    check_in: str
    check_out: str
    allow_partial: bool
    created_at: str
