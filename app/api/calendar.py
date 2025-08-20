from fastapi import APIRouter, Depends, HTTPException, Query
from app.core.container import Container
from dependency_injector.wiring import inject, Provide
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

@router.get("/auction/{auction_id}/user/{user_id}/win-loss-status")
@inject
async def get_user_win_loss_status(
        auction_id: str,
        user_id: int,
        property_id: int = Query(..., description="Property ID"),
        calendar_service: CalendarService = Depends(Provide[Container.calendar_service]),
        bid_service: BidService = Depends(Provide[Container.bid_service])
):
    """
    Get user's win/loss status vs current highest bids
    FOR FRONTEND WIN/LOSS DISPLAY
    """
    try:
        # Get user's current bid
        user_bid = bid_service.get_user_current_bid(user_id, auction_id)

        if not user_bid:
            return {
                "success": True,
                "has_bid": False,
                "comparison": {},
                "message": "User has no active bid for this auction"
            }

        # Get comparison data
        comparison_data = calendar_service.get_user_bid_comparison_data(
            auction_id, user_id, property_id, user_bid
        )

        return comparison_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting win/loss status: {str(e)}")

