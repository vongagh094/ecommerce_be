from pydantic import BaseModel, field_serializer
from datetime import datetime, date, time
from typing import Optional
from uuid import UUID

class AuctionCreateDTO(BaseModel):
    property_id: int
    start_date: date
    end_date: date
    min_nights: int
    max_nights: Optional[int] = None
    starting_price: float
    bid_increment: float
    minimum_bid: float
    auction_start_time: str
    auction_end_time: str
    objective: str

class AuctionResponseDTO(BaseModel):
    id: UUID
    property_id: int
    start_date: date
    end_date: date
    min_nights: int
    max_nights: Optional[int] = None
    starting_price: float
    bid_increment: float
    minimum_bid: float
    auction_start_time: datetime
    auction_end_time: datetime
    objective: str
    status: str
    total_bids: int
    current_highest_bid: Optional[float] = None
    created_at: datetime

    @field_serializer('start_date', 'end_date')
    def serialize_date(self, value: date, _info):
        return value.isoformat()

    @field_serializer('created_at', 'auction_start_time', 'auction_end_time')
    def serialize_datetime(self, value: datetime, _info):
        return value.isoformat()

    @field_serializer('id')
    def serialize_uuid(self, value: UUID, _info):
        return str(value)

    class Config:
        from_attributes = True