from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.models.property_image import PropertyImage
from app.features.property.schemas.PropertyImageDTO import PropertyImageDTO

class PropertyImageRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, property_id: int, images: List[PropertyImageDTO]) -> List[PropertyImageDTO]:
        """Create new property images."""
        created_images = []
        for image in images:
            property_image = PropertyImage(
                property_id=property_id,
                image_url=image.image_url,
                alt_text=image.alt_text,
                title=image.title,  # Lưu title để phân biệt ảnh giấy tờ
                display_order=image.display_order,
                is_primary=image.is_primary
                # id và created_at để database tự sinh
            )
            self.db.add(property_image)
            self.db.commit()
            self.db.refresh(property_image)
            created_images.append(PropertyImageDTO.model_validate(property_image))
        return created_images

    def get_by_property_id(self, property_id: int) -> List[PropertyImageDTO]:
        """Get all images for a property."""
        images = self.db.query(PropertyImage).filter(PropertyImage.property_id == property_id).all()
        return [PropertyImageDTO.model_validate(image) for image in images]

    def delete_by_property_id(self, property_id: int) -> None:
        """Delete all images for a property."""
        self.db.query(PropertyImage).filter(PropertyImage.property_id == property_id).delete()
        self.db.commit()