from fastapi import APIRouter, Depends, HTTPException, Query
from app.core.container import Container
from dependency_injector.wiring import inject, Provide

from app.schemas.BidDTO import BidsDTO
from app.services.calendar_service import CalendarService
from app.services.bid_service import BidService
router = APIRouter()
@router.get("/properties/{property_id}/calendar")
@inject
async def get_calendar(
    property_id: int,
    auction_id:str,
    year: int,
    month: int,
    calendar_service: CalendarService = Depends(Provide[Container.calendar_service])
):
    return calendar_service.get_property_calendar(
        property_id, auction_id ,year, month
    )