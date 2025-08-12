from fastapi import APIRouter
from app.services.calendar_service import CalendarService
from app.core.container import Container
from dependency_injector.wiring import inject, Provide
from fastapi import Depends
router = APIRouter()
@router.get("/properties/{property_id}/calendar")
@inject
async def get_calendar(
    property_id: int,
    year: int,
    month: int,
    calendar_service: CalendarService = Depends(Provide[Container.calendar_service])
):
    return calendar_service.get_property_calendar(
        property_id, year, month
    )