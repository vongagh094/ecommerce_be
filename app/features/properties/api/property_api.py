"""Property API endpoints."""

from typing import List, Optional
from fastapi import APIRouter, Depends, Query, Path, HTTPException
from sqlmodel import Session

from ....shared.dependencies import get_db_session, get_pagination_params
from ....shared.schemas.pagination import PaginationParams
from ....shared.exceptions import NotFoundError
from ..repository import PropertyRepository
from ..services import PropertyService
from ..schemas.search import PropertySearchParams, PropertyFilterParams
from ..schemas.response import PropertySearchResponse, PropertyDetailsResponse

router = APIRouter(prefix="/properties", tags=["properties"])


def get_property_service(db: Session = Depends(get_db_session)) -> PropertyService:
    """Get property service instance."""
    repository = PropertyRepository(db)
    return PropertyService(repository)

@router.get("/categories", response_model=dict)
async def get_categories(
    service: PropertyService = Depends(get_property_service)
):
    """Get list of available property categories."""
    
    categories = await service.get_categories()
    print(categories)
    return {"categories": categories.get("icons", [])}


@router.get("/search", response_model=PropertySearchResponse)
async def search_properties(
    location: Optional[str] = Query(None, description="City, state, or address"),
    check_in: Optional[str] = Query(None, description="Check-in date (YYYY-MM-DD)"),
    check_out: Optional[str] = Query(None, description="Check-out date (YYYY-MM-DD)"),
    guests: Optional[int] = Query(None, ge=1, description="Number of guests"),
    pagination: PaginationParams = Depends(get_pagination_params),
    service: PropertyService = Depends(get_property_service)
):
    """Search properties by location, dates, and guest count."""
    
    params = PropertySearchParams(
        location=location,
        check_in=check_in,
        check_out=check_out,
        guests=guests,
        page=pagination.page,
        limit=pagination.limit
    )
    
    properties = await service.search_properties(params)
    return properties


@router.get("/filter", response_model=PropertySearchResponse)
async def filter_properties(
    # Basic search parameters
    location: Optional[str] = Query(None, description="City, state, or address"),
    check_in: Optional[str] = Query(None, description="Check-in date (YYYY-MM-DD)"),
    check_out: Optional[str] = Query(None, description="Check-out date (YYYY-MM-DD)"),
    guests: Optional[int] = Query(None, ge=1, description="Number of guests"),
    
    # Advanced filter parameters
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price"),
    property_types: Optional[List[str]] = Query(None, description="Property types"),
    amenities: Optional[List[str]] = Query(None, description="Amenity IDs"),
    cancellation_policy: Optional[List[str]] = Query(None, description="Cancellation policies"),
    instant_book: Optional[bool] = Query(None, description="Instant book only"),
    min_rating: Optional[float] = Query(None, ge=0, le=5, description="Minimum rating"),
    bedrooms: Optional[int] = Query(None, ge=0, description="Number of bedrooms"),
    bathrooms: Optional[int] = Query(None, ge=0, description="Number of bathrooms"),
    categories: Optional[List[str]] = Query(None, description="Property categories"),
    
    pagination: PaginationParams = Depends(get_pagination_params),
    service: PropertyService = Depends(get_property_service)
):
    """Filter properties with advanced criteria."""
    
    params = PropertyFilterParams(
        location=location,
        check_in=check_in,
        check_out=check_out,
        guests=guests,
        min_price=min_price,
        max_price=max_price,
        property_types=property_types,
        amenities=amenities,
        cancellation_policy=cancellation_policy,
        instant_book=instant_book,
        min_rating=min_rating,
        bedrooms=bedrooms,
        bathrooms=bathrooms,
        categories=categories,
        page=pagination.page,
        limit=pagination.limit
    )
    
    return await service.filter_properties(params)


@router.get("/categories/{category_name}", response_model=PropertySearchResponse)
async def get_properties_by_category(
    category_name: str = Path(..., description="Category name"),
    location: Optional[str] = Query(None, description="Location filter"),
    check_in: Optional[str] = Query(None, description="Check-in date (YYYY-MM-DD)"),
    check_out: Optional[str] = Query(None, description="Check-out date (YYYY-MM-DD)"),
    guests: Optional[int] = Query(None, ge=1, description="Number of guests"),
    pagination: PaginationParams = Depends(get_pagination_params),
    service: PropertyService = Depends(get_property_service)
):
    """Browse properties by specific category."""
    
    params = PropertySearchParams(
        location=location,
        check_in=check_in,
        check_out=check_out,
        guests=guests,
        page=pagination.page,
        limit=pagination.limit
    )
    
    return await service.get_properties_by_category(category_name, params)


@router.get("/{property_id}", response_model=PropertyDetailsResponse)
async def get_property_details(
    property_id: int = Path(..., description="Property ID"),
    service: PropertyService = Depends(get_property_service)
):
    """Get detailed property information."""
    
    try:
        return await service.get_property_details(property_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)


# Supporting endpoints

@router.get("/amenities/", response_model=dict)
async def get_amenities(
    service: PropertyService = Depends(get_property_service)
):
    """Get list of available amenities for filtering."""
    
    amenities = await service.get_amenities()
    return {"amenities": amenities}


@router.get("/locations/suggestions", response_model=dict)
async def get_location_suggestions(
    query: str = Query(..., description="Search query"),
    limit: int = Query(10, ge=1, le=50, description="Max suggestions"),
    service: PropertyService = Depends(get_property_service)
):
    """Provide location autocomplete suggestions."""
    
    suggestions = await service.get_location_suggestions(query, limit)
    return {"suggestions": suggestions}


