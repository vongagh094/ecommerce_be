from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel, field_serializer
from datetime import datetime
from app.db.sessions.session import get_db_session
from app.db.models.property_category import PropertyCategory

router = APIRouter()

class PropertyCategoryDTO(BaseModel):
    name: str
    description: str | None = None
    created_at: datetime  # Changed to datetime

    @field_serializer('created_at')
    def serialize_created_at(self, created_at: datetime, _info):
        return created_at.isoformat()  # Convert datetime to ISO 8601 string

    class Config:
        from_attributes = True

@router.get("/available", response_model=List[PropertyCategoryDTO], operation_id="getPropertyCategories")
async def get_property_categories(db: Session = Depends(get_db_session)):
    try:
        property_categories = db.query(PropertyCategory).all()
        return [PropertyCategoryDTO.model_validate(pc) for pc in property_categories]
    except Exception as e:
        raise HTTPException(status_code=500, detail={"detail": f"Internal server error: {str(e)}"})