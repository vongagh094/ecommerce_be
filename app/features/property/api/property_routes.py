import logging
from fastapi import APIRouter, Depends, Form, HTTPException, Request, UploadFile, File
from pydantic import ValidationError
import json
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
    data: str = Form(None),
    files: List[UploadFile] = File(None),
    db: Session = Depends(get_db_session),
    property_service: PropertyService = Depends(Provide[Container.property_service])
):
    try:
        if data:
            data_dict = json.loads(data)
            data = PropertyCreateDTO(**data_dict)
        else:
            raise ValueError("Missing data field")
        property = property_service.create_property(data, files)
        return property
    except json.JSONDecodeError as je:
        raise HTTPException(status_code=422, detail={"detail": f"Invalid JSON in data: {str(je)}"})
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail={"detail": ve.errors()})
    except ValueError as ve:
        raise HTTPException(status_code=422, detail={"detail": str(ve)})
    except Exception as e:
        raise HTTPException(status_code=500, detail={"detail": f"Lỗi server: {str(e)}"})

@router.put("/update/{property_id}", response_model=PropertyResponseDTO, operation_id="updateProperty")
@inject
async def update_property(
    property_id: int,
    data: str = Form(None),
    files: List[UploadFile] = File(None),
    db: Session = Depends(get_db_session),
    property_service: PropertyService = Depends(Provide[Container.property_service])
):
    try:
        if data:
            data_dict = json.loads(data)
            update_data = PropertyUpdateDTO(**data_dict)
        else:
            update_data = PropertyUpdateDTO()
        updated_property = property_service.update_property(property_id, update_data, files)
        if updated_property is None:
            raise HTTPException(status_code=404, detail={"detail": "Không tìm thấy bất động sản"})
        return updated_property
    except json.JSONDecodeError as je:
        raise HTTPException(status_code=422, detail={"detail": f"JSON không hợp lệ: {str(je)}"})
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail={"detail": ve.errors()})
    except ValueError as ve:
        raise HTTPException(status_code=422, detail={"detail": str(ve)})
    except Exception as e:
        raise HTTPException(status_code=500, detail={"detail": f"Lỗi server: {str(e)}"})

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
            raise HTTPException(status_code=404, detail={"detail": "Không tìm thấy bất động sản"})
        return {"message": "Xóa bất động sản thành công"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail={"detail": f"Lỗi server: {str(e)}"})