from pydantic import BaseModel
class DailyWinner(BaseModel):
    """Pydantic model cho daily winner - chỉ trả về thông tin winner từng ngày"""
    date: str
    user_id: int
    price_per_day: float
    total_amount: float

    class Config:
        from_attributes = True