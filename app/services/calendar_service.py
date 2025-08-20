from app.db.repositories.bid_repository import BidRepository
from app.db.repositories.calender_repository import CalendarRepository
from app.schemas.BidDTO import BidRecord
from app.schemas.calendarDTO import PropertyCalendarResponseData, DayData, MessageResponseDTO
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class CalendarService:
    def __init__(self,
                 calendar_repository: CalendarRepository,
                 bid_repository: BidRepository
                 ):
        self.calendar_repository = calendar_repository
        self.bid_repository = bid_repository
    # ===== KEEP EXISTING METHODS UNCHANGED =====

    def get_property_calendar(
            self,
            property_id: int,
            auction_id:str,
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
                property_id,auction_id,year, month
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

    def update_calendar_availability(self,
                                     id:int,
                                     check_in:date,
                                     check_out:date,
                                     property_id:int,
                                     auction_id:str,
                                     price_per_night) -> MessageResponseDTO:
        """Update availability of a calendar day"""

        # tính giá phòng trên ngày
        nights = (check_out - check_in).days
        if nights:
            total_price = price_per_night * nights
        else:
            total_price = price_per_night * (nights + 1)
        total_day = (check_out - check_in).days + 1
        bid_amount = total_price / total_day
        # 1. Lấy chuỗi ngày mà user đó bid
            #1.1 có thể có ngày,có thể chưa có ngày đó - hoặc nên tạo ngày khi có auction -> trigger
            #=> luôn có ngày để check
        try:
            calendar_entries = self.calendar_repository.get_calendar_data_range(
                check_in,
                check_out,
                property_id,
                auction_id
            )
        except Exception as e:
            logger.error(f"Error getting calendar entries: {e}")
            return MessageResponseDTO(
                success=False,
                message=f"Error getting calendar entries: {str(e)}",
                Details={}
            )
        # 2. So sánh bid_amount có lớn hơn => danh sách những ngày sẽ update
        update_calendar_list = []
        for entry in calendar_entries:
            if entry.price_amount is None or entry.price_amount < bid_amount:
                entry.bid_id = id
                entry.price_amount = bid_amount
                entry.updated_at = datetime.now()
                update_calendar_list.append(entry)

        # 3. Update calendar entries
        try:
            for entry in update_calendar_list:
                success = self.calendar_repository.update_calendar_entry(
                    property_id=property_id,
                    date=entry.date,
                    bid_id=str(entry.bid_id) if entry.bid_id else None,
                    price_amount=entry.price_amount
                )
                if not success:
                    logger.warning(f"Failed to update calendar entry for date {entry.date}")

            return MessageResponseDTO(
                success=True,
                message=f"Successfully updated {len(update_calendar_list)} calendar entries",
                Details={
                    "updated_entries": len(update_calendar_list),
                    "date_range": {
                        "check_in": check_in.isoformat(),
                        "check_out": check_out.isoformat()
                    },
                    "bid_amount": bid_amount
                }
            )

        except Exception as e:
            logger.error(f"Error updating calendar entries: {e}")
            return MessageResponseDTO(
                success=False,
                message=f"Error updating calendar entries: {str(e)}",
                Details={"error": str(e)}
            )
