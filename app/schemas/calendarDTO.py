from pydantic import BaseModel
import uuid
from datetime import date
class DayData(BaseModel):
    date: date
    highest_bid: int
    active_bids: int
    minimum_to_win: int
    base_price: int
    demand_level: str
    success_rate: int
    is_available: bool
    is_booked: bool
class PropertyCalendarResponseData(BaseModel):
    property_id: int
    month: int
    year: int
    days: list[DayData]
class MessageResponseDTO(BaseModel):
    success: bool
    message: str
    Details: dict