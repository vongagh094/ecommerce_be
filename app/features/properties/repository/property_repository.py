"""Property repository implementation using SQLAlchemy."""

from datetime import date
from typing import List, Optional, Tuple, Dict
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func, select, Table, MetaData

from app.db.models.property import Property
from app.db.models.property_image import PropertyImage
from app.db.models.property_amenity import PropertyAmenity
from app.db.models.amenity import Amenity
from app.db.models.property_extras import PropertyHighlight
from app.db.models.calendar_availability import CalendarAvailability
from ....shared.exceptions import NotFoundError
from ..schemas.search import PropertySearchParams, PropertyFilterParams


class PropertyRepository:
	"""Repository for property data access."""
	
	def __init__(self, db: Session):
		self.db = db
	
	def _apply_location_filter(self, query, location: Optional[str]):
		if not location:
			return query
		# Tokenize by comma and whitespace, apply ILIKE per token across fields
		tokens = [tok.strip() for tok in location.split(",") if tok.strip()]
		if not tokens:
			return query
		per_token_ors = []
		for tok in tokens:
			pattern = f"%{tok}%"
			per_token_ors.append(
				or_(
					Property.city.ilike(pattern),
					Property.state.ilike(pattern),
					Property.country.ilike(pattern),
					Property.address_line1.ilike(pattern)
				)
			)
		# At least one token matches any field
		return query.filter(or_(*per_token_ors))
	
	def _apply_categories_filter(self, query, categories: Optional[List[str]]):
		if not categories:
			return query
		icons = [f"SYSTEM_{c}" for c in categories]
		ph = PropertyHighlight
		sub = (
			self.db.query(ph.property_id)
			.filter(ph.icon.in_(icons))
			.group_by(ph.property_id)
			.having(func.count(func.distinct(ph.icon)) == len(icons))
		).subquery()
		return query.join(sub, sub.c.property_id == Property.id)
	
	def _apply_availability_filter(self, query, check_in: Optional[date], check_out: Optional[date]):
		if not check_in or not check_out:
			return query
		ca = CalendarAvailability
		sub = (
			self.db.query(ca.property_id)
			.filter(
				and_(
					ca.date >= check_in,
					ca.date < check_out,
					ca.is_available.is_(True)
				)
			)
			.group_by(ca.property_id)
			.having(func.count() >= 2)
		).subquery()
		return query.join(sub, sub.c.property_id == Property.id)
	
	async def search_properties(
		self, 
		params: PropertySearchParams
	) -> Tuple[List[Property], int]:
		"""Search properties with basic filters."""
		
		query = self.db.query(Property).filter(Property.status == "ACTIVE")
		
		# Apply location, guests, availability filters
		query = self._apply_location_filter(query, params.location)
		if params.guests:
			query = query.filter(Property.max_guests >= params.guests)
		query = self._apply_availability_filter(query, params.check_in, params.check_out)
		
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
		query = self._apply_location_filter(query, params.location)
		if params.guests:
			query = query.filter(Property.max_guests >= params.guests)
		
		# Categories via PropertyHighlight icons (AND semantics)
		query = self._apply_categories_filter(query, params.categories)
		
		# Availability window (>= 2 days available)
		query = self._apply_availability_filter(query, params.check_in, params.check_out)
		
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
		query = self._apply_location_filter(query, params.location)
		if params.guests:
			query = query.filter(Property.max_guests >= params.guests)
		query = self._apply_availability_filter(query, params.check_in, params.check_out)
		
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
	
	async def get_available_categories(self) -> List[str]:
		"""Get list of available property categories with counts."""
		
		query = self.db.query(PropertyHighlight.icon).distinct()
		icons = query.all()
		return [icon.icon.replace("SYSTEM_", "") for icon in icons]
	
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

	async def get_property_ratings(self, property_ids: List[int]) -> Dict[int, Dict[str, float]]:
		"""Aggregate reviews to compute average rating and count per property.
		Returns mapping: property_id -> {"average": float, "count": int}
		"""
		if not property_ids:
			return {}
		md = MetaData()
		reviews = Table("reviews", md, autoload_with=self.db.bind)
		stmt = (
			select(
				reviews.c.property_id,
				func.count().label("count"),
				func.avg(reviews.c.rating).label("average")
			)
			.where(and_(reviews.c.property_id.in_(property_ids), reviews.c.is_visible == True))
			.group_by(reviews.c.property_id)
		)
		rows = self.db.execute(stmt).all()
		result: Dict[int, Dict[str, float]] = {}
		for pid, count, avg in rows:
			result[int(pid)] = {"average": float(avg) if avg is not None else 0.0, "count": int(count)}
		return result
	
	async def get_property_by_id(self, property_id: int) -> Property:
		"""Get property by ID."""
		return self.db.query(Property).filter(Property.id == property_id).first()   