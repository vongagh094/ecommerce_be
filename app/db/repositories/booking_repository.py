from uuid import UUID
from typing import List, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from app.db.models.bookings import Booking
from app.schemas.BookingDTO import BookingResponse
from app.db.models.auction import Auction
import logging

logger = logging.getLogger(__name__)

class BookingRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_booking(self, booking_dict: Dict) -> BookingResponse:
        try:
            booking = Booking(**booking_dict)
            self.db.add(booking)
            await self.db.commit()
            await self.db.refresh(booking)
            if not booking:
                logger.error("Booking object is None after commit and refresh")
                raise ValueError("Không thể tạo booking: Đối tượng booking không hợp lệ")
            logger.info(f"Đã tạo booking với ID {booking.id}")
            return BookingResponse.model_validate(booking)
        except SQLAlchemyError as e:
            await self.db.rollback()
            logger.error(f"Lỗi cơ sở dữ liệu khi tạo booking: {str(e)}")
            raise
        except ValueError as e:
            await self.db.rollback()
            logger.error(f"Lỗi khi tạo booking: {str(e)}")
            raise
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Lỗi server khi tạo booking: {str(e)}")
            raise
        
    async def get_bookings_by_host(self, host_id: int) -> List[BookingResponse]:
        try:
            query = select(Booking).where(Booking.host_id == host_id)
            result = await self.db.execute(query)
            bookings = result.scalars().all()
            return [BookingResponse.model_validate(booking) for booking in bookings]
        except SQLAlchemyError as e:
            logger.error(f"Lỗi cơ sở dữ liệu khi lấy bookings cho host {host_id}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Lỗi server khi lấy bookings cho host {host_id}: {str(e)}")
            raise

    async def get_booking_by_id(self, booking_id: UUID) -> BookingResponse:
        try:
            query = select(Booking).where(Booking.id == booking_id)
            result = await self.db.execute(query)
            booking = result.scalars().first()
            if booking:
                return BookingResponse.model_validate(booking)
            logger.info(f"Không tìm thấy booking với ID {booking_id}")
            return BookingResponse(id=booking_id, auction_id=UUID(int=0), guest_id=0, host_id=0, property_id=0, check_in_date=None, check_out_date=None, total_nights=0, base_amount=0.0, cleaning_fee=0.0, taxes=0.0, total_amount=0.0, booking_status="NOT_FOUND", payment_status="NOT_FOUND", created_at=None, updated_at=None)
        except SQLAlchemyError as e:
            logger.error(f"Lỗi cơ sở dữ liệu khi lấy booking {booking_id}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Lỗi server khi lấy booking {booking_id}: {str(e)}")
            raise

    async def get_all_bookings(self) -> List[BookingResponse]:
        try:
            query = select(Booking)
            result = await self.db.execute(query)
            bookings = result.scalars().all()
            return [BookingResponse.model_validate(booking) for booking in bookings]
        except SQLAlchemyError as e:
            logger.error(f"Lỗi cơ sở dữ liệu khi lấy tất cả bookings: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Lỗi server khi lấy tất cả bookings: {str(e)}")
            raise

    async def get_bookings_by_auction_id(self, auction_id: UUID) -> List[BookingResponse]:
        try:
            query = select(Booking).where(Booking.auction_id == auction_id)
            result = await self.db.execute(query)
            bookings = result.scalars().all()
            return [BookingResponse.model_validate(booking) for booking in bookings]
        except SQLAlchemyError as e:
            logger.error(f"Lỗi cơ sở dữ liệu khi lấy bookings cho auction {auction_id}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Lỗi server khi lấy bookings cho auction {auction_id}: {str(e)}")
            raise
        
    async def get_bookings_by_property_id(self, property_id: int) -> List[BookingResponse]:
        try:
            query = select(Booking).where(Booking.property_id == property_id)
            result = await self.db.execute(query)
            bookings = result.scalars().all()
            return [BookingResponse.model_validate(booking) for booking in bookings]
        except SQLAlchemyError as e:
            logger.error(f"Lỗi cơ sở dữ liệu khi lấy bookings cho property {property_id}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Lỗi server khi lấy bookings cho property {property_id}: {str(e)}")
            raise

    async def get_bookings_by_auction_ids(self, auction_ids: List[UUID]) -> List[BookingResponse]:
        try:
            query = select(Booking).where(Booking.auction_id.in_(auction_ids))
            result = await self.db.execute(query)
            bookings = result.scalars().all()
            return [BookingResponse.model_validate(booking) for booking in bookings]
        except SQLAlchemyError as e:
            logger.error(f"Lỗi cơ sở dữ liệu khi lấy bookings cho auction_ids: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Lỗi server khi lấy bookings cho auction_ids: {str(e)}")
            raise

    async def get_auction_ids_by_property(self, property_id: int) -> List[UUID]:
        try:
            query = select(Auction.id).where(Auction.property_id == property_id)
            result = await self.db.execute(query)
            return [auction_id for auction_id in result.scalars().all()]
        except SQLAlchemyError as e:
            logger.error(f"Lỗi cơ sở dữ liệu khi lấy auction_ids cho property {property_id}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Lỗi server khi lấy auction_ids cho property {property_id}: {str(e)}")
            raise

    async def update_booking(self, booking_id: UUID, update_dict: Dict) -> BookingResponse:
        try:
            query = select(Booking).where(Booking.id == booking_id)
            result = await self.db.execute(query)
            booking = result.scalars().first()
            if not booking:
                logger.info(f"Không tìm thấy booking với ID {booking_id}")
                return BookingResponse(id=booking_id, auction_id=UUID(int=0), guest_id=0, host_id=0, property_id=0, check_in_date=None, check_out_date=None, total_nights=0, base_amount=0.0, cleaning_fee=0.0, taxes=0.0, total_amount=0.0, booking_status="NOT_FOUND", payment_status="NOT_FOUND", created_at=None, updated_at=None)
            for key, value in update_dict.items():
                if hasattr(booking, key):
                    setattr(booking, key, value)
            await self.db.commit()
            await self.db.refresh(booking)
            return BookingResponse.model_validate(booking)
        except SQLAlchemyError as e:
            await self.db.rollback()
            logger.error(f"Lỗi cơ sở dữ liệu khi cập nhật booking {booking_id}: {str(e)}")
            raise
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Lỗi server khi cập nhật booking {booking_id}: {str(e)}")
            raise

    async def delete_booking(self, booking_id: UUID) -> bool:
        try:
            query = select(Booking).where(Booking.id == booking_id)
            result = await self.db.execute(query)
            booking = result.scalars().first()
            if not booking:
                logger.info(f"Không tìm thấy booking với ID {booking_id}")
                return False
            await self.db.delete(booking)
            await self.db.commit()
            return True
        except SQLAlchemyError as e:
            await self.db.rollback()
            logger.error(f"Lỗi cơ sở dữ liệu khi xóa booking {booking_id}: {str(e)}")
            raise
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Lỗi server khi xóa booking {booking_id}: {str(e)}")
            raise