from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List
from app.db.sessions.session import get_async_db_session
from app.core.container import Container
from dependency_injector.wiring import inject, Provide
from app.schemas.BookingDTO import BookingCreate, BookingUpdate, BookingResponse, MonthlySales, OccupancyDataPoint, PropertyStats, PropertyResponse
from app.services.booking_service import BookingService
from fastapi import Query
from datetime import datetime

router = APIRouter()

async def get_async_session():
    async with get_async_db_session() as session:
        yield session

@router.post("/create", response_model=BookingResponse, operation_id="createBooking")
@inject
async def create_booking(
    booking: BookingCreate,
    db: AsyncSession = Depends(get_async_session),
    booking_service: BookingService = Depends(Provide[Container.booking_service])
):
    try:
        return await booking_service.create_booking(booking, db)
    except ValueError as e:
        raise HTTPException(status_code=422, detail={"detail": str(e)})
    except Exception as e:
        raise HTTPException(status_code=500, detail={"detail": f"Lỗi server: {str(e)}"})

@router.get("/host/{host_id}", response_model=List[BookingResponse], operation_id="getBookingsByHost")
@inject
async def get_bookings_by_host(
    host_id: int,
    db: AsyncSession = Depends(get_async_session),
    booking_service: BookingService = Depends(Provide[Container.booking_service])
):
    try:
        return await booking_service.get_bookings_by_host(host_id, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail={"detail": f"Lỗi server: {str(e)}"})

@router.get("/property/{property_id}", response_model=List[BookingResponse], operation_id="getBookingsByProperty")
@inject
async def get_bookings_by_property(
    property_id: int,
    db: AsyncSession = Depends(get_async_session),
    booking_service: BookingService = Depends(Provide[Container.booking_service])
):
    try:
        return await booking_service.get_bookings_by_property(property_id, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail={"detail": f"Lỗi server: {str(e)}"})

@router.get("/auction/{auction_id}", response_model=List[BookingResponse], operation_id="getBookingsByAuction")
@inject
async def get_bookings_by_auction(
    auction_id: UUID,
    db: AsyncSession = Depends(get_async_session),
    booking_service: BookingService = Depends(Provide[Container.booking_service])
):
    try:
        return await booking_service.get_bookings_by_auction(auction_id, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail={"detail": f"Lỗi server: {str(e)}"})

@router.put("/update/{booking_id}", response_model=BookingResponse, operation_id="updateBooking")
@inject
async def update_booking(
    booking_id: UUID,
    booking_update: BookingUpdate,
    db: AsyncSession = Depends(get_async_session),
    booking_service: BookingService = Depends(Provide[Container.booking_service])
):
    try:
        booking = await booking_service.update_booking(booking_id, booking_update, db)
        if not booking:
            raise HTTPException(status_code=404, detail={"detail": "Không tìm thấy booking"})
        return booking
    except ValueError as e:
        raise HTTPException(status_code=422, detail={"detail": str(e)})
    except Exception as e:
        raise HTTPException(status_code=500, detail={"detail": f"Lỗi server: {str(e)}"})

@router.delete("/delete/{booking_id}", operation_id="deleteBooking")
@inject
async def delete_booking(
    booking_id: UUID,
    db: AsyncSession = Depends(get_async_session),
    booking_service: BookingService = Depends(Provide[Container.booking_service])
):
    try:
        success = await booking_service.delete_booking(booking_id, db)
        if not success:
            raise HTTPException(status_code=404, detail={"detail": "Không tìm thấy booking"})
        return {"message": "Xóa booking thành công"}
    except Exception as e:
        raise HTTPException(status_code=500, detail={"detail": f"Lỗi server: {str(e)}"})

@router.get("/property/{property_id}/monthly-sales", response_model=List[MonthlySales], operation_id="getMonthlySalesByProperty")
@inject
async def get_monthly_sales_by_property(
    property_id: int,
    year: int = Query(datetime.now().year, description="Năm để lấy dữ liệu doanh thu"),
    db: AsyncSession = Depends(get_async_session),
    booking_service: BookingService = Depends(Provide[Container.booking_service])
):
    try:
        return await booking_service.get_monthly_sales(property_id, db, year)
    except Exception as e:
        raise HTTPException(status_code=500, detail={"detail": f"Lỗi server: {str(e)}"})

@router.get("/property/{property_id}/occupancy", response_model=List[OccupancyDataPoint], operation_id="getOccupancyByProperty")
@inject
async def get_occupancy_by_property(
    property_id: int,
    period: str = Query("daily", description="Khoảng thời gian: daily, weekly, monthly"),
    num_points: int = Query(30, description="Số lượng điểm dữ liệu"),
    units_available: int = Query(1, description="Số đơn vị khả dụng của bất động sản"),
    db: AsyncSession = Depends(get_async_session),
    booking_service: BookingService = Depends(Provide[Container.booking_service])
):
    try:
        return await booking_service.get_occupancy(property_id, db, period, num_points, units_available)
    except ValueError as e:
        raise HTTPException(status_code=422, detail={"detail": str(e)})
    except Exception as e:
        raise HTTPException(status_code=500, detail={"detail": f"Lỗi server: {str(e)}"})

@router.get("/property/{property_id}/stats", response_model=PropertyStats, operation_id="getPropertyStats")
@inject
async def get_property_stats(
    property_id: int,
    db: AsyncSession = Depends(get_async_session),
    booking_service: BookingService = Depends(Provide[Container.booking_service])
):
    try:
        return await booking_service.get_property_stats(property_id, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail={"detail": f"Lỗi server: {str(e)}"})
    
@router.get("/host/{host_id}/properties", response_model=List[PropertyResponse], operation_id="getPropertiesByHost")
@inject
async def get_properties_by_host(
    host_id: int,
    db: AsyncSession = Depends(get_async_session),
    booking_service: BookingService = Depends(Provide[Container.booking_service])
):
    try:
        return await booking_service.get_properties_by_host(host_id, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail={"detail": f"Lỗi server: {str(e)}"})