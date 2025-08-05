from typing import List
from sqlalchemy.orm import Session
from app.features.property.schemas.AmenityDTO import AmenityDTO
from app.features.property.repositories.property_amenity_repository import PropertyAmenityRepository
from app.features.property.repositories.amenity_repository import AmenityRepository
from uuid import UUID as UUIDType

class PropertyAmenityService:
    def __init__(self, property_amenity_repository: PropertyAmenityRepository, amenity_repository: AmenityRepository):
        self.property_amenity_repository = property_amenity_repository
        self.amenity_repository = amenity_repository

    def get_available_amenities(self) -> List[AmenityDTO]:
        """Retrieve all available amenities for user selection."""
        amenities = self.amenity_repository.get_all()
        return [AmenityDTO.model_validate(amenity) for amenity in amenities]

    def assign_amenities_to_property(self, property_id: int, amenity_ids: List[UUIDType]) -> bool:
        """Assign selected amenities to a property."""
        self.property_amenity_repository.delete_by_property_id(property_id)
        for amenity_id in amenity_ids:
            self.property_amenity_repository.create(property_id, amenity_id)
        return True