"""ZaloPay payment endpoints."""

from fastapi import APIRouter, Depends, Body, Path, Header
from sqlmodel import Session

from ....shared.dependencies.database import get_db_session
from ....shared.dependencies.auth import require_auth
from ..services.payment_service import PaymentService
from ....core.container import Container

router = APIRouter(prefix="/payment/zalopay")

container = Container()

def get_payment_service(db: Session = Depends(get_db_session)) -> PaymentService:
    service = PaymentService(db)
    return container.wire_payment_service(service)

@router.post("/create")
async def create_zalopay_order(
    payload: dict = Body(...),
    idempotency_key: str = Header(None),
    user_id: int = Depends(require_auth),
    payment_service: PaymentService = Depends(get_payment_service)
):
    """Create a ZaloPay order."""
    return await payment_service.create_zalopay_order(user_id, payload, idempotency_key)

@router.get("/status/{app_trans_id}")
async def get_zalopay_status(
    app_trans_id: str = Path(...),
    user_id: int = Depends(require_auth),
    payment_service: PaymentService = Depends(get_payment_service)
):
    """Get ZaloPay payment status."""
    return await payment_service.get_zalopay_status(user_id, app_trans_id)

@router.post("/callback")
async def zalopay_callback(
    payload: dict = Body(...),
    payment_service: PaymentService = Depends(get_payment_service)
):
    """ZaloPay callback endpoint (no auth required)."""
    return await payment_service.handle_zalopay_callback(payload)


@router.get("/sessions/{session_id}")
async def get_payment_session(
	session_id: str = Path(...),
	user=Depends(require_auth),
	service: PaymentService = Depends(get_payment_service)
):
	return await service.get_payment_session(user.id, session_id)


@router.get("/transactions/{transaction_id}")
async def get_payment_transaction(
	transaction_id: str = Path(...),
	user=Depends(require_auth),
	service: PaymentService = Depends(get_payment_service)
):
	return await service.get_payment_transaction(user.id, transaction_id) 