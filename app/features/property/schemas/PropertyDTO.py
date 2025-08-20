from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID as UUIDType

from sqlalchemy import Enum

from .AmenityDTO import AmenityDTO
from .PropertyAmenityDTO import PropertyAmenityDTO
from .PropertyImageDTO import PropertyImageDTO

class CancellationPolicy(str, Enum):
    FLEXIBLE = "FLEXIBLE"
    MODERATE = "MODERATE"
    STRICT = "STRICT"
    SUPER_STRICT = "SUPER_STRICT"

class PropertyStatus(str, Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPENDED = "SUSPENDED"

class HostDTO(BaseModel):
    host_id: int
    host_rating_average: Optional[float] = 4.5

    class Config:
        from_attributes = True

class PropertyCreateDTO(BaseModel):
    host_id: int
    title: str
    description: Optional[str] = None
    property_type: str
    category: str
    max_guests: int
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    address_line1: Optional[str] = None
    city: str
    state: Optional[str] = None
    country: str
    postal_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    base_price: float
    cleaning_fee: Optional[float] = 0
    cancellation_policy: str
    instant_book: bool = False
    minimum_stay: int = 1
    home_tier: Optional[int] = None
    is_guest_favorite: Optional[bool] = None
    language: str = "en"
    status: str = "DRAFT"
    amenities: Optional[List[UUIDType]] = None
    images: Optional[List[PropertyImageDTO]] = None

    class Config:
        from_attributes = True

class PropertyUpdateDTO(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    property_type: Optional[str] = None
    category: Optional[str] = None
    max_guests: Optional[int] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    address_line1: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    base_price: Optional[float] = None
    cleaning_fee: Optional[float] = None
    cancellation_policy: Optional[str] = None
    instant_book: Optional[bool] = None
    minimum_stay: Optional[int] = None
    home_tier: Optional[int] = None
    is_guest_favorite: Optional[bool] = None
    language: Optional[str] = None
    status: Optional[str] = None
    amenities: Optional[List[UUIDType]] = None
    images: Optional[List[PropertyImageDTO]] = None
    deletedImageIds: Optional[List[UUIDType]] = None
    class Config:
        from_attributes = True

class PropertyResponseDTO(BaseModel):
    id: int
    host_id: int
    title: str
    description: Optional[str] = None
    property_type: str
    category: str
    max_guests: int
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    address_line1: Optional[str] = None
    city: str
    state: Optional[str] = None
    country: str
    postal_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    base_price: float
    cleaning_fee: Optional[float] = None
    cancellation_policy: str
    instant_book: bool
    minimum_stay: int
    home_tier: Optional[int] = None
    is_guest_favorite: Optional[bool] = None
    language: str
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    amenities: Optional[List[AmenityDTO]] = None
    images: Optional[List[PropertyImageDTO]] = None
    host: Optional[HostDTO] = None
    class Config:
        from_attributes = True