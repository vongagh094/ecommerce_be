from uuid import UUID
from typing import List
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.repositories.booking_repository import BookingRepository
from app.schemas.BookingDTO import BookingCreate, BookingUpdate, BookingResponse, MonthlySales, OccupancyDataPoint, PropertyResponse, PropertyStats
from app.db.models.user import User
from app.db.models.auction import Auction
import logging
from datetime import datetime, date

logger = logging.getLogger(__name__)

class BookingService:
    def __init__(self, booking_repository: BookingRepository):
        self.repository = booking_repository

    async def create_booking(self, booking_data: BookingCreate, db: AsyncSession) -> BookingResponse:
        try:
            # Kiểm tra các trường bắt buộc
            required_fields = ['guest_id', 'host_id', 'property_id', 'check_in_date', 'check_out_date', 'base_amount']
            missing_fields = [field for field in required_fields if getattr(booking_data, field) is None]
            if missing_fields:
                raise ValueError(f"Thiếu các trường bắt buộc: {', '.join(missing_fields)}")

            # Kiểm tra guest_id và host_id hợp lệ
            if booking_data.guest_id <= 0 or booking_data.host_id <= 0:
                raise ValueError("guest_id và host_id phải là số nguyên dương")

            # Kiểm tra base_amount hợp lệ
            if booking_data.base_amount <= 0:
                raise ValueError("base_amount phải lớn hơn 0")

            # Kiểm tra định dạng ngày
            if not isinstance(booking_data.check_in_date, (datetime, date)) or not isinstance(booking_data.check_out_date, (datetime, date)):
                raise ValueError("check_in_date và check_out_date phải là định dạng datetime hoặc date hợp lệ")

            # Kiểm tra ngày check-out phải sau ngày check-in
            if isinstance(booking_data.check_in_date, datetime):
                check_in_date = booking_data.check_in_date.date()
                check_out_date = booking_data.check_out_date.date()
            else:
                check_in_date = booking_data.check_in_date
                check_out_date = booking_data.check_out_date

            if check_in_date >= check_out_date:
                raise ValueError("Ngày check-out phải sau ngày check-in")

            # Kiểm tra sự tồn tại của guest_id, host_id, và auction_id
            logger.info(f"Checking guest_id={booking_data.guest_id}, host_id={booking_data.host_id}, auction_id={booking_data.auction_id}")
            query = select(User).where(User.id == booking_data.guest_id)
            result = await db.execute(query)
            if not result.scalars().first():
                raise ValueError(f"guest_id {booking_data.guest_id} không tồn tại trong bảng users")

            query = select(User).where(User.id == booking_data.host_id)
            result = await db.execute(query)
            if not result.scalars().first():
                raise ValueError(f"host_id {booking_data.host_id} không tồn tại trong bảng users")

            if booking_data.auction_id:
                query = select(Auction).where(Auction.id == booking_data.auction_id)
                result = await db.execute(query)
                if not result.scalars().first():
                    raise ValueError(f"auction_id {booking_data.auction_id} không tồn tại trong bảng auctions")

            # Tính total_nights
            total_nights = (check_out_date - check_in_date).days
            if total_nights <= 0:
                raise ValueError("Booking phải có ít nhất một đêm")

            # Tính total_amount
            cleaning_fee = booking_data.cleaning_fee or 0.0
            taxes = booking_data.taxes or 0.0
            total_amount = booking_data.base_amount + cleaning_fee + taxes

            # Tạo booking_dict
            booking_dict = booking_data.dict()
            booking_dict["check_in_date"] = check_in_date
            booking_dict["check_out_date"] = check_out_date
            booking_dict["total_nights"] = total_nights
            booking_dict["total_amount"] = total_amount
            logger.info(f"Prepared booking_dict: {booking_dict}")

            logger.info(f"Bắt đầu tạo booking với auction_id {booking_data.auction_id}")
            result = await self.repository.create_booking(booking_dict)
            if result is None:
                logger.error("create_booking returned None")
                raise ValueError("Không thể tạo booking: Repository trả về None")
            logger.info(f"Đã tạo booking thành công với ID {result.id}")
            return result
        except ValueError as e:
            logger.error(f"Lỗi khi tạo booking: {str(e)}")
            raise HTTPException(status_code=422, detail={"detail": str(e)})
        except SQLAlchemyError as e:
            logger.error(f"Lỗi cơ sở dữ liệu khi tạo booking: {str(e)}")
            raise HTTPException(status_code=500, detail={"detail": f"Lỗi server: Cơ sở dữ liệu không khả dụng - {str(e)}"})

    async def get_bookings_by_host(self, host_id: int, db: AsyncSession) -> List[BookingResponse]:
        try:
            return await self.repository.get_bookings_by_host(host_id)
        except SQLAlchemyError as e:
            logger.error(f"Lỗi cơ sở dữ liệu khi lấy bookings cho host {host_id}: {str(e)}")
            raise HTTPException(status_code=500, detail={"detail": f"Lỗi server: {str(e)}"})

    async def get_bookings_by_property(self, property_id: int, db: AsyncSession) -> List[BookingResponse]:
        try:
            return await self.repository.get_bookings_by_property_id(property_id)
        except SQLAlchemyError as e:
            logger.error(f"Lỗi cơ sở dữ liệu khi lấy bookings cho property {property_id}: {str(e)}")
            raise HTTPException(status_code=500, detail={"detail": f"Lỗi server: {str(e)}"})

    async def get_bookings_by_auction(self, auction_id: UUID, db: AsyncSession) -> List[BookingResponse]:
        try:
            return await self.repository.get_bookings_by_auction_id(auction_id)
        except SQLAlchemyError as e:
            logger.error(f"Lỗi cơ sở dữ liệu khi lấy bookings cho auction {auction_id}: {str(e)}")
            raise HTTPException(status_code=500, detail={"detail": f"Lỗi server: {str(e)}"})

    async def update_booking(self, booking_id: UUID, booking_update: BookingUpdate, db: AsyncSession) -> BookingResponse:
        try:
            logger.info(f"Bắt đầu cập nhật booking {booking_id}")
            update_dict = booking_update.dict(exclude_unset=True)
            if 'check_in_date' in update_dict and 'check_out_date' in update_dict:
                if isinstance(update_dict['check_in_date'], datetime):
                    update_dict['check_in_date'] = update_dict['check_in_date'].date()
                if isinstance(update_dict['check_out_date'], datetime):
                    update_dict['check_out_date'] = update_dict['check_out_date'].date()
                if update_dict['check_in_date'] >= update_dict['check_out_date']:
                    raise ValueError("Ngày check-out phải sau ngày check-in")
                total_nights = (update_dict['check_out_date'] - update_dict['check_in_date']).days
                if total_nights <= 0:
                    raise ValueError("Booking phải có ít nhất một đêm")
                update_dict['total_nights'] = total_nights
            if any(key in update_dict for key in ['base_amount', 'cleaning_fee', 'taxes']):
                booking = await self.repository.get_booking_by_id(booking_id)
                if booking.booking_status == "NOT_FOUND":
                    logger.info(f"Không tìm thấy booking với ID {booking_id}")
                    raise HTTPException(status_code=404, detail={"detail": "Không tìm thấy booking"})
                base_amount = update_dict.get('base_amount', booking.base_amount)
                cleaning_fee = update_dict.get('cleaning_fee', booking.cleaning_fee)
                taxes = update_dict.get('taxes', booking.taxes)
                if base_amount <= 0:
                    raise ValueError("base_amount phải lớn hơn 0")
                update_dict['total_amount'] = base_amount + cleaning_fee + taxes
            updated_booking = await self.repository.update_booking(booking_id, update_dict)
            if updated_booking.booking_status == "NOT_FOUND":
                logger.info(f"Không tìm thấy booking với ID {booking_id}")
                raise HTTPException(status_code=404, detail={"detail": "Không tìm thấy booking"})
            logger.info(f"Đã cập nhật booking với ID {booking_id}")
            return updated_booking
        except ValueError as e:
            logger.error(f"Lỗi khi cập nhật booking {booking_id}: {str(e)}")
            raise HTTPException(status_code=422, detail={"detail": str(e)})
        except SQLAlchemyError as e:
            logger.error(f"Lỗi cơ sở dữ liệu khi cập nhật booking {booking_id}: {str(e)}")
            raise HTTPException(status_code=500, detail={"detail": f"Lỗi server: Cơ sở dữ liệu không khả dụng - {str(e)}"})
        except HTTPException as e:
            raise e
        except Exception as e:
            logger.error(f"Lỗi server khi cập nhật booking {booking_id}: {str(e)}")
            raise HTTPException(status_code=500, detail={"detail": f"Lỗi server: {str(e)}"})

    async def update_booking_status(self, booking_id: UUID, booking_status: str, payment_status: str | None, db: AsyncSession) -> BookingResponse:
        try:
            logger.info(f"Bắt đầu cập nhật trạng thái booking {booking_id}")
            update_dict = {"booking_status": booking_status}
            if payment_status:
                update_dict["payment_status"] = payment_status
            updated_booking = await self.repository.update_booking(booking_id, update_dict)
            if updated_booking.booking_status == "NOT_FOUND":
                logger.info(f"Không tìm thấy booking với ID {booking_id}")
                raise HTTPException(status_code=404, detail={"detail": "Không tìm thấy booking"})
            logger.info(f"Đã cập nhật trạng thái booking với ID {booking_id}")
            return updated_booking
        except SQLAlchemyError as e:
            logger.error(f"Lỗi cơ sở dữ liệu khi cập nhật trạng thái booking {booking_id}: {str(e)}")
            raise HTTPException(status_code=500, detail={"detail": f"Lỗi server: Cơ sở dữ liệu không khả dụng - {str(e)}"})
        except HTTPException as e:
            raise e
        except Exception as e:
            logger.error(f"Lỗi server khi cập nhật trạng thái booking {booking_id}: {str(e)}")
            raise HTTPException(status_code=500, detail={"detail": f"Lỗi server: {str(e)}"})

    async def delete_booking(self, booking_id: UUID, db: AsyncSession) -> bool:
        try:
            logger.info(f"Bắt đầu xóa booking {booking_id}")
            success = await self.repository.delete_booking(booking_id)
            if not success:
                logger.info(f"Không tìm thấy booking với ID {booking_id}")
                raise HTTPException(status_code=404, detail={"detail": "Không tìm thấy booking"})
            logger.info(f"Đã xóa booking với ID {booking_id}")
            return True
        except SQLAlchemyError as e:
            logger.error(f"Lỗi cơ sở dữ liệu khi xóa booking {booking_id}: {str(e)}")
            raise HTTPException(status_code=500, detail={"detail": f"Lỗi server: Cơ sở dữ liệu không khả dụng - {str(e)}"})
        except HTTPException as e:
            raise e
        except Exception as e:
            logger.error(f"Lỗi server khi xóa booking {booking_id}: {str(e)}")
            raise HTTPException(status_code=500, detail={"detail": f"Lỗi server: {str(e)}"})

    async def get_monthly_sales(self, property_id: int, db: AsyncSession, year: int) -> List[MonthlySales]:
        try:
            monthly_sales_data = await self.repository.get_monthly_sales(property_id, year)
            return [MonthlySales(**data) for data in monthly_sales_data]
        except SQLAlchemyError as e:
            logger.error(f"Lỗi cơ sở dữ liệu khi lấy doanh thu hàng tháng cho property {property_id}: {str(e)}")
            raise HTTPException(status_code=500, detail={"detail": f"Lỗi server: {str(e)}"})

    async def get_occupancy(self, property_id: int, db: AsyncSession, period: str, num_points: int, units_available: int = 1) -> List[OccupancyDataPoint]:
        try:
            if period not in ["daily", "weekly", "monthly"]:
                raise ValueError("Period phải là 'daily', 'weekly', hoặc 'monthly'")
            occupancy_data = await self.repository.get_occupancy(property_id, period, num_points, units_available)
            return [OccupancyDataPoint(**data) for data in occupancy_data]
        except ValueError as e:
            logger.error(f"Lỗi khi lấy tỷ lệ lấp đầy cho property {property_id}: {str(e)}")
            raise HTTPException(status_code=422, detail={"detail": str(e)})
        except SQLAlchemyError as e:
            logger.error(f"Lỗi cơ sở dữ liệu khi lấy tỷ lệ lấp đầy cho property {property_id}: {str(e)}")
            raise HTTPException(status_code=500, detail={"detail": f"Lỗi server: {str(e)}"})

    async def get_property_stats(self, property_id: int, db: AsyncSession) -> PropertyStats:
        try:
            stats_data = await self.repository.get_property_stats(property_id)
            return PropertyStats(**stats_data)
        except SQLAlchemyError as e:
            logger.error(f"Lỗi cơ sở dữ liệu khi lấy thống kê cho property {property_id}: {str(e)}")
            raise HTTPException(status_code=500, detail={"detail": f"Lỗi server: {str(e)}"})
        
    async def get_properties_by_host(self, host_id: int, db: AsyncSession) -> List[PropertyResponse]:
        try:
            return await self.repository.get_properties_by_host(host_id)
        except SQLAlchemyError as e:
            logger.error(f"Lỗi cơ sở dữ liệu khi lấy danh sách properties cho host {host_id}: {str(e)}")
            raise HTTPException(status_code=500, detail={"detail": f"Lỗi server: {str(e)}"})
        