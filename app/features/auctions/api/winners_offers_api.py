"""Auction winners and offers API endpoints."""

from typing import List, Optional
from fastapi import APIRouter, Depends, Path, Body
from sqlmodel import Session

from ....shared.dependencies.database import get_db_session
from ....shared.dependencies.auth import require_auth
from ....shared.exceptions import NotFoundError, ValidationError, BusinessLogicError

from ..services.winner_service import WinnerService
from ..services.offer_service import OfferService

router = APIRouter(prefix="/auctions")


def get_winner_service(db: Session = Depends(get_db_session)) -> WinnerService:
	return WinnerService(db)

def get_offer_service(db: Session = Depends(get_db_session)) -> OfferService:
	return OfferService(db)


@router.get("/winners/me")
async def get_my_winners(
	user=Depends(require_auth),
	service: WinnerService = Depends(get_winner_service)
):
	return await service.list_winners_for_user(user.id)


@router.get("/winners/{auction_id}")
async def get_my_winner_by_auction(
	auction_id: str = Path(...),
	user=Depends(require_auth),
	service: WinnerService = Depends(get_winner_service)
):
	return await service.get_winner_for_user_and_auction(user.id, auction_id)


@router.post("/winners/{auction_id}/accept")
async def accept_full_win(
	auction_id: str = Path(...),
	user=Depends(require_auth),
	service: WinnerService = Depends(get_winner_service)
):
	await service.accept_full_win(user.id, auction_id)
	return {"success": True}


@router.post("/winners/{auction_id}/decline")
async def decline_full_or_partial(
	auction_id: str = Path(...),
	payload: dict = Body(default={}),
	user=Depends(require_auth),
	service: WinnerService = Depends(get_winner_service)
):
	reason = payload.get("reason")
	result = await service.decline_offer(user.id, auction_id, reason)
	return {"success": True, "fallbackTriggered": result.get("fallbackTriggered", False)}


@router.post("/offers/{offer_id}/accept")
async def accept_offer(
	offer_id: str = Path(...),
	payload: dict = Body(...),
	user=Depends(require_auth),
	service: OfferService = Depends(get_offer_service)
):
	selected = payload.get("selectedNights") or []
	resp = await service.accept_offer(user.id, offer_id, selected)
	return {"success": True, "acceptedNights": resp["acceptedNights"], "totalAmount": resp["totalAmount"]}


@router.post("/offers/{offer_id}/decline")
async def decline_offer(
	offer_id: str = Path(...),
	payload: dict = Body(default={}),
	user=Depends(require_auth),
	service: OfferService = Depends(get_offer_service)
):
	reason = payload.get("reason")
	resp = await service.decline_offer(user.id, offer_id, reason)
	return {"success": True, "nextBidderNotified": resp.get("nextBidderNotified", False)}


@router.get("/offers/second-chance/me")
async def get_my_second_chance_offers(
	user=Depends(require_auth),
	service: OfferService = Depends(get_offer_service)
):
	return await service.list_second_chance_offers(user.id)


@router.get("/offers/second-chance/{offer_id}")
async def get_second_chance_offer(
	offer_id: str = Path(...),
	user=Depends(require_auth),
	service: OfferService = Depends(get_offer_service)
):
	return await service.get_second_chance_offer(user.id, offer_id)


@router.post("/offers/second-chance/{offer_id}/accept")
async def accept_second_chance_offer(
	offer_id: str = Path(...),
	user=Depends(require_auth),
	service: OfferService = Depends(get_offer_service)
):
	await service.accept_second_chance_offer(user.id, offer_id)
	return {"success": True}


@router.post("/offers/second-chance/{offer_id}/decline")
async def decline_second_chance_offer(
	offer_id: str = Path(...),
	payload: dict = Body(default={}),
	user=Depends(require_auth),
	service: OfferService = Depends(get_offer_service)
):
	reason = payload.get("reason")
	resp = await service.decline_second_chance_offer(user.id, offer_id, reason)
	return {"success": True, "nextBidderNotified": resp.get("nextBidderNotified", False)}


@router.post("/analytics/decline")
async def track_decline_reason(
	payload: dict = Body(...),
	user=Depends(require_auth),
	service: OfferService = Depends(get_offer_service)
):
	await service.track_decline_reason(user.id, payload)
	return {"success": True} 