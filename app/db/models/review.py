# app/models/review.py
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, UUID
from sqlalchemy.sql import func
from .basic import BasicModel


class Review(BasicModel):
    __tablename__ = "reviews"

    booking_id = Column(UUID(as_uuid=True), ForeignKey("bookings.id"), nullable=False)
    reviewer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    reviewee_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)

    # Main review fields
    rating = Column(Integer, nullable=False)
    review_text = Column(String, nullable=True)
    review_type = Column(String, nullable=False)  # Có thể dùng Enum nếu có các type cố định
    response_text = Column(String, nullable=True)
    is_visible = Column(Boolean, default=True, nullable=False)

    # Detailed ratings
    accuracy_rating = Column(Integer, nullable=True)
    checking_rating = Column(Integer, nullable=True)
    cleanliness_rating = Column(Integer, nullable=True)
    communication_rating = Column(Integer, nullable=True)
    location_rating = Column(Integer, nullable=True)
    value_rating = Column(Integer, nullable=True)

    def __repr__(self):
        return f"<Review(id={self.id}, booking_id={self.booking_id}, " \
               f"reviewer_id={self.reviewer_id}, rating={self.rating})>"

    class Config:
        orm_mode = True