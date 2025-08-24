from typing import Optional
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class BookingCreate(BaseModel):
    auction_id: UUID | None = None
    guest_id: int
    host_id: int
    property_id: int
    check_in_date: datetime
    check_out_date: datetime
    base_amount: float
    cleaning_fee: float = 0.0
    taxes: float = 0.0

    class Config:
        from_attributes = True

class BookingUpdate(BaseModel):
    check_in_date: datetime | None = None
    check_out_date: datetime | None = None
    base_amount: float | None = None
    cleaning_fee: float | None = 0.0
    taxes: float | None = 0.0
    booking_status: str | None = None
    payment_status: str | None = None

    class Config:
        from_attributes = True

class BookingResponse(BaseModel):
    id: UUID
    auction_id: UUID | None
    guest_id: int
    host_id: int
    property_id: int
    check_in_date: datetime
    check_out_date: datetime
    total_nights: int
    base_amount: float
    cleaning_fee: float
    taxes: float
    total_amount: float
    booking_status: str
    payment_status: str
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

class MonthlySales(BaseModel):
    month: str
    expected: float
    actual: float

    class Config:
        from_attributes = True

class OccupancyDataPoint(BaseModel):
    date: str
    occupancyRate: float
    period: str

    class Config:
        from_attributes = True

class PropertyStats(BaseModel):
    totalBooking: int
    totalBidActive: int
    sales: float
    expectedSales: float
    totalSales: float
    salesIncrease: float

    class Config:
        from_attributes = True
        
class PropertyResponse(BaseModel):
    id: int
    name: str
    location: Optional[str] = None

    class Config:
        from_attributes = True