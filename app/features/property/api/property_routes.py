from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.features.property.schemas.PropertyDTO import PropertyCreateDTO, PropertyResponseDTO, PropertyUpdateDTO
from app.db.sessions.session import get_db_session
from app.core.container import Container
from dependency_injector.wiring import inject, Provide
from app.features.property.services.property_service import PropertyService

router = APIRouter()

@router.get("/list", response_model=List[PropertyResponseDTO], operation_id="listProperties")
@inject
async def get_properties(
    limit: int = 12,
    offset: int = 0,
    db: Session = Depends(get_db_session),
    property_service: PropertyService = Depends(Provide[Container.property_service])
):
    try:
        properties = property_service.get_properties(limit, offset)
        return properties
    except Exception as e:
        raise HTTPException(status_code=500, detail={"detail": f"Internal server error: {str(e)}"})

@router.get("/{property_id}", response_model=PropertyResponseDTO, operation_id="getPropertyById")
@inject
async def get_property(
    property_id: int,
    db: Session = Depends(get_db_session),
    property_service: PropertyService = Depends(Provide[Container.property_service])
):
    try:
        property = property_service.get_by_id(property_id)
        if not property:
            raise HTTPException(status_code=404, detail={"detail": "Property not found"})
        return property
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail={"detail": f"Internal server error: {str(e)}"})

@router.get("/host/{host_id}/properties", response_model=List[PropertyResponseDTO], operation_id="getPropertiesByHost")
@inject
async def get_properties_by_host(
    host_id: int,
    limit: int = 12,
    offset: int = 0,
    db: Session = Depends(get_db_session),
    property_service: PropertyService = Depends(Provide[Container.property_service])
):
    try:
        properties = property_service.get_properties_by_host(host_id, limit, offset)
        return properties
    except Exception as e:
        raise HTTPException(status_code=500, detail={"detail": f"Internal server error: {str(e)}"})

@router.post("/create", response_model=PropertyResponseDTO, operation_id="createProperty")
@inject
async def create_property(
    data: PropertyCreateDTO,
    db: Session = Depends(get_db_session),
    property_service: PropertyService = Depends(Provide[Container.property_service])
):
    try:
        property = property_service.create_property(data)
        return property
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail={"detail": f"Internal server error: {str(e)}"})

@router.put("/update/{property_id}", response_model=PropertyResponseDTO, operation_id="updateProperty")
@inject
async def update_property(
    property_id: int,
    data: PropertyUpdateDTO,
    db: Session = Depends(get_db_session),
    property_service: PropertyService = Depends(Provide[Container.property_service])
):
    try:
        updated_property = property_service.update_property(property_id, data)
        if updated_property is None:
            raise HTTPException(status_code=404, detail={"detail": "Property not found"})
        return updated_property
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail={"detail": f"Internal server error: {str(e)}"})

@router.delete("/delete/{property_id}", operation_id="deleteProperty")
@inject
async def delete_property(
    property_id: int,
    db: Session = Depends(get_db_session),
    property_service: PropertyService = Depends(Provide[Container.property_service])
):
    try:
        success = property_service.delete_property(property_id)
        if not success:
            raise HTTPException(status_code=404, detail={"detail": "Property not found"})
        return {"message": "Property deleted successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail={"detail": f"Internal server error: {str(e)}"})