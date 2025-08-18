"""Payments API module."""

from fastapi import APIRouter

from .zalopay_api import router as zalopay_router
from .booking_api import router as booking_router
from .payment_api import router as payment_router

router = APIRouter()
router.include_router(zalopay_router, tags=["payment"], prefix="")
router.include_router(payment_router, tags=["payment"], prefix="")
router.include_router(booking_router, tags=["payment"]) 

__all__ = ["router"] 