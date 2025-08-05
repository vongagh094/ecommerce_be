"""Property service implementation."""

from typing import List, Tuple
from decimal import Decimal

from ....shared.models import Property, Amenity
from ....shared.schemas.pagination import PaginationInfo
from ..repository import PropertyRepository
from ..schemas.search import PropertySearchParams, PropertyFilterParams
from ..schemas.response import (
    PropertySearchResponse, 
    PropertyDetailsResponse,
    ReviewSummaryResponse,
    AvailabilityCalendarResponse
)


class PropertyService:
    """Service for property business logic."""
    
    def __init__(self, repository: PropertyRepository):
        self.repository = repository
    
    async def search_properties(self, params: PropertySearchParams) -> PropertySearchResponse:
        """Search properties with basic filters."""
        
        properties, total = await self.repository.search_properties(params)
        
        # Convert to property cards
        property_cards = []
        for property in properties:
            # Calculate rating from reviews
            rating = await self._calculate_property_rating(property)
            rating = {
                "average": float(rating.get("average")),
                "count": rating.get("count")
            }
            print(property.id)
            # Format property card
            property_card = {
                "id": str(property.id),
                "title": property.title,
                "images": [self._format_image(img) for img in property.images],
                "base_price": property.base_price,
                "location": {
                    "city": property.city,
                    "state": property.state,
                    "country": property.country
                },
                "rating": rating,
                "property_type": property.property_type,
                "max_guests": property.max_guests,
                "is_guest_favorite": property.is_guest_favorite,
                "host": self._format_host(property.host)
            }
            property_cards.append(property_card)
        
        # Create pagination info
        pagination = PaginationInfo(
            page=params.page,
            limit=params.limit,
            total=total,
            has_more=(params.page * params.limit) < total
        )
        
        return PropertySearchResponse(
            properties=property_cards,
            pagination=pagination
        )
    
    async def filter_properties(self, params: PropertyFilterParams) -> PropertySearchResponse:
        """Filter properties with advanced criteria."""
        
        properties, total = await self.repository.filter_properties(params)
        
        # Convert to property cards (same logic as search)
        property_cards = []
        for property in properties:
            rating = await self._calculate_property_rating(property)
            
            property_card = {
                "id": property.id,
                "title": property.title,
                "images": [self._format_image(img) for img in property.images],
                "base_price": property.base_price,
                "location": {
                    "city": property.city,
                    "state": property.state,
                    "country": property.country
                },
                "rating": rating,
                "property_type": property.property_type,
                "max_guests": property.max_guests,
                "is_guest_favorite": property.is_guest_favorite,
                "host": self._format_host(property.host)
            }
            property_cards.append(property_card)
        
        pagination = PaginationInfo(
            page=params.page,
            limit=params.limit,
            total=total,
            has_more=(params.page * params.limit) < total
        )
        
        return PropertySearchResponse(
            properties=property_cards,
            pagination=pagination
        )
    
    async def get_properties_by_category(
        self, 
        category: str, 
        params: PropertySearchParams
    ) -> PropertySearchResponse:
        """Get properties by category."""
        
        properties, total = await self.repository.get_properties_by_category(category, params)
        
        # Convert to property cards (same logic as search)
        property_cards = []
        for property in properties:
            rating = await self._calculate_property_rating(property)
            
            property_card = {
                "id": property.id,
                "title": property.title,
                "images": [self._format_image(img) for img in property.images],
                "base_price": property.base_price,
                "location": {
                    "city": property.city,
                    "state": property.state,
                    "country": property.country
                },
                "rating": rating,
                "property_type": property.property_type,
                "max_guests": property.max_guests,
                "is_guest_favorite": property.is_guest_favorite,
                "host": self._format_host(property.host)
            }
            property_cards.append(property_card)
        
        pagination = PaginationInfo(
            page=params.page,
            limit=params.limit,
            total=total,
            has_more=(params.page * params.limit) < total
        )
        
        return PropertySearchResponse(
            properties=property_cards,
            pagination=pagination
        )
    
    async def get_property_details(self, property_id: int) -> PropertyDetailsResponse:
        """Get detailed property information."""
        
        property = await self.repository.get_property_by_id(property_id)
        
        # Format detailed response
        return PropertyDetailsResponse(
            id=property.id,
            title=property.title,
            description=property.description,
            property_type=property.property_type,
            category=property.category,
            max_guests=property.max_guests,
            bedrooms=property.bedrooms,
            bathrooms=property.bathrooms,
            location={
                "address_line1": property.address_line1,
                "city": property.city,
                "state": property.state,
                "country": property.country,
                "postal_code": property.postal_code,
                "latitude": float(property.latitude) if property.latitude else None,
                "longitude": float(property.longitude) if property.longitude else None
            },
            pricing={
                "base_price": float(property.base_price),
                "cleaning_fee": float(property.cleaning_fee),
                "service_fee": self._calculate_service_fee(property.base_price)
            },
            policies={
                "cancellation_policy": property.cancellation_policy,
                "instant_book": property.instant_book,
                "minimum_stay": property.minimum_stay,
                "check_in_time": "3:00 PM",  # Default values
                "check_out_time": "11:00 AM"
            },
            images=[self._format_image(img) for img in property.images],
            amenities=[self._format_amenity(amenity) for amenity in property.amenities],
            highlights=[self._format_highlight(highlight) for highlight in property.highlights],
            house_rules=[self._format_house_rule(rule) for rule in property.house_rules],
            location_descriptions=[
                self._format_location_description(desc) 
                for desc in property.location_descriptions
            ],
            host=self._format_host_profile(property.host),
            reviews=await self._format_review_summary(property),
            availability_calendar=await self._get_availability_calendar(property.id),
            active_auctions=[self._format_auction(auction) for auction in property.auctions]
        )
    
    async def get_categories(self) -> List[dict]:
        """Get list of available property categories."""
        return await self.repository.get_available_categories()
    
    async def get_amenities(self) -> List[Amenity]:
        """Get list of available amenities."""
        return await self.repository.get_available_amenities()
    
    async def get_location_suggestions(self, query: str, limit: int = 10) -> List[dict]:
        """Get location suggestions for autocomplete."""
        return await self.repository.get_location_suggestions(query, limit)
    
    # Helper methods
    
    async def _calculate_property_rating(self, property: Property) -> dict:
        """Calculate property rating from reviews."""
        # TODO: Implement actual rating calculation from reviews
        return {
            "average": 4.5,
            "count": 123
        }
    
    def _format_image(self, image) -> dict:
        """Format property image."""
        return {
            "id": str(image.id),
            "image_url": image.image_url,
            "alt_text": image.alt_text,
            "is_primary": image.is_primary,
            "display_order": image.display_order
        }
    
    def _format_host(self, host) -> dict:
        """Format host information for property card.

        HostProfile schema (shared.schemas.user.HostProfile) requires:
        id, full_name, is_super_host, created_at (required) and several optional
        fields.  Validation was failing because *created_at* was omitted.  We
        now supply all mandatory fields and include the optional ones when
        available.
        """
        return {
            "id": host.id,
            "full_name": host.full_name,
            "profile_image_url": getattr(host, "profile_image_url", None),
            "is_super_host": getattr(host, "is_super_host", False),
            "host_about": getattr(host, "host_about", None),
            "host_review_count": getattr(host, "host_review_count", None),
            "host_rating_average": float(host.host_rating_average) if getattr(host, "host_rating_average", None) is not None else None,
            "created_at": host.created_at if hasattr(host, "created_at") else None,
        }
    
    def _format_host_profile(self, host) -> dict:
        """Format detailed host profile."""
        return {
            "id": host.id,
            "full_name": host.full_name,
            "profile_image_url": host.profile_image_url,
            "is_super_host": host.is_super_host,
            "host_about": host.host_about,
            "host_review_count": host.host_review_count or 0,
            "host_rating_average": float(host.host_rating_average) if host.host_rating_average else 0.0,
            "created_at": host.created_at.isoformat()
        }
    
    def _format_amenity(self, amenity) -> dict:
        """Format amenity information."""
        return {
            "id": str(amenity.id),
            "name": amenity.name,
            "category": amenity.category
        }
    
    def _format_highlight(self, highlight) -> dict:
        """Format property highlight."""
        return {
            "id": highlight.id,
            "title": highlight.title,
            "subtitle": highlight.subtitle,
            "icon": highlight.icon
        }
    
    def _format_house_rule(self, rule) -> dict:
        """Format house rule."""
        return {
            "id": rule.id,
            "rule_type": rule.rule_type,
            "title": rule.title,
            "description": rule.description
        }
    
    def _format_location_description(self, desc) -> dict:
        """Format location description."""
        return {
            "id": desc.id,
            "description_type": desc.description_type,
            "title": desc.title,
            "description": desc.description
        }
    
    def _format_auction(self, auction) -> dict:
        """Format auction information."""
        return {
            "id": str(auction.id),
            "start_date": auction.start_date.isoformat(),
            "end_date": auction.end_date.isoformat(),
            "auction_start_time": auction.auction_start_time.isoformat(),
            "auction_end_time": auction.auction_end_time.isoformat(),
            "starting_price": float(auction.starting_price),
            "current_highest_bid": float(auction.current_highest_bid) if auction.current_highest_bid else None,
            "minimum_bid": float(auction.minimum_bid),
            "total_bids": auction.total_bids,
            "status": auction.status
        }
    
    def _calculate_service_fee(self, base_price: Decimal) -> float:
        """Calculate service fee (typically 3-5% of base price)."""
        return float(base_price * Decimal("0.03"))
    
    async def _format_review_summary(self, property: Property) -> ReviewSummaryResponse:
        """Format review summary."""
        # TODO: Implement actual review aggregation
        return ReviewSummaryResponse(
            total_reviews=0,
            average_rating=Decimal("0.0"),
            rating_breakdown={
                "accuracy": 0.0,
                "cleanliness": 0.0,
                "communication": 0.0,
                "location": 0.0,
                "value": 0.0,
                "checking": 0.0
            },
            recent_reviews=[]
        )
    
    async def _get_availability_calendar(self, property_id: int) -> AvailabilityCalendarResponse:
        """Get availability calendar for property."""
        # TODO: Implement actual calendar availability
        return AvailabilityCalendarResponse(
            available_dates=[],
            blocked_dates=[],
            price_calendar=[]
        )