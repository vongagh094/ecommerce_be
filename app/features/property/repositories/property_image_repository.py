from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.models.property_image import PropertyImage
from app.features.property.schemas.PropertyImageDTO import PropertyImageDTO
from uuid import UUID as UUIDType

class PropertyImageRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, property_id: int, images: List[PropertyImageDTO]) -> List[PropertyImageDTO]:
        """Tạo mới các ảnh cho bất động sản."""
        created_images = []
        for image in images:
            property_image = PropertyImage(
                property_id=property_id,
                image_url=image.image_url,
                alt_text=image.alt_text,
                title=image.title,
                display_order=image.display_order,
                is_primary=image.is_primary
            )
            self.db.add(property_image)
            self.db.commit()
            self.db.refresh(property_image)
            created_images.append(PropertyImageDTO.model_validate(property_image))
        return created_images
    
    def get_by_id(self, image_id: UUIDType) -> Optional[PropertyImageDTO]:
        """Lấy ảnh theo ID."""
        image = self.db.query(PropertyImage).filter(PropertyImage.id == image_id).first()
        return PropertyImageDTO.model_validate(image) if image else None

    def get_by_property_id(self, property_id: int) -> List[PropertyImageDTO]:
        """Lấy tất cả ảnh của một bất động sản"""
        images = self.db.query(PropertyImage).filter(PropertyImage.property_id == property_id).order_by(PropertyImage.display_order).all()
        return [PropertyImageDTO.model_validate(image) for image in images]

    def delete_by_property_id(self, property_id: int) -> None:
        """Xóa tất cả ảnh của một bất động sản."""
        self.db.query(PropertyImage).filter(PropertyImage.property_id == property_id).delete()
        self.db.commit()

    def delete_by_id(self, image_id: UUIDType) -> bool:
        """Xóa một ảnh cụ thể theo ID."""
        image = self.db.query(PropertyImage).filter(PropertyImage.id == image_id).first()
        if image:
            self.db.delete(image)
            self.db.commit()
            return True
        return False

    def update_image(self, image_id: UUIDType, image_data: PropertyImageDTO) -> Optional[PropertyImageDTO]:
        """Cập nhật thông tin ảnh (ví dụ: display_order, is_primary, alt_text, title)."""
        image = self.db.query(PropertyImage).filter(PropertyImage.id == image_id).first()
        if image:
            if image_data.image_url is not None:
                image.image_url = image_data.image_url
            if image_data.alt_text is not None:
                image.alt_text = image_data.alt_text
            if image_data.title is not None:
                image.title = image_data.title
            if image_data.display_order is not None:
                image.display_order = image_data.display_order
            if image_data.is_primary is not None:
                image.is_primary = image_data.is_primary
            self.db.commit()
            self.db.refresh(image)
            return PropertyImageDTO.model_validate(image)
        return None