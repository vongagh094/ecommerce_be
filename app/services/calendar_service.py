from app.db.repositories.calender_repository import CalendarRepository
from app.schemas.calendarDTO import PropertyCalendarResponseData, DayData
import logging

logger = logging.getLogger(__name__)
class CalendarService:
    def __init__(self, calendar_repository: CalendarRepository):
        self.calendar_repository = calendar_repository

    def get_property_calendar(
            self,
            property_id: int,
            year: int,
            month: int
    ) -> PropertyCalendarResponseData:
        """
        Main method: Get property calendar với business logic
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
        """Validate calendar request parameters"""

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



