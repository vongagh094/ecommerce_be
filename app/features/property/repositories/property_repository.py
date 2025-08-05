from typing import List, Optional, Dict
from sqlalchemy.orm import Session, selectinload
from app.features.property.schemas.PropertyDTO import PropertyCreateDTO, PropertyResponseDTO, HostDTO
from app.db.models.property import Property
from app.db.models.user import User
from app.db.models.property_type import PropertyType
from app.db.models.property_category import PropertyCategory
from app.features.property.repositories.property_amenity_repository import PropertyAmenityRepository
from app.features.property.repositories.property_image_repository import PropertyImageRepository
from app.features.property.schemas.AmenityDTO import AmenityDTO
from app.features.property.schemas.PropertyImageDTO import PropertyImageDTO

class PropertyRepository:
    def __init__(self, db: Session, property_amenity_repository: PropertyAmenityRepository, property_image_repository: PropertyImageRepository):
        self.db = db
        self.property_amenity_repository = property_amenity_repository
        self.property_image_repository = property_image_repository

    def create(self, data: PropertyCreateDTO) -> Property:
        """Create a new property."""
        if not self.db.query(PropertyType).filter(PropertyType.name == data.property_type).first():
            raise ValueError(f"Invalid property_type: {data.property_type}")
        if not self.db.query(PropertyCategory).filter(PropertyCategory.name == data.category).first():
            raise ValueError(f"Invalid category: {data.category}")

        property_data = data.model_dump(exclude={"amenities", "images"})
        property = Property(**property_data)
        self.db.add(property)
        self.db.commit()
        self.db.refresh(property)
        return property

    def get_by_id(self, property_id: int) -> Optional[PropertyResponseDTO]:
        """Get a property by ID."""
        property = self.db.query(Property).options(
            selectinload(Property.host)
        ).filter(Property.id == property_id).first()
        if not property:
            return None
        return self._to_property_response_dto(property)

    def get_all(self, limit: int, offset: int) -> List[PropertyResponseDTO]:
        """Get all properties with pagination."""
        properties = self.db.query(Property).options(
            selectinload(Property.host)
        ).limit(limit).offset(offset).all()
        return [self._to_property_response_dto(prop) for prop in properties]

    def get_by_host_id(self, host_id: int, limit: int, offset: int) -> List[PropertyResponseDTO]:
        """Get properties by host ID with pagination."""
        properties = self.db.query(Property).options(
            selectinload(Property.host)
        ).filter(Property.host_id == host_id).limit(limit).offset(offset).all()
        return [self._to_property_response_dto(prop) for prop in properties]

    def update(self, property_id: int, data: Dict) -> Optional[Property]:
        """Update a property."""
        if "property_type" in data and not self.db.query(PropertyType).filter(PropertyType.name == data["property_type"]).first():
            raise ValueError(f"Invalid property_type: {data['property_type']}")
        if "category" in data and not self.db.query(PropertyCategory).filter(PropertyCategory.name == data["category"]).first():
            raise ValueError(f"Invalid category: {data['category']}")

        property = self.db.query(Property).filter(Property.id == property_id).first()
        if property:
            for key, value in data.items():
                if value is not None:
                    setattr(property, key, value)
            self.db.commit()
            self.db.refresh(property)
            return property
        return None

    def delete(self, property_id: int) -> bool:
        """Delete a property."""
        property = self.db.query(Property).filter(Property.id == property_id).first()
        if property:
            self.db.delete(property)
            self.db.commit()
            return True
        return False

    def _to_property_response_dto(self, property: Property) -> PropertyResponseDTO:
        """Helper method to convert Property to PropertyResponseDTO with related data."""
        amenities = self.property_amenity_repository.get_by_property_id(property.id) or []
        images = self.property_image_repository.get_by_property_id(property.id) or []
        host_dto = None
        if property.host:
            host_dto = HostDTO(
                host_id=property.host.id,
                host_rating_average=getattr(property.host, 'host_rating_average', 4.5)
            )

        return PropertyResponseDTO(
            id=property.id,
            host_id=property.host_id,
            title=property.title,
            description=property.description,
            property_type=property.property_type,
            category=property.category,
            max_guests=property.max_guests,
            bedrooms=property.bedrooms,
            bathrooms=property.bathrooms,
            address_line1=property.address_line1,
            city=property.city,
            state=property.state,
            country=property.country,
            postal_code=property.postal_code,
            latitude=property.latitude,
            longitude=property.longitude,
            base_price=property.base_price,
            cleaning_fee=property.cleaning_fee,
            cancellation_policy=property.cancellation_policy,
            instant_book=property.instant_book,
            minimum_stay=property.minimum_stay,
            home_tier=property.home_tier,
            is_guest_favorite=property.is_guest_favorite,
            language=property.language,
            status=property.status,
            created_at=property.created_at,
            updated_at=property.updated_at,
            amenities=amenities,
            images=images,
            host=host_dto
        )