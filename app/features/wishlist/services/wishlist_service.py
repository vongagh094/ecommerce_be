from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from app.features.wishlist.repositories.wishlist_repository import WishlistRepository
from app.features.wishlist.schemas.WishlistDTO import WishlistResponseDTO
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WishlistService:
    def __init__(self, db: Session):
        self.repository = WishlistRepository(db)
        
    def check_wishlist_exists(self, user_id: int) -> bool:
        existing_wishlist = self.repository.get_wishlist_by_user_id(user_id)
        return existing_wishlist is not None

    def create_wishlist(self, user_id: int) -> WishlistResponseDTO:
        logger.info(f"Creating wishlist for user_id={user_id}")
        existing_wishlist = self.repository.get_wishlist_by_user_id(user_id)
        if existing_wishlist:
            logger.warning(f"Wishlist already exists for user_id={user_id}")
            raise HTTPException(status_code=400, detail={"detail": "Người dùng đã có wishlist"})

        wishlist = self.repository.create_wishlist(user_id)
        try:
            self.repository.db.commit()
            logger.info(f"Wishlist created for user_id={user_id}, id={wishlist.id}")
        except Exception as e:
            logger.error(f"Failed to commit wishlist creation for user_id={user_id}: {str(e)}")
            self.repository.db.rollback()
            raise
        return WishlistResponseDTO(property_ids=[])

    def add_property_to_wishlist(self, user_id: int, property_id: int) -> WishlistResponseDTO:
        logger.info(f"Adding property_id={property_id} to wishlist for user_id={user_id}")
        try:
            wishlist = self.repository.get_wishlist_by_user_id(user_id)
            if not wishlist:
                logger.info(f"No wishlist found for user_id={user_id}, creating new one")
                wishlist = self.repository.create_wishlist(user_id)
                self.repository.db.flush()

            property = self.repository.get_property_by_id(property_id)
            if not property:
                logger.warning(f"Property_id={property_id} not found")
                raise HTTPException(status_code=404, detail={"detail": "Bất động sản không tồn tại"})

            # Double-check property existence to avoid race conditions
            if self.repository.check_property_in_wishlist(wishlist.id, property_id):
                logger.info(f"Property_id={property_id} already in wishlist_id={wishlist.id}")
                # Return current wishlist instead of raising an error
                property_ids = self.repository.get_wishlist_property_ids(user_id)
                return WishlistResponseDTO(property_ids=property_ids)

            logger.info(f"Adding property_id={property_id} to wishlist_id={wishlist.id}")
            self.repository.add_property_to_wishlist(wishlist.id, property_id)
            wishlist.updated_at = datetime.now()
            self.repository.db.commit()
            logger.info(f"Property_id={property_id} added to wishlist_id={wishlist.id}")

            property_ids = self.repository.get_wishlist_property_ids(user_id)
            logger.info(f"Returning property_ids={property_ids} for user_id={user_id}")
            return WishlistResponseDTO(property_ids=property_ids)
        except IntegrityError as e:
            logger.error(f"IntegrityError adding property_id={property_id} for user_id={user_id}: {str(e)}")
            self.repository.db.rollback()
            # Check again to handle race conditions
            if self.repository.check_property_in_wishlist(wishlist.id, property_id):
                logger.info(f"Property_id={property_id} already in wishlist_id={wishlist.id} after IntegrityError")
                property_ids = self.repository.get_wishlist_property_ids(user_id)
                return WishlistResponseDTO(property_ids=property_ids)
            raise HTTPException(status_code=400, detail={"detail": "Không thể thêm bất động sản: đã tồn tại hoặc lỗi cơ sở dữ liệu"})
        except Exception as e:
            logger.error(f"Unexpected error adding property_id={property_id} for user_id={user_id}: {str(e)}")
            self.repository.db.rollback()
            raise HTTPException(status_code=500, detail={"detail": f"Không thể thêm bất động sản: {str(e)}"})

    def remove_property_from_wishlist(self, user_id: int, property_id: int) -> WishlistResponseDTO:
        logger.info(f"Removing property_id={property_id} from wishlist for user_id={user_id}")
        try:
            wishlist = self.repository.get_wishlist_by_user_id(user_id)
            if not wishlist:
                logger.warning(f"Wishlist not found for user_id={user_id}")
                raise HTTPException(status_code=404, detail={"detail": "Wishlist không tồn tại"})

            if not self.repository.check_property_in_wishlist(wishlist.id, property_id):
                logger.warning(f"Property_id={property_id} not in wishlist_id={wishlist.id}")
                raise HTTPException(status_code=404, detail={"detail": "Bất động sản không có trong wishlist"})

            self.repository.remove_property_from_wishlist(wishlist.id, property_id)
            wishlist.updated_at = datetime.now()
            self.repository.db.commit()
            logger.info(f"Property_id={property_id} removed from wishlist_id={wishlist.id}")

            property_ids = self.repository.get_wishlist_property_ids(user_id)
            return WishlistResponseDTO(property_ids=property_ids)
        except Exception as e:
            logger.error(f"Error removing property_id={property_id} for user_id={user_id}: {str(e)}")
            self.repository.db.rollback()
            raise HTTPException(status_code=500, detail={"detail": f"Không thể xóa bất động sản: {str(e)}"})

    def get_wishlist_property_ids(self, user_id: int) -> WishlistResponseDTO:
        logger.info(f"Fetching wishlist property IDs for user_id={user_id}")
        try:
            wishlist = self.repository.get_wishlist_by_user_id(user_id)
            if not wishlist:
                logger.info(f"No wishlist found for user_id={user_id}")
                return WishlistResponseDTO(property_ids=[])

            property_ids = self.repository.get_wishlist_property_ids(user_id)
            logger.info(f"Found property_ids={property_ids} for user_id={user_id}")
            return WishlistResponseDTO(property_ids=property_ids)
        except Exception as e:
            logger.error(f"Error fetching wishlist for user_id={user_id}: {str(e)}")
            raise HTTPException(status_code=500, detail={"detail": f"Không thể lấy danh sách bất động sản: {str(e)}"})