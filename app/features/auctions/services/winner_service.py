"""Winner service handling winners and full-win flow."""

from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select, and_, func
from datetime import timedelta

from ....shared.exceptions import NotFoundError, BusinessLogicError, AuthorizationError
from ....db.models import Bids, Auction, Property, PropertyImage


class WinnerService:
	def __init__(self, db: Session):
		self.db = db

	async def list_winners_for_user(self, user_id: int) -> List[Dict[str, Any]]:
		rows = self.db.execute(
			select(Bids, Auction, Property).join(Auction, Bids.auction_id == Auction.id).join(Property, Property.id == Auction.property_id).where(and_(Bids.user_id == user_id, Bids.status == "ACTIVE"))
		).all()
		result = []
		for bid, auction, prop in rows:
			awarded = self._compute_awarded_nights(bid)
			result.append({
				"id": str(bid.id),
				"auctionId": str(auction.id),
				"property": {
					"id": str(prop.id),
					"title": prop.title,
					"location": {"city": prop.city, "state": prop.state},
					"images": [{"image_url": img.image_url} for img in prop.images[:1]],
					"max_guests": prop.max_guests,
				},
				"bidAmount": int(bid.total_amount),
				"checkIn": bid.check_in.isoformat(),
				"checkOut": bid.check_out.isoformat(),
				"isPartialWin": bid.partial_awarded,
				"awardedNights": awarded,
				"status": "PENDING_PAYMENT",
				"paymentDeadline": None,
			})
		return result

	async def get_winner_for_user_and_auction(self, user_id: int, auction_id: str) -> Dict[str, Any]:
		bid = self.db.execute(select(Bids).where(and_(Bids.auction_id == auction_id, Bids.user_id == user_id))).scalar_one_or_none()
		if not bid:
			raise NotFoundError("Winner", auction_id)
		auction = self.db.get(Auction, auction_id)
		prop = self.db.get(Property, auction.property_id)
		return {
			"id": str(bid.id),
			"auctionId": str(auction.id),
			"property": {
				"id": str(prop.id),
				"title": prop.title,
				"location": {"city": prop.city, "state": prop.state},
				"images": [{"image_url": img.image_url} for img in prop.images[:1]],
				"max_guests": prop.max_guests,
			},
			"bidAmount": int(bid.total_amount),
			"checkIn": bid.check_in.isoformat(),
			"checkOut": bid.check_out.isoformat(),
			"isPartialWin": bid.partial_awarded,
			"awardedNights": self._compute_awarded_nights(bid),
			"status": "PENDING_PAYMENT",
			"paymentDeadline": None,
		}

	async def accept_full_win(self, user_id: int, auction_id: str) -> None:
		bid = self.db.execute(select(Bids).where(and_(Bids.auction_id == auction_id, Bids.user_id == user_id))).scalar_one_or_none()
		if not bid:
			raise NotFoundError("Winner", auction_id)
		# Mark as accepted (placeholder using status)
		bid.status = "ACCEPTED"
		self.db.commit()

	async def decline_offer(self, user_id: int, auction_id: str, reason: str | None) -> Dict[str, Any]:
		bid = self.db.execute(select(Bids).where(and_(Bids.auction_id == auction_id, Bids.user_id == user_id))).scalar_one_or_none()
		if not bid:
			raise NotFoundError("Winner", auction_id)
		bid.status = "DECLINED"
		self.db.commit()
		# Trigger fallback (next bidder) - placeholder
		return {"fallbackTriggered": True}

	def _compute_awarded_nights(self, bid: Bids) -> list[dict]:
		nights = []
		if not bid:
			return nights
		total_nights = max(1, (bid.check_out - bid.check_in).days)
		price_per_night = int(bid.total_amount / total_nights)
		curr = bid.check_in
		while curr < bid.check_out:
			nights.append({"date": curr.isoformat(), "pricePerNight": price_per_night})
			curr += timedelta(days=1)
		return nights 