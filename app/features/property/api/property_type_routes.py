from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel, field_serializer
from datetime import datetime
from app.db.sessions.session import get_db_session
from app.db.models.property_type import PropertyType

router = APIRouter()

class PropertyTypeDTO(BaseModel):
    name: str
    description: str | None = None
    created_at: datetime  # Changed to datetime

    @field_serializer('created_at')
    def serialize_created_at(self, created_at: datetime, _info):
        return created_at.isoformat()  # Convert datetime to ISO 8601 string

    class Config:
        from_attributes = True

@router.get("/available", response_model=List[PropertyTypeDTO], operation_id="getPropertyTypes")
async def get_property_types(db: Session = Depends(get_db_session)):
    try:
        property_types = db.query(PropertyType).all()
        return [PropertyTypeDTO.model_validate(pt) for pt in property_types]
    except Exception as e:
        raise HTTPException(status_code=500, detail={"detail": f"Internal server error: {str(e)}"})