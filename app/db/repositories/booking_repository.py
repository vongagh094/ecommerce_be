from uuid import UUID
from typing import List, Dict
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from app.db.models.bookings import Booking
from app.db.models.property import Property
from app.schemas.BookingDTO import BookingResponse, PropertyResponse
from app.db.models.auction import Auction
import logging
from sqlalchemy import func
from datetime import datetime, timedelta

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

    async def get_monthly_sales(self, property_id: int, year: int) -> List[Dict]:
        try:
            months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            monthly_sales = []
            for month in range(1, 13):
                start_date = datetime(year, month, 1)
                end_date = (start_date + timedelta(days=31)).replace(day=1) - timedelta(days=1) if month < 12 else datetime(year, 12, 31)
                
                query = select(
                    func.sum(Booking.total_amount).label("actual"),
                    func.avg(Booking.total_amount).label("expected")
                ).where(
                    Booking.property_id == property_id,
                    Booking.booking_status == "CONFIRMED",
                    Booking.check_in_date >= start_date,
                    Booking.check_in_date <= end_date
                )
                result = await self.db.execute(query)
                total, avg_historical = result.first()
                total = total or 0.0
                avg_historical = avg_historical or 0.0
                
                query_count = select(func.count()).where(
                    Booking.property_id == property_id,
                    Booking.booking_status == "CONFIRMED",
                    Booking.check_in_date >= start_date,
                    Booking.check_in_date <= end_date
                )
                result_count = await self.db.execute(query_count)
                booking_count = result_count.scalar() or 0
                
                monthly_sales.append({
                    "month": months[month - 1],
                    "actual": float(total),
                    "expected": float(avg_historical * booking_count)
                })
            return monthly_sales
        except SQLAlchemyError as e:
            logger.error(f"Lỗi cơ sở dữ liệu khi lấy doanh thu hàng tháng cho property {property_id}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Lỗi server khi lấy doanh thu hàng tháng cho property {property_id}: {str(e)}")
            raise
    async def get_occupancy(self, db: AsyncSession, property_id: int, period: str, num_points: int, units_available: int = 1) -> List[Dict]:
        try:
            if period not in ["daily", "weekly", "monthly"]:
                raise HTTPException(status_code=400, detail="Period phải là 'daily', 'weekly' hoặc 'monthly'")
            
            # Sử dụng datetime.utcnow() và chuyển thành datetime.date
            end_date = datetime.utcnow().date()
            if period == "daily":
                start_date = end_date - timedelta(days=num_points)
                time_delta = timedelta(days=1)
            elif period == "weekly":
                start_date = end_date - timedelta(weeks=num_points)
                time_delta = timedelta(weeks=1)
            elif period == "monthly":
                start_date = end_date - timedelta(days=num_points * 30)
                time_delta = timedelta(days=30)
            else:
                logger.error(f"Period không hợp lệ: {period}")
                raise HTTPException(status_code=400, detail="Period phải là 'daily', 'weekly' hoặc 'monthly'")

            # Truy vấn các đặt phòng hợp lệ
            query = select(Booking).where(
                Booking.property_id == property_id,
                Booking.booking_status == "CONFIRMED",
                Booking.check_out_date > Booking.check_in_date,
                # Chuyển đổi datetime.date thành datetime.datetime để so sánh
                Booking.check_in_date <= datetime.combine(end_date, datetime.min.time()),
                Booking.check_out_date >= datetime.combine(start_date, datetime.min.time())
            )
            result = await db.execute(query)
            bookings = result.scalars().all()

            logger.info(f"Tìm thấy {len(bookings)} đặt phòng hợp lệ cho property_id={property_id}")

            # Tạo danh sách các khoảng thời gian
            occupancy_data = []
            current_date = start_date
            while current_date < end_date:
                booked_nights = 0
                total_nights = time_delta.days * units_available

                # Tính số đêm được đặt trong khoảng thời gian
                for booking in bookings:
                    booking_start = max(booking.check_in_date.date() if isinstance(booking.check_in_date, datetime) else booking.check_in_date, current_date)
                    booking_end = min(booking.check_out_date.date() if isinstance(booking.check_out_date, datetime) else booking.check_out_date, current_date + time_delta)
                    if booking_end > booking_start:
                        booked_nights += (booking_end - booking_start).days

                # Tính tỷ lệ lấp đầy
                occupancy_rate = (booked_nights / total_nights * 100) if total_nights > 0 else 0
                occupancy_data.append({
                    "date": current_date.strftime("%Y-%m-%d"),
                    "occupancyRate": round(occupancy_rate, 2),
                    "period": period
                })
                current_date += time_delta

            return occupancy_data
        except Exception as e:
            logger.error(f"Lỗi khi tính toán tỷ lệ lấp đầy cho property_id={property_id}, period={period}: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Lỗi máy chủ: {str(e)}")

    async def get_property_stats(self, property_id: int) -> Dict:
        try:
            query = select(func.count()).where(
                Booking.property_id == property_id,
                Booking.booking_status == "CONFIRMED"
            )
            result = await self.db.execute(query)
            total_booking = result.scalar() or 0

            query = select(func.count()).where(
                Booking.property_id == property_id,
                Booking.auction_id.isnot(None),
                Booking.booking_status == "PENDING"
            )
            result = await self.db.execute(query)
            total_bid_active = result.scalar() or 0

            query = select(func.sum(Booking.total_amount)).where(
                Booking.property_id == property_id,
                Booking.booking_status == "CONFIRMED"
            )
            result = await self.db.execute(query)
            total_sales = result.scalar() or 0.0

            historical_query = select(func.avg(Booking.total_amount)).where(
                Booking.property_id == property_id,
                Booking.booking_status == "CONFIRMED",
                func.extract('year', Booking.check_in_date) < datetime.now().year
            )
            result = await self.db.execute(historical_query)
            avg_historical = result.scalar() or 0.0
            expected_sales = avg_historical * total_booking

            sales_increase = total_sales - expected_sales

            query = select(func.count()).where(Property.id == property_id)
            result = await self.db.execute(query)
            total_listing = result.scalar() or 0

            return {
                "totalBooking": total_booking,
                "totalBidActive": total_bid_active,
                "sales": total_sales,
                "expectedSales": expected_sales,
                "totalSales": total_sales,
                "salesIncrease": sales_increase,
                "totalListing": total_listing
            }
        except SQLAlchemyError as e:
            logger.error(f"Lỗi cơ sở dữ liệu khi lấy thống kê cho property {property_id}: {str(e)}")
            raise

    async def get_properties_by_host(self, host_id: int) -> List[PropertyResponse]:
        try:
            query = select(Property).where(Property.host_id == host_id)
            result = await self.db.execute(query)
            properties = result.scalars().all()
            return [PropertyResponse(id=prop.id, name=prop.title, location=f"{prop.city}, {prop.country}" if prop.city and prop.country else None) for prop in properties]
        except SQLAlchemyError as e:
            logger.error(f"Lỗi cơ sở dữ liệu khi lấy danh sách properties cho host {host_id}: {str(e)}")
            raise