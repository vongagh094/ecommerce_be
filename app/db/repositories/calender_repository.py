import uuid
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import date, datetime
from sqlalchemy import and_
from app.db.models.calendar_availability import CalendarAvailability
import logging
logger = logging.getLogger(__name__)

class CalendarRepository:
    """Repository cho calendar data access với direct table functions"""

    def __init__(self, db: Session):
        self.db = db
    def get_calendar_data(
            self,
            property_id: int,
            auction_id: str,
            year: int,
            month: int
    ) -> List[Dict[str, Any]]:
        """
        Main method: Get calendar data sử dụng optimized direct function
        """
        try:
            query = text("SELECT * FROM get_calendar_optimized_direct(:property_id, :auction_id,:year, :month)")

            result = self.db.execute(query, {
                'property_id': property_id,
                'auction_id': auction_id,
                'year': year,
                'month': month
            })
            rows = result.fetchall()

            # Convert to clean dictionaries
            calendar_data = []
            for row in rows:
                calendar_data.append({
                    'date': row.date,
                    'highest_bid': float(row.highest_bid),
                    'active_bids': int(row.active_bids),
                    'minimum_to_win': float(row.minimum_to_win),
                    'base_price': float(row.base_price),
                    'demand_level': row.demand_level,
                    'success_rate': int(row.success_rate),
                    'is_available': bool(row.is_available),
                    'is_booked': bool(row.is_booked)
                })

            return calendar_data

        except Exception as e:
            logger.error(f"Error getting calendar data for property {property_id}: {e}")
            raise

    def validate_property_exists(self, property_id: int) -> bool:
        """Check if the property exists"""
        try:
            query = text("SELECT 1 FROM properties WHERE id = :property_id")
            result = self.db.execute(query, {"property_id": property_id})
            return result.fetchone() is not None
        except Exception as e:
            print(f"Error validating property exists: {e}")
            return False

    async def get_property_base_price(self, property_id: int) -> float:
        """Get base price for property"""
        try:
            query = text("SELECT * FROM properties WHERE id = :property_id")
            result = await self.db.execute(query, {"property_id": property_id})
            print(result.fetchone())
            return result.fetchone() is not None
        except Exception as e:
            print(f"Error getting property base price: {e}")
            return 0.0

    def get_calendar_availability_for_date_range(self, property_id: int, start_date: date, end_date: date) -> list[
        type[CalendarAvailability]]:
        """Get calendar availability entries for date range"""
        return self.db.query(CalendarAvailability).filter(
            and_(
                CalendarAvailability.property_id == property_id,
                CalendarAvailability.date >= start_date,
                CalendarAvailability.date <= end_date
            )
        ).all()

    def get_calendar_entry_for_date(self, property_id: int, date: date, auction_id: str) -> Optional[Dict]:
        """Get calendar entry for specific date and auction"""
        entry = self.db.query(CalendarAvailability).filter(
            and_(
                CalendarAvailability.property_id == property_id,
                CalendarAvailability.date == date,
                CalendarAvailability.auction_id == auction_id
            )
        ).first()

        if entry:
            return {
                'date': entry.date,
                'price_amount': entry.price_amount,
                'bid_id': entry.bid_id,
                'is_available': entry.is_available,
                'updated_at': entry.updated_at
            }
        return None

    def create_calendar_entry(self, property_id: int, date: date, bid_id: str,
                              price_amount: int, is_available: bool = True) -> bool:
        """Create new calendar availability entry"""
        try:
            new_entry = CalendarAvailability(
                property_id=property_id,
                date=date,
                bid_id=bid_id,
                price_amount=price_amount,
                is_available=is_available,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            self.db.add(new_entry)
            self.db.commit()
            return True
        except Exception as e:
            print(f"Error creating calendar entry: {e}")
            self.db.rollback()
            return False

    def update_calendar_entry(self, property_id: int, date: date, bid_id: str, price_amount: int) -> bool:
        """Update existing calendar entry with new highest bid"""
        try:
            entry = self.db.query(CalendarAvailability).filter(
                and_(
                    CalendarAvailability.property_id == property_id,
                    CalendarAvailability.date == date
                )
            ).first()

            if entry:
                entry.price_amount = price_amount
                entry.bid_id = bid_id
                entry.updated_at = datetime.now()
                self.db.commit()
                return True
            return False
        except Exception as e:
            print(f"Error updating calendar entry: {e}")
            self.db.rollback()
            return False
    def get_calendar_data_range(self,
                                check_in: date,
                                check_out: date,
                                property_id: int,
                                auction_id: str) -> Optional[list[type[CalendarAvailability]]]:
        """
        Get calendar availability data for a specific date range and property
        """
        return self.db.query(CalendarAvailability).filter(
            and_(
                CalendarAvailability.date >= check_in,
                CalendarAvailability.date <= check_out,
                CalendarAvailability.property_id == property_id,
                CalendarAvailability.auction_id == uuid.UUID(auction_id)
            )
        ).all()
