# app/models/review.py
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, UUID
from sqlalchemy.sql import func
from .basic import BasicModel


class Review(BasicModel):
    __tablename__ = "reviews"

    booking_id = Column(UUID(as_uuid=True), nullable=True)
    reviewer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    reviewee_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=True)

    # Main review fields
    rating = Column(Integer, nullable=True)
    review_text = Column(String, nullable=False)
    review_type = Column(String, nullable=True)  # Có thể dùng Enum nếu có các type cố định
    response_text = Column(String, nullable=True)
    is_visible = Column(Boolean, default=True, nullable=False)

    # Detailed ratings
    accuracy_rating = Column(Integer, nullable=False)
    checking_rating = Column(Integer, nullable=False)
    cleanliness_rating = Column(Integer, nullable=False)
    communication_rating = Column(Integer, nullable=False)
    location_rating = Column(Integer, nullable=False)
    value_rating = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Review(id={self.id}, booking_id={self.booking_id}, " \
               f"reviewer_id={self.reviewer_id}, rating={self.rating})>"

    class Config:
        orm_mode = True