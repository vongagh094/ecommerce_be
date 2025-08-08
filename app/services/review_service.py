from datetime import datetime
from typing import Optional
import logging
from fastapi import HTTPException
from app.db.repositories.review_repository import ReviewRepository
from app.schemas.ReviewDTO import PaginatedResponseDTO, ReviewRequestDTO, CreateReviewResponseDTO

# Tạo logger cho module này
logger = logging.getLogger(__name__)

class ReviewService:
    def __init__(self, review_repository: ReviewRepository):
        self.review_repository = review_repository

    async def get_paginated_reviews(
        self,
        limit: int = 10,
        offset: int = 0,
        property_id: Optional[str] = None
    ) -> PaginatedResponseDTO:
        """
        Get paginated reviews with an optional property filter
        """
        try:
            # Validate pagination parameters
            limit = min(max(1, limit), 100)  # Limit between 1 and 100
            offset = max(0, offset)  # Offset cannot be negative

            # Get reviews and total count from the repository
            reviews, total_count = await self.review_repository.get_reviews_by_pagination(
                limit=limit,
                offset=offset,
                property_id=property_id
            )

            # Calculate if there are more items
            has_more = (offset + limit) < total_count

            # Return paginated response
            return PaginatedResponseDTO(
                items=reviews,
                total=total_count,
                limit=limit,
                offset=offset,
                has_more=has_more
            )

        except HTTPException:
            # Re-raise HTTPException từ repository
            raise
        except Exception as e:
            logger.error(f"Error in review service - get_paginated_reviews: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Service error: {str(e)}"
            )