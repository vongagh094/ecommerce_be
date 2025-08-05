from typing import List
from sqlalchemy.orm import Session
from app.db.models.property_amenity import PropertyAmenity
from app.db.models.amenity import Amenity
from app.features.property.schemas.AmenityDTO import AmenityDTO
from uuid import UUID as UUIDType

class PropertyAmenityRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, property_id: int, amenity_id: UUIDType) -> None:
        """Create a new property-amenity relationship."""
        property_amenity = PropertyAmenity(property_id=property_id, amenity_id=amenity_id)
        self.db.add(property_amenity)
        self.db.commit()

    def get_by_property_id(self, property_id: int) -> List[AmenityDTO]:
        """Get all amenities for a property."""
        amenities = (
            self.db.query(Amenity)
            .join(PropertyAmenity, PropertyAmenity.amenity_id == Amenity.id)
            .filter(PropertyAmenity.property_id == property_id)
            .all()
        )
        return [AmenityDTO.model_validate(amenity) for amenity in amenities]

    def delete_by_property_id(self, property_id: int) -> None:
        """Delete all property-amenity relationships for a property."""
        self.db.query(PropertyAmenity).filter(PropertyAmenity.property_id == property_id).delete()
        self.db.commit()