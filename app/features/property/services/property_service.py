from importlib.resources import files
from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi import UploadFile
from app.features.property.schemas.PropertyDTO import PropertyCreateDTO, PropertyResponseDTO, PropertyUpdateDTO
from app.features.property.repositories.property_repository import PropertyRepository
from app.features.property.repositories.property_amenity_repository import PropertyAmenityRepository
from app.features.property.repositories.property_image_repository import PropertyImageRepository
from app.features.property.services.property_image_service import PropertyImageService
from app.db.models.user import User
from app.db.models.property_type import PropertyType
from app.db.models.property_category import PropertyCategory
from app.db.models.property import Property

class PropertyService:
    def __init__(self, property_repository: PropertyRepository, property_amenity_repository: PropertyAmenityRepository, property_image_repository: PropertyImageRepository):
        self.property_repository = property_repository
        self.property_amenity_repository = property_amenity_repository
        self.property_image_repository = property_image_repository
        self.property_image_service = PropertyImageService(property_image_repository)
        self.db = property_repository.db

    def create_property(self, data: PropertyCreateDTO, files: Optional[List[UploadFile]] = None) -> PropertyResponseDTO:
        """Create a new property with validation logic."""
        if not self.db.query(PropertyType).filter(PropertyType.name == data.property_type).first():
            raise ValueError(f"Invalid property_type: {data.property_type}")
        if not self.db.query(PropertyCategory).filter(PropertyCategory.name == data.category).first():
            raise ValueError(f"Invalid category: {data.category}")

        property = self.property_repository.create(data)
        if data.amenities:
            self.property_amenity_repository.delete_by_property_id(property.id)
            for amenity_id in data.amenities:
                self.property_amenity_repository.create(property.id, amenity_id)
        if files and data.images:
            self.property_image_service.upload_and_create_images(property.id, files, data.images)
        elif data.images:
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

    def update_property(self, property_id: int, data: PropertyUpdateDTO, files: Optional[List[UploadFile]] = None) -> Optional[PropertyResponseDTO]:
        """Cập nhật bất động sản."""
        existing_property = self.property_repository.get_by_id(property_id)
        if not existing_property:
            return None

        if data.property_type and not self.db.query(PropertyType).filter(PropertyType.name == data.property_type).first():
            raise ValueError(f"Loại bất động sản không hợp lệ: {data.property_type}")
        if data.category and not self.db.query(PropertyCategory).filter(PropertyCategory.name == data.category).first():
            raise ValueError(f"Danh mục không hợp lệ: {data.category}")

        # Cập nhật amenities nếu được cung cấp
        if data.amenities is not None:
            self.property_amenity_repository.delete_by_property_id(property_id)
            for amenity_id in data.amenities:
                self.property_amenity_repository.create(property_id, amenity_id)

        # Xử lý ảnh
        if data.images is not None:
            # Xóa ảnh nếu có deleted_image_ids
            if data.deletedImageIds:
                for image_id in data.deletedImageIds:
                    self.property_image_service.delete_image(image_id)

            # Đếm số lượng image_data mới (id: null)
            new_image_count = sum(1 for img in data.images if img.id is None)
            
            # Kiểm tra files
            files = files or []  # Nếu files là None, gán thành danh sách rỗng
            if new_image_count > len(files):
                raise ValueError(f"Không đủ tệp ảnh: {new_image_count} image_data mới nhưng chỉ có {len(files)} tệp")

            file_index = 0
            for image_data in data.images:
                if image_data.id:
                    self.property_image_service.update_image(image_data.id, image_data)
                else:
                    if file_index >= len(files):
                        raise ValueError(f"Không có tệp ảnh cho image_data mới tại index {file_index}")
                    self.property_image_service.upload_and_create_images(property_id, [files[file_index]], [image_data])
                    file_index += 1

        # Cập nhật các trường khác
        update_data = data.model_dump(exclude_unset=True, exclude={"amenities", "images", "deletedImageIds"})
        if update_data:
            self.property_repository.update(property_id, update_data)
        return self.property_repository.get_by_id(property_id)

    def delete_property(self, property_id: int) -> bool:
        """Delete a property."""
        return self.property_repository.delete(property_id)