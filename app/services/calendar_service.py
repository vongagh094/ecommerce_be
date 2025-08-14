from app.db.repositories.calender_repository import CalendarRepository
from app.schemas.calendarDTO import PropertyCalendarResponseData, DayData
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class CalendarService:
    def __init__(self, calendar_repository: CalendarRepository):
        self.calendar_repository = calendar_repository

    # ===== KEEP EXISTING METHODS UNCHANGED =====

    def get_property_calendar(
            self,
            property_id: int,
            year: int,
            month: int
    ) -> PropertyCalendarResponseData:
        """
        Main method: Get property calendar với business logic
        [KEEP EXISTING IMPLEMENTATION UNCHANGED]
        """
        try:
            # Validate inputs
            self._validate_calendar_request(property_id, year, month)

            # Get base calendar data
            calendar_data = self.calendar_repository.get_calendar_data(
                property_id, year, month
            )

            # Convert to Pydantic models
            day_objects = []
            for day_dict in calendar_data:
                day_obj = DayData(
                    date=day_dict['date'],
                    highest_bid=int(day_dict['highest_bid']),
                    active_bids=day_dict['active_bids'],
                    minimum_to_win=int(day_dict['minimum_to_win']),
                    base_price=int(day_dict['base_price']),
                    demand_level=day_dict['demand_level'],
                    success_rate=day_dict['success_rate'],
                    is_available=day_dict['is_available'],
                    is_booked=day_dict['is_booked']
                )
                day_objects.append(day_obj)

            return PropertyCalendarResponseData(
                property_id=property_id,
                month=month,
                year=year,
                days=day_objects
            )

        except Exception as e:
            logger.error(f"Error in get_property_calendar: {e}")
            raise

    def _validate_calendar_request(
            self,
            property_id: int,
            year: int,
            month: int
    ) -> None:
        """Validate calendar request parameters [KEEP UNCHANGED]"""

        if property_id <= 0:
            raise ValueError("Invalid property_id")

        if year < 2020 or year > 2030:
            raise ValueError("Invalid year")

        if month < 1 or month > 12:
            raise ValueError("Invalid month")

        # Check if the property exists
        exists = self.calendar_repository.validate_property_exists(property_id)
        if not exists:
            raise ValueError(f"Property {property_id} not found")

    def get_auction_highest_bids_for_polling(
            self,
            auction_id: str,
            property_id: int,
            start_date: date,
            end_date: date
    ) -> Dict[str, Dict]:
        """
        FIXED METHOD: Get highest bids for date range - For frontend polling
        Properly handle SQLAlchemy objects
        """
        try:
            # Use repository method to get calendar availability data
            calendar_entries = self.calendar_repository.get_calendar_availability_for_date_range(
                property_id, start_date, end_date
            )

            # Build result dictionary
            result = {}
            current_date = start_date

            while current_date <= end_date:
                date_str = current_date.strftime('%Y-%m-%d')

                # Find calendar entry for this date
                # FIXED: Handle SQLAlchemy objects properly
                entry = None
                for calendar_entry in calendar_entries:
                    # Access SQLAlchemy object attributes with dot notation
                    if calendar_entry.date == current_date:
                        entry = calendar_entry
                        break

                if entry and entry.price_amount:
                    result[date_str] = {
                        "highest_bid": int(entry.price_amount),
                        "bid_id": str(entry.bid_id) if entry.bid_id else None,
                        "bidder_id": getattr(entry, 'highest_bidder_id', None),
                        "total_bids": getattr(entry, 'bid_count', 1),
                        "is_available": entry.is_available,
                        "updated_at": entry.updated_at.isoformat() if entry.updated_at else None
                    }
                else:
                    result[date_str] = {
                        "highest_bid": 0,
                        "bid_id": None,
                        "bidder_id": None,
                        "total_bids": 0,
                        "is_available": True,
                        "updated_at": None
                    }

                current_date += timedelta(days=1)

            logger.info(f"Retrieved highest bids for auction {auction_id}, dates {start_date} to {end_date}")
            return result

        except Exception as e:
            logger.error(f"Error getting auction highest bids: {e}")
            logger.exception("Full exception details:")  # Add full stack trace
            return {}

    def get_user_bid_comparison_data(
            self,
            auction_id: str,
            user_id: int,
            property_id: int,
            user_bid_data: Dict
    ) -> Dict:
        """
        NEW METHOD: Compare user's bid with current highest bids
        For win/loss status calculation
        """
        try:
            if not user_bid_data:
                return {
                    "success": True,
                    "has_bid": False,
                    "comparison": {}
                }

            # Get user's date range
            start_date = datetime.fromisoformat(user_bid_data["check_in"]).date()
            end_date = datetime.fromisoformat(user_bid_data["check_out"]).date()

            # Get current highest bids for that range using repository
            highest_bids = self.get_auction_highest_bids_for_polling(
                auction_id, property_id, start_date, end_date
            )

            # Calculate win/loss status for each date
            comparison = {}
            user_price_per_night = user_bid_data["price_per_night"]

            current_date = start_date
            while current_date < end_date:
                date_str = current_date.strftime('%Y-%m-%d')
                current_highest = highest_bids.get(date_str, {}).get("highest_bid", 0)

                comparison[date_str] = {
                    "user_bid": user_price_per_night,
                    "current_highest": current_highest,
                    "status": "WINNING" if user_price_per_night >= current_highest else "LOSING",
                    "difference": user_price_per_night - current_highest,
                    "is_winning": user_price_per_night >= current_highest
                }

                current_date += timedelta(days=1)

            # Calculate overall statistics
            winning_dates = [d for d, data in comparison.items() if data["status"] == "WINNING"]
            losing_dates = [d for d, data in comparison.items() if data["status"] == "LOSING"]
            win_rate = len(winning_dates) / len(comparison) * 100 if comparison else 0

            logger.info(f"Calculated bid comparison for user {user_id}, win rate: {win_rate:.1f}%")

            return {
                "success": True,
                "has_bid": True,
                "user_bid": user_bid_data,
                "comparison": comparison,
                "summary": {
                    "win_rate": round(win_rate, 1),
                    "winning_dates": winning_dates,
                    "losing_dates": losing_dates,
                    "total_nights": len(comparison),
                    "winning_nights": len(winning_dates),
                    "losing_nights": len(losing_dates)
                }
            }

        except Exception as e:
            logger.error(f"Error calculating user bid comparison: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def update_calendar_with_new_bid(
            self,
            property_id: int,
            bid_record
    ) -> List[str]:
        """
        FIXED METHOD: Update calendar_availability when new bid is placed
        Handle repository responses properly
        """
        try:
            updated_dates = []
            current_date = bid_record.check_in

            while current_date < bid_record.check_out:
                date_str = current_date.strftime('%Y-%m-%d')

                # Check if this bid is higher than current highest for this date
                current_entry = self.calendar_repository.get_calendar_entry_for_date(
                    property_id, current_date
                )

                should_update = False

                if not current_entry:
                    # Create new entry using repository
                    success = self.calendar_repository.create_calendar_entry(
                        property_id=property_id,
                        date=current_date,
                        bid_id=bid_record.id,
                        price_amount=bid_record.price_per_night,
                        is_available=True
                    )
                    if success:
                        should_update = True
                        logger.info(f"Created new calendar entry for {current_date}")

                else:
                    # FIXED: Handle repository response properly
                    if isinstance(current_entry, dict):
                        current_price = current_entry.get('price_amount', 0) or 0
                    else:
                        # If it's a SQLAlchemy object
                        current_price = getattr(current_entry, 'price_amount', 0) or 0

                    if current_price < bid_record.price_per_night:
                        # Update existing entry using repository
                        success = self.calendar_repository.update_calendar_entry(
                            property_id=property_id,
                            date=current_date,
                            bid_id=bid_record.id,
                            price_amount=bid_record.price_per_night
                        )
                        if success:
                            should_update = True
                            logger.info(
                                f"Updated calendar entry for {current_date}: {current_price} → {bid_record.price_per_night}")

                if should_update:
                    updated_dates.append(date_str)

                current_date += timedelta(days=1)

            logger.info(f"Calendar updated for {len(updated_dates)} dates: {updated_dates}")
            return updated_dates

        except Exception as e:
            logger.error(f"Error updating calendar with new bid: {e}")
            logger.exception("Full exception details:")
            return []
