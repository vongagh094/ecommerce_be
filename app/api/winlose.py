# 📁 FILE: app/api/win_lose_routes.py

from fastapi import APIRouter, Depends, HTTPException
from app.core.container import Container
from dependency_injector.wiring import inject, Provide
from app.services.winlose_service import WinLoseService
from typing import Dict
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/user/{user_id}/auction/{auction_id}/status", operation_id="getUserWinLoseStatus")
@inject
async def get_user_win_lose_status(
        user_id: int,
        auction_id: str,
        winlose_service: WinLoseService = Depends(Provide[Container.winlose_service])
) -> Dict:
    """
    Lấy win-lose status của user trong auction cụ thể

    Args:
        user_id: ID của user
        auction_id: ID của auction

    Returns:
        Dict chứa thông tin win-lose analysis
        :param user_id:
        :param auction_id:
        :param winlose_service:
    """
    try:
        # 🔧 FIX: Gọi đúng tên method
        result = winlose_service.get_user_win_lose_status(user_id, auction_id)

        if not result.get("success"):
            raise HTTPException(
                status_code=500,
                detail=result.get("message", "Internal server error")
            )

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"API Error getting win-lose status: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/user/{user_id}/auction/{auction_id}/insights", operation_id="getUserBidInsights")
@inject
async def get_user_bid_insights(
        user_id: int,
        auction_id: str,
        winlose_service: WinLoseService = Depends(Provide[Container.winlose_service])
) -> Dict:
    """
    Lấy performance insights chi tiết của user bid

    Args:
        user_id: ID của user
        auction_id: ID của auction

    Returns:
        Dict chứa insights và recommendations
    """
    try:
        result = winlose_service.get_bid_performance_insights(user_id, auction_id)

        if not result.get("success"):
            raise HTTPException(
                status_code=500,
                detail=result.get("message", "Internal server error")
            )

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"API Error getting bid insights: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/user/{user_id}/auction/{auction_id}/summary", operation_id="getUserBidSummary")
@inject
async def get_user_bid_summary(
        user_id: int,
        auction_id: str,
        winlose_service: WinLoseService = Depends(Provide[Container.winlose_service])
) -> Dict:
    """
    Lấy summary nhanh của user bid (cho UI components)

    Args:
        user_id: ID của user
        auction_id: ID của auction

    Returns:
        Dict chứa summary thông tin cơ bản
    """
    try:
        result = winlose_service.get_user_win_lose_status(user_id, auction_id)

        if not result.get("success"):
            return {
                "success": True,
                "has_bid": False,
                "summary": None
            }

        if not result.get("has_bid"):
            return result

        # Trả về format đơn giản cho UI
        return {
            "success": True,
            "has_bid": True,
            "bid_id": result["bid_info"]["bid_id"],
            "summary": result["summary"],
            "bid_amount": result["bid_info"]["total_amount"],
            "price_per_night": result["bid_info"]["price_per_day"],
            "check_in": result["bid_info"]["check_in"],
            "check_out": result["bid_info"]["check_out"],
            "nights": result["bid_info"]["nights"]
        }

    except Exception as e:
        logger.error(f"API Error getting bid summary: {e}")
        return {
            "success": False,
            "has_bid": False,
            "message": f"Error: {str(e)}"
        }


@router.get("/health", operation_id="winLoseHealthCheck")
async def health_check() -> Dict:
    """
    Health check endpoint cho win-lose service
    """
    return {
        "status": "healthy",
        "service": "win-lose-api",
        "version": "1.0.0"
    }