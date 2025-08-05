from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from app.db.models.wishlist import Wishlist
from app.db.models.wishlist_property import WishlistProperty
from app.db.models.property import Property
from datetime import datetime

class WishlistRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_wishlist_by_user_id(self, user_id: int) -> Wishlist | None:
        result = self.db.execute(
            select(Wishlist).filter(Wishlist.user_id == user_id)
        )
        return result.scalar_one_or_none()

    def create_wishlist(self, user_id: int) -> Wishlist:
        wishlist = Wishlist(
            user_id=user_id,
            is_private=False,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.db.add(wishlist)
        self.db.flush()
        return wishlist

    def get_property_by_id(self, property_id: int) -> Property | None:
        result = self.db.execute(
            select(Property).filter(Property.id == property_id)
        )
        return result.scalar_one_or_none()

    def check_property_in_wishlist(self, wishlist_id: int, property_id: int) -> bool:
        result = self.db.execute(
            select(WishlistProperty)
            .filter(WishlistProperty.wishlist_id == wishlist_id, WishlistProperty.property_id == property_id)
        )
        return result.scalar_one_or_none() is not None

    def add_property_to_wishlist(self, wishlist_id: int, property_id: int) -> WishlistProperty:
        wishlist_property = WishlistProperty(
            wishlist_id=wishlist_id,
            property_id=property_id,
            added_at=datetime.now()
        )
        self.db.add(wishlist_property)
        self.db.flush()
        return wishlist_property

    def remove_property_from_wishlist(self, wishlist_id: int, property_id: int) -> None:
        self.db.execute(
            delete(WishlistProperty)
            .where(WishlistProperty.wishlist_id == wishlist_id, WishlistProperty.property_id == property_id)
        )

    def get_wishlist_property_ids(self, user_id: int) -> list[int]:
        result = self.db.execute(
            select(WishlistProperty.property_id)
            .join(Wishlist, WishlistProperty.wishlist_id == Wishlist.id)
            .filter(Wishlist.user_id == user_id)
        )
        property_ids = [row for row in result.scalars().all()]
        return property_ids