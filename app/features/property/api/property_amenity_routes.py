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

@router.get("/available", response_model=List[AmenityDTO], operation_id="getAvailableAmenities")
@inject
async def get_available_amenities(
    db: Session = Depends(get_db_session),
    property_amenity_service: PropertyAmenityService = Depends(Provide[Container.property_amenity_service])
):
    try:
        amenities = property_amenity_service.get_available_amenities()
        return amenities
    except Exception as e:
        raise HTTPException(status_code=500, detail={"detail": f"Internal server error: {str(e)}"})