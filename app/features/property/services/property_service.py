from typing import Optional, List
from sqlalchemy.orm import Session
from app.features.property.schemas.PropertyDTO import PropertyCreateDTO, PropertyResponseDTO, PropertyUpdateDTO
from app.features.property.repositories.property_repository import PropertyRepository
from app.features.property.repositories.property_amenity_repository import PropertyAmenityRepository
from app.features.property.repositories.property_image_repository import PropertyImageRepository
from app.db.models.user import User
from app.db.models.property_type import PropertyType
from app.db.models.property_category import PropertyCategory
from app.db.models.property import Property

class PropertyService:
    def __init__(self, property_repository: PropertyRepository, property_amenity_repository: PropertyAmenityRepository, property_image_repository: PropertyImageRepository):
        self.property_repository = property_repository
        self.property_amenity_repository = property_amenity_repository
        self.property_image_repository = property_image_repository
        self.db = property_repository.db

    def create_property(self, data: PropertyCreateDTO) -> PropertyResponseDTO:
        """Create a new property with validation logic."""
        if not self.db.query(PropertyType).filter(PropertyType.name == data.property_type).first():
            raise ValueError(f"Invalid property_type: {data.property_type}")
        if not self.db.query(PropertyCategory).filter(PropertyCategory.name == data.category).first():
            raise ValueError(f"Invalid category: {data.category}")

        property = self.property_repository.create(data)
        if data.amenities:
            for amenity_data in data.amenities:
                self.property_amenity_repository.create(property.id, amenity_data.amenity_id)
        if data.images:
            # Truyền danh sách images như List[PropertyImageDTO]
            self.property_image_repository.create(property.id, data.images)
        return self.property_repository.get_by_id(property.id)

    def get_by_id(self, property_id: int) -> Optional[PropertyResponseDTO]:
        """Retrieve a property by ID."""
        return self.property_repository.get_by_id(property_id)

    def get_properties(self, limit: int, offset: int) -> List[PropertyResponseDTO]:
        """Retrieve properties with pagination and business logic."""
        return self.property_repository.get_all(limit, offset)

    def get_properties_by_host(self, host_id: int, limit: int, offset: int) -> List[PropertyResponseDTO]:
        """Retrieve properties by host ID with pagination."""
        return self.property_repository.get_by_host_id(host_id, limit, offset)

    def update_property(self, property_id: int, data: PropertyUpdateDTO) -> Optional[PropertyResponseDTO]:
        """Update property with business logic."""
        existing_property = self.property_repository.get_by_id(property_id)
        if not existing_property:
            return None

        if data.property_type and not self.db.query(PropertyType).filter(PropertyType.name == data.property_type).first():
            raise ValueError(f"Invalid property_type: {data.property_type}")
        if data.category and not self.db.query(PropertyCategory).filter(PropertyCategory.name == data.category).first():
            raise ValueError(f"Invalid category: {data.category}")

        if data.amenities:
            self.property_amenity_repository.delete_by_property_id(property_id)
            for amenity_data in data.amenities:
                self.property_amenity_repository.create(property_id, amenity_data.amenity_id)

        if data.images:
            self.property_image_repository.delete_by_property_id(property_id)
            for image_data in data.images:
                self.property_image_repository.create(property_id, image_data.image_url, image_data.alt_text, image_data.display_order, image_data.is_primary)

        update_data = data.model_dump(exclude_unset=True, exclude={"amenities", "images"})
        if update_data:
            self.property_repository.update(property_id, update_data)
        return self.property_repository.get_by_id(property_id)

    def delete_property(self, property_id: int) -> bool:
        """Delete a property."""
        return self.property_repository.delete(property_id)