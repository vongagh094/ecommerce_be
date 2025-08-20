from pydantic import BaseModel, Field

class SubscriptionDTO(BaseModel):
    user_id: int
    endpoint: str = Field(..., max_length=2000)
    p256dh: str
    auth: str

    class Config:
        from_attributes = True