from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.features.property.schemas.PropertyAmenityDTO import PropertyAmenityDTO
from app.features.property.schemas.AmenityDTO import AmenityDTO
from app.db.sessions.session import get_db_session
from app.core.container import Container
from dependency_injector.wiring import inject, Provide
from app.features.property.services.property_amenity_service import PropertyAmenityService

router = APIRouter()

# thêm offset và limit vô đi
@router.get("/available", response_model=List[AmenityDTO], operation_id="getAvailableAmenities")
@inject
async def get_available_amenities(
    db: Session = Depends(get_db_session),
    property_amenity_service: PropertyAmenityService = Depends(Provide[Container.property_amenity_service]),
    offset: int = 0,
    limit: int = 100
):
    try:
        amenities = property_amenity_service.get_available_amenities(offset=offset, limit=limit)
        return amenities
    except Exception as e:
        raise HTTPException(status_code=500, detail={"detail": f"Internal server error: {str(e)}"})
    
# search amenity
@router.get("/search", response_model=List[AmenityDTO], operation_id="searchAmenities")
@inject
async def search_amenities(
    db: Session = Depends(get_db_session),
    property_amenity_service: PropertyAmenityService = Depends(Provide[Container.property_amenity_service]),
    query: str = "",
    offset: int = 0,
    limit: int = 100
):
    try:
        amenities = property_amenity_service.search_amenities(query=query, offset=offset, limit=limit)
        return amenities
    except Exception as e:
        raise HTTPException(status_code=500, detail={"detail": f"Internal server error: {str(e)}"})
