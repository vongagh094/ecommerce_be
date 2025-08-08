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
    async def create_review(self, review_data: ReviewRequestDTO) -> CreateReviewResponseDTO:
        """
        Create a new review từ simple request (backward compatibility)
        """
        try:
            # Validate rating
            if not (1 <= review_data.rating <= 5):
                raise HTTPException(
                    status_code=400,
                    detail="Rating must be between 1 and 5"
                )

            # Validate review text
            if not review_data.review_text or len(review_data.review_text.strip()) == 0:
                raise HTTPException(
                    status_code=400,
                    detail="Review text cannot be empty"
                )

            # Validate user_id
            if not review_data.reviewer_id :
                raise HTTPException(
                    status_code=400,
                    detail="User ID cannot be empty"
                )

            # Validate user_id is numeric
            try:
                int(review_data.reviewer_id)
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail="User ID must be a valid number"
                )

            # Validate created_at a format
            try:
                datetime.fromisoformat(review_data.created_at.replace('Z', '+00:00'))
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid created_at format. Use ISO format"
                )

            # Create review - repository sẽ populate tất cả fields
            review_response = await self.review_repository.create_review(review_data)

            return CreateReviewResponseDTO(
                success=True,
                message="Review created successfully",
                review_id=review_response.id,
                data=review_response  # CompleteReviewResponseDTO với tất cả fields
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error in review service - create_review: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Service error: {str(e)}"
            )