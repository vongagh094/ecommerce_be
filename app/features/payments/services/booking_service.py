"""Booking service for creating and managing bookings from payments."""

from typing import Any, Dict
from datetime import datetime, date, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import select, and_

from ....shared.exceptions import ValidationError, BusinessLogicError, NotFoundError, AuthorizationError
from ....db.models import Booking, Property, User, AuctionDB, Bids, CalendarAvailability, Conversation, PaymentSession
from ....features.messages.repositories.conversation_repository import ConversationRepository


class BookingService:
	def __init__(self, db: Session):
		self.db = db
		self.ws_notifier = None  # Will be injected by container

	def set_ws_notifier(self, notifier):
		"""Set WebSocket notifier for booking events."""
		self.ws_notifier = notifier

	def _notify_booking_confirmed(self, user_id: int, booking_id: str, property_name: str, check_in: str, check_out: str):
		"""Send booking confirmation notification via WebSocket if available."""
		if self.ws_notifier:
			try:
				message = {
					"type": "BOOKING_CONFIRMED",
					"bookingId": booking_id,
					"userId": str(user_id),
					"propertyName": property_name,
					"checkIn": check_in,
					"checkOut": check_out
				}
				self.ws_notifier.send_to_user(user_id, message)
			except Exception as e:
				print(f"WebSocket notification error: {e}")

	async def create_booking_for_payment(self, user_id: int, payment_id: str, idempotency_key: str | None) -> Dict[str, Any]:
		# payment_id == appTransId
		session = self.db.execute(select(PaymentSession).where(PaymentSession.app_trans_id == payment_id)).scalar_one_or_none()
		if not session:
			raise NotFoundError("PaymentSession", payment_id)
		if session.user_id != user_id:
			raise AuthorizationError("Forbidden")
		if session.status != "PAID":
			raise BusinessLogicError("Payment not completed", code="CONFLICT", status_code=409)

		bid = self.db.get(Bids, session.bid_id)
		prop_id = self._get_property_id_from_auction(session.auction_id)
		prop = self.db.get(Property, prop_id)

		# Determine check-in/out from selected nights
		selected = sorted(session.selected_nights)
		check_in = datetime.fromisoformat(selected[0]).date()
		check_out = datetime.fromisoformat(selected[-1]).date() + timedelta(days=1)
		self._ensure_dates_available(prop.id, check_in, check_out)

		total_nights = max(1, (check_out - check_in).days)
		booking = Booking(
			auction_id=session.auction_id,
			property_id=prop.id,
			guest_id=user_id,
			host_id=prop.host_id,
			check_in_date=check_in,
			check_out_date=check_out,
			total_nights=total_nights,
			base_amount=session.amount,
			cleaning_fee=0,
			taxes=0,
			total_amount=session.amount,
			booking_status="CONFIRMED",
			payment_status="PAID",
		)
		self.db.add(booking)
		self.db.commit()
		self.db.refresh(booking)

		self._block_calendar(prop.id, check_in, check_out)

		conv_repo = ConversationRepository(self.db)
		thread = conv_repo.get_existing_conversation(prop.host_id, user_id, prop.id) or conv_repo.create_conversation(
			data=type("DTO", (), {"model_dump": lambda s: {"guest_id": user_id, "host_id": prop.host_id, "property_id": prop.id}})()
		)

		# Notify booking confirmation
		self._notify_booking_confirmed(
			user_id, 
			str(booking.id), 
			prop.title, 
			booking.check_in_date.isoformat(), 
			booking.check_out_date.isoformat()
		)

		return {
			"id": str(booking.id),
			"referenceNumber": f"BK{datetime.utcnow().strftime('%Y%m%d%H%M')}-{'%03d' % (booking.created_at.microsecond % 1000)}",
			"propertyId": str(prop.id),
			"propertyName": prop.title,
			"hostId": str(prop.host_id),
			"checkIn": booking.check_in_date.isoformat(),
			"checkOut": booking.check_out_date.isoformat(),
			"guestCount": 1,
			"totalAmount": int(booking.total_amount),
			"status": booking.booking_status,
			"createdAt": booking.created_at.isoformat()
		}

	async def get_booking_by_payment(self, user_id: int, payment_id: str) -> Dict[str, Any]:
		# Try to find by payment session first
		session = self.db.execute(select(PaymentSession).where(PaymentSession.app_trans_id == payment_id)).scalar_one_or_none()
		if session:
			# Look for booking by auction_id and user_id
			bk = self.db.execute(select(Booking).where(and_(
				Booking.auction_id == session.auction_id,
				Booking.guest_id == user_id
			)).order_by(Booking.created_at.desc())).scalars().first()
			if bk:
				prop = self.db.get(Property, bk.property_id)
				return {
					"id": str(bk.id),
					"referenceNumber": f"BK{bk.created_at.strftime('%Y%m%d%H%M')}-{'%03d' % (bk.created_at.microsecond % 1000)}",
					"propertyId": str(prop.id),
					"propertyName": prop.title,
					"hostId": str(prop.host_id),
					"checkIn": bk.check_in_date.isoformat(),
					"checkOut": bk.check_out_date.isoformat(),
					"guestCount": 1,
					"totalAmount": int(bk.total_amount),
					"status": bk.booking_status,
					"createdAt": bk.created_at.isoformat()
				}
		
		# Fallback to latest booking
		bk = self.db.execute(select(Booking).where(Booking.guest_id == user_id).order_by(Booking.created_at.desc())).scalars().first()
		if not bk:
			raise NotFoundError("Booking", payment_id)
		prop = self.db.get(Property, bk.property_id)
		return {
			"id": str(bk.id),
			"referenceNumber": f"BK{bk.created_at.strftime('%Y%m%d%H%M')}-{'%03d' % (bk.created_at.microsecond % 1000)}",
			"propertyId": str(prop.id),
			"propertyName": prop.title,
			"hostId": str(prop.host_id),
			"checkIn": bk.check_in_date.isoformat(),
			"checkOut": bk.check_out_date.isoformat(),
			"guestCount": 1,
			"totalAmount": int(bk.total_amount),
			"status": bk.booking_status,
			"createdAt": bk.created_at.isoformat()
		}

	async def update_calendar(self, booking_id: str) -> None:
		bk = self.db.get(Booking, booking_id)
		if not bk:
			raise NotFoundError("Booking", booking_id)
		self._block_calendar(bk.property_id, bk.check_in_date, bk.check_out_date)

	async def create_conversation_thread(self, booking_id: str) -> Dict[str, Any]:
		bk = self.db.get(Booking, booking_id)
		if not bk:
			raise NotFoundError("Booking", booking_id)
		conv_repo = ConversationRepository(self.db)
		thread = conv_repo.get_existing_conversation(bk.host_id, bk.guest_id, bk.property_id) or conv_repo.create_conversation(
			data=type("DTO", (), {"model_dump": lambda s: {"guest_id": bk.guest_id, "host_id": bk.host_id, "property_id": bk.property_id}})()
		)
		return {"threadId": str(thread.id) if hasattr(thread, "id") else "thread-uuid"}

	async def send_confirmation_email(self, booking_id: str) -> None:
		return None

	def _get_property_id_from_auction(self, auction_id):
		a = self.db.execute(select(AuctionDB).where(AuctionDB.id == auction_id)).scalar_one()
		return a.property_id

	def _ensure_dates_available(self, property_id: int, check_in: date, check_out: date) -> None:
		curr = check_in
		while curr < check_out:
			row = self.db.execute(select(CalendarAvailability).where(and_(CalendarAvailability.property_id == property_id, CalendarAvailability.date == curr))).scalar_one_or_none()
			if row and not row.is_available:
				raise BusinessLogicError("Requested dates are not available", code="CONFLICT", status_code=409)
			curr += timedelta(days=1)

	def _block_calendar(self, property_id: int, check_in: date, check_out: date) -> None:
		curr = check_in
		while curr < check_out:
			row = self.db.execute(select(CalendarAvailability).where(and_(CalendarAvailability.property_id == property_id, CalendarAvailability.date == curr))).scalar_one_or_none()
			if row:
				row.is_available = False
			else:
				row = CalendarAvailability(property_id=property_id, date=curr, is_available=False)
				self.db.add(row)
			curr += timedelta(days=1)
		self.db.commit() 