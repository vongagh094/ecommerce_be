"""Property repository implementation using SQLAlchemy."""

from datetime import date
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func

from app.db.models.property import Property
from app.db.models.property_image import PropertyImage
from app.db.models.property_amenity import PropertyAmenity
from app.db.models.amenity import Amenity
from app.db.models.user import User
from ....shared.exceptions import NotFoundError
from ..schemas.search import PropertySearchParams, PropertyFilterParams


class PropertyRepository:
    """Repository for property data access."""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def search_properties(
        self, 
        params: PropertySearchParams
    ) -> Tuple[List[Property], int]:
        """Search properties with basic filters."""
        
        query = self.db.query(Property).filter(Property.status == "ACTIVE")
        
        # Apply location filter
        if params.location:
            location_filter = or_(
                Property.city.ilike(f"%{params.location}%"),
                Property.state.ilike(f"%{params.location}%"),
                Property.country.ilike(f"%{params.location}%"),
                Property.address_line1.ilike(f"%{params.location}%")
            )
            query = query.filter(location_filter)
        
        # Apply guest capacity filter
        if params.guests:
            query = query.filter(Property.max_guests >= params.guests)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        offset = (params.page - 1) * params.limit
        query = query.offset(offset).limit(params.limit)
        
        # Execute query with eager loading
        query = query.options(
            joinedload(Property.images),
            joinedload(Property.host)
        )
        
        properties = query.all()
        return properties, total
    
    async def filter_properties(
        self, 
        params: PropertyFilterParams
    ) -> Tuple[List[Property], int]:
        """Filter properties with advanced criteria."""
        
        query = self.db.query(Property).filter(Property.status == "ACTIVE")
        
        # Apply basic search filters
        if params.location:
            location_filter = or_(
                Property.city.ilike(f"%{params.location}%"),
                Property.state.ilike(f"%{params.location}%"),
                Property.country.ilike(f"%{params.location}%"),
                Property.address_line1.ilike(f"%{params.location}%")
            )
            query = query.filter(location_filter)
        
        if params.guests:
            query = query.filter(Property.max_guests >= params.guests)
        
        # Apply price filters
        if params.min_price is not None:
            query = query.filter(Property.base_price >= params.min_price)
        
        if params.max_price is not None:
            query = query.filter(Property.base_price <= params.max_price)
        
        # Apply property type filter
        if params.property_types:
            query = query.filter(Property.property_type.in_(params.property_types))
        
        # Apply category filter
        if params.categories:
            query = query.filter(Property.category.in_(params.categories))
        
        # Apply other filters
        if params.instant_book is not None:
            query = query.filter(Property.instant_book == params.instant_book)
        
        if params.bedrooms is not None:
            query = query.filter(Property.bedrooms >= params.bedrooms)
        
        if params.bathrooms is not None:
            query = query.filter(Property.bathrooms >= params.bathrooms)
        
        if params.cancellation_policy:
            query = query.filter(Property.cancellation_policy.in_(params.cancellation_policy))
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        offset = (params.page - 1) * params.limit
        query = query.offset(offset).limit(params.limit)
        
        # Execute query with eager loading
        query = query.options(
            joinedload(Property.images),
            joinedload(Property.host)
        )
        
        properties = query.all()
        return properties, total
    
    async def get_properties_by_category(
        self, 
        category: str,
        params: PropertySearchParams
    ) -> Tuple[List[Property], int]:
        """Get properties by category."""
        
        query = self.db.query(Property).filter(
            and_(
                Property.status == "ACTIVE",
                Property.category == category
            )
        )
        
        # Apply optional filters
        if params.location:
            location_filter = or_(
                Property.city.ilike(f"%{params.location}%"),
                Property.state.ilike(f"%{params.location}%"),
                Property.country.ilike(f"%{params.location}%")
            )
            query = query.filter(location_filter)
        
        if params.guests:
            query = query.filter(Property.max_guests >= params.guests)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        offset = (params.page - 1) * params.limit
        query = query.offset(offset).limit(params.limit)
        
        # Execute query with eager loading
        query = query.options(
            joinedload(Property.images),
            joinedload(Property.host)
        )
        
        properties = query.all()
        
        return properties, total
    
    async def get_property_by_id(self, property_id: int) -> Property:
        """Get property by ID with all related data."""
        
        property = self.db.query(Property).options(
            joinedload(Property.images),
            joinedload(Property.amenities),
            joinedload(Property.highlights),
            joinedload(Property.house_rules),
            joinedload(Property.location_descriptions),
            joinedload(Property.host),
            joinedload(Property.auctions),
        ).filter(Property.id == property_id).first()
        
        if not property:
            raise NotFoundError("Property", str(property_id))
        
        return property
    
    async def get_available_categories(self) -> List[dict]:
        """Get list of available property categories with counts."""
        
        results = self.db.query(
            Property.category,
            func.count(Property.id).label("property_count")
        ).filter(
            Property.status == "ACTIVE"
        ).group_by(Property.category).all()
        
        categories = []
        for category, count in results:
            categories.append({
                "name": category,
                "display_name": category.replace("_", " ").title(),
                "property_count": count
            })
        
        return categories
    
    async def get_available_amenities(self) -> List[Amenity]:
        """Get list of available amenities."""
        
        return self.db.query(Amenity).order_by(Amenity.category, Amenity.name).all()
    
    async def get_location_suggestions(self, query_text: str, limit: int = 10) -> List[dict]:
        """Get location suggestions for autocomplete."""
        
        # Search in cities, states, and countries
        results = self.db.query(
            Property.city,
            Property.state, 
            Property.country,
            func.count(Property.id).label("property_count")
        ).filter(
            and_(
                Property.status == "ACTIVE",
                or_(
                    Property.city.ilike(f"%{query_text}%"),
                    Property.state.ilike(f"%{query_text}%"),
                    Property.country.ilike(f"%{query_text}%")
                )
            )
        ).group_by(
            Property.city, Property.state, Property.country
        ).limit(limit).all()
        
        suggestions = []
        for city, state, country, count in results:
            display_name = f"{city}, {state}, {country}"
            suggestions.append({
                "display_name": display_name,
                "city": city,
                "state": state,
                "country": country,
                "property_count": count
            })
        
        return suggestions