from typing import List
from app.features.property.schemas.PropertyImageDTO import PropertyImageDTO
from app.features.property.repositories.property_image_repository import PropertyImageRepository

class PropertyImageService:
    def __init__(self, property_image_repository: PropertyImageRepository):
        self.property_image_repository = property_image_repository

    def get_images_by_property_id(self, property_id: int) -> List[PropertyImageDTO]:
        """Retrieve all images for a property."""
        return self.property_image_repository.get_by_property_id(property_id)