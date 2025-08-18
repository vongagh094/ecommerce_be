"""Generic payment endpoints (sessions, transactions)."""

from fastapi import APIRouter, Depends, Path
from sqlmodel import Session

from ....shared.dependencies.database import get_db_session
from ....shared.dependencies.auth import require_auth
from ..services.payment_service import PaymentService
from ....core.container import Container

router = APIRouter(prefix="/payment")

container = Container()

def get_payment_service(db: Session = Depends(get_db_session)) -> PaymentService:
    service = PaymentService(db)
    return container.wire_payment_service(service)

@router.get("/sessions/{session_id}")
async def get_payment_session(
    session_id: str = Path(...),
    user_id: int = Depends(require_auth),
    payment_service: PaymentService = Depends(get_payment_service)
):
    """Get payment session by ID."""
    return await payment_service.get_payment_session(user_id, session_id)

@router.get("/transactions/{transaction_id}")
async def get_payment_transaction(
    transaction_id: str = Path(...),
    user_id: int = Depends(require_auth),
    payment_service: PaymentService = Depends(get_payment_service)
):
    """Get payment transaction by ID."""
    return await payment_service.get_payment_transaction(user_id, transaction_id) 