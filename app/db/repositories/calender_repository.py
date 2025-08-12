from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import text
import logging
logger = logging.getLogger(__name__)

class CalendarRepository:
    """Repository cho calendar data access với direct table functions"""

    def __init__(self, db: Session):
        self.db = db
    def get_calendar_data(
            self,
            property_id: int,
            year: int,
            month: int
    ) -> List[Dict[str, Any]]:
        """
        Main method: Get calendar data sử dụng optimized direct function
        """
        try:
            query = text("SELECT * FROM get_calendar_optimized_direct(:property_id, :year, :month)")

            result = self.db.execute(query, {
                'property_id': property_id,
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


