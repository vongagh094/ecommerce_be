from pydantic import BaseModel
from uuid import UUID as UUIDType

class PropertyAmenityDTO(BaseModel):
    property_id: int
    amenity_id: UUIDType