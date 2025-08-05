from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.features.wishlist.schemas.WishlistDTO import WishlistResponseDTO
from app.features.wishlist.services.wishlist_service import WishlistService
from app.db.sessions.session import get_db_session

router = APIRouter()

def get_wishlist_service(db: Session = Depends(get_db_session)) -> WishlistService:
    return WishlistService(db)

@router.post("/create", response_model=WishlistResponseDTO)
def create_user_wishlist(user_id: int, service: WishlistService = Depends(get_wishlist_service)):
    try:
        return service.create_wishlist(user_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail={"detail": f"Không thể tạo wishlist: {str(e)}"})

@router.post("/{user_id}/add-property", response_model=WishlistResponseDTO)
def add_property(user_id: int, property_id: int, service: WishlistService = Depends(get_wishlist_service)):
    try:
        return service.add_property_to_wishlist(user_id, property_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail={"detail": f"Không thể thêm bất động sản vào wishlist: {str(e)}"})

@router.delete("/{user_id}/remove-property/{property_id}", response_model=WishlistResponseDTO)
def remove_property(user_id: int, property_id: int, service: WishlistService = Depends(get_wishlist_service)):
    try:
        return service.remove_property_from_wishlist(user_id, property_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail={"detail": f"Không thể xóa bất động sản khỏi wishlist: {str(e)}"})

@router.get("/{user_id}/properties", response_model=WishlistResponseDTO)
def get_wishlist_properties(user_id: int, service: WishlistService = Depends(get_wishlist_service)):
    try:
        return service.get_wishlist_property_ids(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail={"detail": f"Không thể lấy danh sách bất động sản trong wishlist: {str(e)}"})