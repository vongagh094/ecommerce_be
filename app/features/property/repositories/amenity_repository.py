from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.models.amenity import Amenity
from uuid import UUID as UUIDType

class AmenityRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, amenity_id: UUIDType) -> Optional[Amenity]:
        """Get an amenity by ID."""
        return self.db.query(Amenity).filter(Amenity.id == amenity_id).first()

    def get_all(self) -> List[Amenity]:
        """Get all amenities."""
        return self.db.query(Amenity).all()