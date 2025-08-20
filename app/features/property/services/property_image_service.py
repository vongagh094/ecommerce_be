from typing import List, Optional
from urllib.parse import urlparse
from fastapi import UploadFile
from app.features.property.schemas.PropertyImageDTO import PropertyImageDTO
from app.features.property.repositories.property_image_repository import PropertyImageRepository
from app.core.supabase_client import supabase_client
import uuid
from uuid import UUID

class PropertyImageService:
    def __init__(self, property_image_repository: PropertyImageRepository):
        self.property_image_repository = property_image_repository

    def upload_and_create_images(self, property_id: int, files: List[UploadFile], image_data: List[PropertyImageDTO]) -> List[PropertyImageDTO]:
        """Tải hình ảnh lên Supabase và lưu vào cơ sở dữ liệu."""
        created_images = []
        for file, data in zip(files, image_data):
            file_extension = file.filename.split('.')[-1] if file.filename else 'jpg'
            file_name = f"{property_id}/{uuid.uuid4()}.{file_extension}"
            file_content = file.file.read()
            response = supabase_client.storage.from_("property-images").upload(file_name, file_content)
            print(f"Uploading file to Supabase: {file_name}")
            print(response)
            public_url = supabase_client.storage.from_("property-images").get_public_url(file_name)
            data.image_url = public_url
            created_images.extend(self.property_image_repository.create(property_id, [data]))
        return created_images

    def get_images_by_property_id(self, property_id: int) -> List[PropertyImageDTO]:
        """Lấy tất cả hình ảnh cho một bất động sản."""
        return self.property_image_repository.get_by_property_id(property_id)
    
    def delete_image(self, image_id: UUID) -> bool:
        """Xóa một ảnh cụ thể theo ID và xóa tệp trên Supabase."""
        image = self.property_image_repository.get_by_id(image_id)
        if not image or not image.image_url:
            print(f"No image found or no image_url for image_id: {image_id}")
            return False

        try:
            parsed_url = urlparse(image.image_url)
            file_path = parsed_url.path.split("/property-images/")[-1]

            supabase_client.storage.from_("property-images").remove([file_path])

            deleted = self.property_image_repository.delete_by_id(image_id)
            if not deleted:
                print(f"Failed to delete image record from database for image_id: {image_id}")
                return False

            return True
        except Exception as e:
            print(f"Error deleting file from Supabase for image_id {image_id}: {str(e)}")
            return False
    
    def update_image(self, image_id: UUID, image_data: PropertyImageDTO) -> Optional[PropertyImageDTO]:
        """Cập nhật thông tin ảnh, bảo vệ ảnh identity (display_order = 0)."""
        existing_image = self.property_image_repository.get_by_id(image_id)
        if existing_image and existing_image.display_order == 0 and image_data.display_order != 0:
            raise ValueError("Cannot change display_order of identity image (display_order = 0)")
        return self.property_image_repository.update_image(image_id, image_data)