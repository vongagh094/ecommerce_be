# app/repositories/review_repository.py
from typing import Tuple, List, Optional
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.db.models.property import Property
from app.db.models.review import Review
from app.schemas.ReviewDTO import ReviewResponseDTO, ReviewRequestDTO
from fastapi import HTTPException
from app.db.models.user import User
import logging

logger = logging.getLogger(__name__)


class ReviewRepository:
    def __init__(self, db: Session):
        self.db = db
    def get_reviews_by_property_id(self, property_id: int) -> list:
        """Get all reviews for a property."""
        return self.db.query(Review).filter(Review.property_id == property_id).all()


    def get_info_user_review(self, user_id: int):
        return  self.db.query(User).filter(User.id == user_id).first()

    async def get_reviews_by_pagination(
            self,
            limit: int = 10,
            offset: int = 0,
            property_id: Optional[str] = None
    ) -> Tuple[List[ReviewResponseDTO], int]:
        """
        Get paginated reviews with total count
        Returns tuple of (reviews, total_count)
        """
        try:
            # Base query với join để lấy thông tin user
            query = select(Review).join(User, Review.reviewer_id == User.id)
            count_query = select(func.count(Review.id))

            # Add filters if property_id is provided
            if property_id:
                query = query.where(Review.property_id == property_id)
                count_query = count_query.where(Review.property_id == property_id)

            # Get total count
            total =  self.db.execute(count_query)
            total_count = total.scalar()

            # Get paginated results
            query = (
                query.order_by(Review.created_at.desc())
                .offset(offset)
                .limit(limit)
            )

            result =  self.db.execute(query)
            reviews = result.scalars().all()

            # Convert to DTO
            review_dtos = []
            for review in reviews:
                # Lấy thông tin user
                user_info = self.get_info_user_review(review.reviewer_id)

                # Tạo user dict theo format frontend cần
                user_dict = {
                    "name": user_info.username if user_info else "Unknown User",
                    "avatar": user_info.profile_image_url if (
                                user_info and user_info.profile_image_url) else "/placeholder.svg?height=40&width=40",
                    "date": review.created_at.strftime("%B %Y")  # Format: "December 2021"
                }

                review_dto = ReviewResponseDTO(
                    id=str(review.id),
                    user=user_dict,
                    comment=review.review_text,  # Mapping từ review_text sang comment
                    rating=review.rating
                )
                review_dtos.append(review_dto)

            return review_dtos, total_count

        except Exception as e:
            logger.error(f"Error fetching paginated reviews: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error: {str(e)}"
            )
