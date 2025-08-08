# app/routes/review_routes.py
from fastapi import APIRouter, Depends, Query
from typing import Optional
from app.services.review_service import ReviewService
from app.schemas.ReviewDTO import PaginatedResponseDTO, ReviewRequestDTO, CreateReviewResponseDTO
from dependency_injector.wiring import inject, Provide
from app.core.container import Container
router = APIRouter()

@router.get("/get_reviews", response_model=PaginatedResponseDTO)
@inject
async def get_reviews(
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    property_id: Optional[str] = Query(default=None),
    service: ReviewService = Depends(Provide[Container.review_service])
):
    """
    Get paginated reviews with an optional property filter
    """
    return await service.get_paginated_reviews(
        limit=limit,
        offset=offset,
        property_id=property_id
    )


@router.post("/create_review", response_model=CreateReviewResponseDTO)
@inject
async def create_review(
        review_data: ReviewRequestDTO,
        service: ReviewService = Depends(Provide[Container.review_service])
):
    return await service.create_review(review_data)