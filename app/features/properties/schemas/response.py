"""Property response schemas."""

from datetime import datetime, date
from decimal import Decimal
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel

from ....shared.schemas.property import PropertyCard
from ....shared.schemas.pagination import PaginationInfo


class PropertySearchResponse(BaseModel):
    """Property search response."""
    
    properties: List[PropertyCard]
    pagination: PaginationInfo
    status_code: int = 200


class AmenityResponse(BaseModel):
    """Amenity response schema."""
    
    id: UUID
    name: str
    category: str
    
    class Config:
        from_attributes = True


class PropertyHighlightResponse(BaseModel):
    """Property highlight response schema."""
    
    id: int
    title: Optional[str] = None
    subtitle: Optional[str] = None
    icon: Optional[str] = None
    
    class Config:
        from_attributes = True


class HouseRuleResponse(BaseModel):
    """House rule response schema."""
    
    id: int
    rule_type: str
    title: Optional[str] = None
    description: Optional[str] = None
    
    class Config:
        from_attributes = True


class LocationDescriptionResponse(BaseModel):
    """Location description response schema."""
    
    id: int
    description_type: str
    title: Optional[str] = None
    description: Optional[str] = None
    
    class Config:
        from_attributes = True


class ReviewResponse(BaseModel):
    """Review response schema."""
    
    id: UUID
    reviewer: dict
    rating: Decimal
    review_text: Optional[str] = None
    created_at: datetime
    response_text: Optional[str] = None
    
    class Config:
        from_attributes = True


class ReviewSummaryResponse(BaseModel):
    """Review summary response schema."""
    
    total_reviews: int
    average_rating: Decimal
    rating_breakdown: dict
    recent_reviews: List[ReviewResponse]


class AvailabilityCalendarResponse(BaseModel):
    """Availability calendar response schema."""
    
    available_dates: List[str]
    blocked_dates: List[str]
    price_calendar: List[dict]


class AuctionInfoResponse(BaseModel):
    """Auction info response schema."""
    
    id: UUID
    start_date: date
    end_date: date
    auction_start_time: datetime
    auction_end_time: datetime
    starting_price: Decimal
    current_highest_bid: Optional[Decimal] = None
    minimum_bid: Decimal
    total_bids: int
    status: str
    
    class Config:
        from_attributes = True


class PropertyDetailsResponse(BaseModel):
    """Property details response schema."""
    
    id: int
    title: str
    description: Optional[str] = None
    property_type: str
    category: str
    max_guests: int
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    location: dict
    pricing: dict
    policies: dict
    images: List[dict]
    amenities: List[AmenityResponse]
    highlights: List[PropertyHighlightResponse]
    house_rules: List[HouseRuleResponse]
    location_descriptions: List[LocationDescriptionResponse]
    host: dict
    reviews: ReviewSummaryResponse
    availability_calendar: AvailabilityCalendarResponse
    active_auctions: List[AuctionInfoResponse]
    
    class Config:
        from_attributes = True