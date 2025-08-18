"""Offer service for partial and second-chance offers."""

from typing import List, Dict, Any
from datetime import timedelta
from sqlalchemy.orm import Session
from sqlalchemy import select, and_

from ....shared.exceptions import ValidationError, NotFoundError, AuthorizationError
from ....db.models import SecondChanceOffer, Bids


class OfferService:
	def __init__(self, db: Session):
		self.db = db

	async def accept_offer(self, user_id: int, offer_id: str, selected_nights: List[str]) -> Dict[str, Any]:
		if not selected_nights:
			raise ValidationError("selectedNights cannot be empty", code="VALIDATION_ERROR")
		# For partial offers, we model via SecondChanceOffer linked to a bid of the user
		offer = self.db.get(SecondChanceOffer, offer_id)
		if not offer:
			raise NotFoundError("Offer", offer_id)
		bid = self.db.get(Bids, offer.bid_id)
		if bid.user_id != user_id:
			raise AuthorizationError("Forbidden")
		self._validate_nights_within_offer(bid, selected_nights)
		total = self._calc_total(bid, selected_nights)
		offer.status = "ACCEPTED"
		self.db.commit()
		return {"acceptedNights": selected_nights, "totalAmount": total}

	async def decline_offer(self, user_id: int, offer_id: str, reason: str | None) -> Dict[str, Any]:
		offer = self.db.get(SecondChanceOffer, offer_id)
		if not offer:
			raise NotFoundError("Offer", offer_id)
		bid = self.db.get(Bids, offer.bid_id)
		if bid.user_id != user_id:
			raise AuthorizationError("Forbidden")
		offer.status = "DECLINED"
		self.db.commit()
		return {"nextBidderNotified": True}

	async def list_second_chance_offers(self, user_id: int) -> List[Dict[str, Any]]:
		rows = self.db.execute(select(SecondChanceOffer, Bids).join(Bids, SecondChanceOffer.bid_id == Bids.id).where(and_(Bids.user_id == user_id, SecondChanceOffer.status == "WAITING"))).all()
		result = []
		for offer, bid in rows:
			result.append({
				"id": str(offer.id),
				"originalBidId": str(bid.id),
				"userId": str(bid.user_id),
				"auctionId": str(bid.auction_id),
				"offeredNights": self._dates_in_range(offer.offered_check_in, offer.offered_check_out),
				"amount": int(bid.total_amount),
				"responseDeadline": offer.response_deadline.isoformat(),
				"status": offer.status,
			})
		return result

	async def get_second_chance_offer(self, user_id: int, offer_id: str) -> Dict[str, Any]:
		offer = self.db.get(SecondChanceOffer, offer_id)
		if not offer:
			raise NotFoundError("Offer", offer_id)
		bid = self.db.get(Bids, offer.bid_id)
		if bid.user_id != user_id:
			raise AuthorizationError("Forbidden")
		return {
			"id": str(offer.id),
			"originalBidId": str(bid.id),
			"userId": str(bid.user_id),
			"auctionId": str(bid.auction_id),
			"offeredNights": self._dates_in_range(offer.offered_check_in, offer.offered_check_out),
			"amount": int(bid.total_amount),
			"responseDeadline": offer.response_deadline.isoformat(),
			"status": offer.status,
		}

	async def accept_second_chance_offer(self, user_id: int, offer_id: str) -> None:
		offer = self.db.get(SecondChanceOffer, offer_id)
		if not offer:
			raise NotFoundError("Offer", offer_id)
		bid = self.db.get(Bids, offer.bid_id)
		if bid.user_id != user_id:
			raise AuthorizationError("Forbidden")
		offer.status = "ACCEPTED"
		self.db.commit()

	async def decline_second_chance_offer(self, user_id: int, offer_id: str, reason: str | None) -> Dict[str, Any]:
		offer = self.db.get(SecondChanceOffer, offer_id)
		if not offer:
			raise NotFoundError("Offer", offer_id)
		bid = self.db.get(Bids, offer.bid_id)
		if bid.user_id != user_id:
			raise AuthorizationError("Forbidden")
		offer.status = "DECLINED"
		self.db.commit()
		return {"nextBidderNotified": True}

	async def track_decline_reason(self, user_id: int, payload: Dict[str, Any]) -> None:
		# Persist analytics using BidEvent or a dedicated table (out-of-scope here)
		return None

	def _calc_total(self, bid: Bids, selected_nights: List[str]) -> int:
		total_nights = max(1, (bid.check_out - bid.check_in).days)
		ppn = int(bid.total_amount / total_nights)
		return ppn * len(selected_nights)

	def _validate_nights_within_offer(self, bid: Bids, selected_nights: List[str]) -> None:
		allowed = set(self._dates_in_range(bid.check_in, bid.check_out))
		for d in selected_nights:
			if d not in allowed:
				raise ValidationError("selectedNights include invalid dates", code="VALIDATION_ERROR")

	def _dates_in_range(self, start, end) -> List[str]:
		curr = start
		res = []
		while curr < end:
			res.append(curr.isoformat())
			curr += timedelta(days=1)
		return res 