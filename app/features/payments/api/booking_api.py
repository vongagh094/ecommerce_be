"""Booking endpoints related to payments."""

from fastapi import APIRouter, Depends, Path, Body
from sqlmodel import Session

from ....shared.dependencies.database import get_db_session
from ....shared.dependencies.auth import require_auth

from ..services.payment_service import PaymentService
from ..services.booking_service import BookingService
from ....core.container import Container

router = APIRouter()

container = Container()

def get_payment_service(db: Session = Depends(get_db_session)) -> PaymentService:
    service = PaymentService(db)
    return container.wire_payment_service(service)

def get_booking_service(db: Session = Depends(get_db_session)) -> BookingService:
    service = BookingService(db)
    return container.wire_booking_service(service)

@router.post("/payment/{payment_id}/booking")
async def create_booking(
    payment_id: str = Path(...),
    idempotency_key: str = Body(None),
    user_id: int = Depends(require_auth),
    booking_service: BookingService = Depends(get_booking_service)
):
    """Create booking from successful payment."""
    return await booking_service.create_booking_for_payment(user_id, payment_id, idempotency_key)

@router.get("/payment/{payment_id}/booking")
async def get_booking_for_payment(
    payment_id: str = Path(...),
    user_id: int = Depends(require_auth),
    booking_service: BookingService = Depends(get_booking_service)
):
    """Get booking created for a payment."""
    return await booking_service.get_booking_by_payment(user_id, payment_id)

@router.post("/bookings/{booking_id}/update-calendar")
async def update_calendar(
    booking_id: str = Path(...),
    user_id: int = Depends(require_auth),
    booking_service: BookingService = Depends(get_booking_service)
):
    """Update calendar availability for a booking."""
    await booking_service.update_calendar(booking_id)
    return {}

@router.post("/bookings/{booking_id}/conversation")
async def create_conversation(
    booking_id: str = Path(...),
    user_id: int = Depends(require_auth),
    booking_service: BookingService = Depends(get_booking_service)
):
    """Create conversation thread for a booking."""
    return await booking_service.create_conversation_thread(booking_id)

@router.post("/bookings/{booking_id}/send-confirmation")
async def send_confirmation(
    booking_id: str = Path(...),
    user_id: int = Depends(require_auth),
    booking_service: BookingService = Depends(get_booking_service)
):
    """Send booking confirmation email."""
    await booking_service.send_confirmation_email(booking_id)
    return {} 