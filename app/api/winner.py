from fastapi import APIRouter, HTTPException, Depends
from dependency_injector.wiring import Provide, inject

from app.features.notification.services.notification_service import NotificationService
from app.services.winner_service import WinnerService
from app.core.container import Container
from app.schemas.winnerDTO import DailyWinner

router = APIRouter()

@router.get("/{auction_id}")
@inject
def get_auction_winners(
        auction_id: str,
        allow_partial: bool = False,
        winner_service: WinnerService = Depends(Provide[Container.winner_service]),
):
    """
    Lấy danh sách người chiến thắng auction dưới dạng booking periods

    Returns:
    [
        {
            "auction_id": "auction_123",
            "check_in_win": "2025-08-25",
            "check_out_win": "2025-08-28",
            "amount": 135.0,
            "user_id": 1
        }
    ]
    """
    try:
        # ✅ Gọi service method mới
        booking_periods = winner_service.calculate_booking_periods(auction_id)
        return booking_periods
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Simple health check
@router.get("/check/health")
def health():
    return {"status": "ok"}