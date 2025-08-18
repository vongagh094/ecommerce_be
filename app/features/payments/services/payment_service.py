"""Payment service for ZaloPay integration."""

import hmac
import hashlib
import json
import time
from typing import Any, Dict, Optional
from datetime import datetime, timedelta

import requests
from sqlalchemy.orm import Session
from sqlalchemy import select, and_, func

from ....core.config import settings
from ....shared.exceptions import ValidationError, BusinessLogicError, NotFoundError, AuthorizationError
from ....db.models import Bids, AuctionDB, Property, Booking, PaymentSession, PaymentTransaction

SESSION_TTL_SECONDS = 15 * 60


class PaymentService:
	def __init__(self, db: Session):
		self.db = db
		self.cfg = settings.zalopay
		self.ws_notifier = None  # Will be injected by container

	def set_ws_notifier(self, notifier):
		"""Set WebSocket notifier for payment events."""
		self.ws_notifier = notifier

	def _notify_payment_status(self, user_id: int, payment_id: str, status: str, transaction_id: Optional[str] = None):
		"""Send payment status notification via WebSocket if available."""
		if self.ws_notifier:
			try:
				message = {
					"type": "PAYMENT_STATUS",
					"paymentId": payment_id,
					"userId": str(user_id),
					"status": status,
				}
				if transaction_id:
					message["transactionId"] = transaction_id
				self.ws_notifier.send_to_user(user_id, message)
			except Exception as e:
				print(f"WebSocket notification error: {e}")

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

	def _gen_app_trans_id(self, order_suffix: str) -> str:
		ts = time.strftime("%y%m%d")
		return f"{ts}_{order_suffix}"

	def _sign_key1(self, app_id: str, app_trans_id: str, app_user: str, amount: int, app_time: int, embed_data: str, item: str) -> str:
		data = f"{app_id}|{app_trans_id}|{app_user}|{amount}|{app_time}|{embed_data}|{item}"
		return hmac.new(self.cfg.key1.encode(), data.encode(), hashlib.sha256).hexdigest()

	def _sign_query(self, app_id: str, app_trans_id: str) -> str:
		data = f"{app_id}|{app_trans_id}|{self.cfg.key1}"
		return hmac.new(self.cfg.key1.encode(), data.encode(), hashlib.sha256).hexdigest()

	def _verify_key2(self, data_str: str, mac: str) -> bool:
		calc = hmac.new(self.cfg.key2.encode(), data_str.encode(), hashlib.sha256).hexdigest()
		return hmac.compare_digest(calc, mac)

	def _calc_amount_for_selection(self, bid: Bids, selected_nights: list[str]) -> int:
		night_price = int(bid.total_amount / max(1, (bid.check_out - bid.check_in).days))
		return night_price * len(selected_nights)

	def _create_or_get_session(self, *, user_id: int, auction_id: str, bid_id: str, app_trans_id: str, amount: int, selected_nights: list[str], idempotency_key: Optional[str], order_url: str) -> PaymentSession:
		existing = self.db.execute(select(PaymentSession).where(PaymentSession.app_trans_id == app_trans_id)).scalar_one_or_none()
		if existing:
			return existing
		session = PaymentSession(
			user_id=user_id,
			auction_id=auction_id,
			bid_id=bid_id,
			app_trans_id=app_trans_id,
			amount=amount,
			selected_nights=selected_nights,
			status="PENDING",
			idempotency_key=idempotency_key or None,
			expires_at=datetime.utcnow() + timedelta(seconds=SESSION_TTL_SECONDS),
			order_url=order_url
		)
		self.db.add(session)
		self.db.commit()
		self.db.refresh(session)
		return session

	def _update_session_status(self, app_trans_id: str, status: str) -> PaymentSession:
		session = self.db.execute(select(PaymentSession).where(PaymentSession.app_trans_id == app_trans_id)).scalar_one_or_none()
		if session:
			session.status = status
			self.db.commit()
		return session

	async def create_zalopay_order(self, user_id: int, payload: Dict[str, Any], idempotency_key: Optional[str]) -> Dict[str, Any]:
		auction_id = payload.get("auctionId")
		selected_nights = payload.get("selectedNights", [])
		req_amount = int(payload.get("amount", 0))
		order_info = payload.get("orderInfo", "")
		if not auction_id:
			raise ValidationError("auctionId is required", code="VALIDATION_ERROR")
		if not selected_nights:
			raise ValidationError("selectedNights required", code="VALIDATION_ERROR")

		bid = self.db.execute(select(Bids).where(and_(Bids.auction_id == auction_id, Bids.user_id == user_id))).scalar_one_or_none()
		if not bid:
			raise NotFoundError("Bid", auction_id)

		allowed = set()
		curr = bid.check_in
		from datetime import timedelta
		while curr < bid.check_out:
			allowed.add(curr.isoformat())
			curr += timedelta(days=1)
		for d in selected_nights:
			if d not in allowed:
				raise ValidationError("selectedNights contain dates outside bid range", code="VALIDATION_ERROR")

		srv_amount = self._calc_amount_for_selection(bid, selected_nights)
		if req_amount != srv_amount:
			raise BusinessLogicError("Amount mismatch", code="CONFLICT", status_code=409)

		app_id = self.cfg.app_id
		app_user = str(user_id)
		app_time = int(time.time() * 1000)
		app_trans_id = self._gen_app_trans_id(f"{auction_id}_{int(time.time())}")
		item = json.dumps([])
		embed_data = json.dumps({"auctionId": auction_id, "nights": selected_nights})
		mac = self._sign_key1(app_id, app_trans_id, app_user, srv_amount, app_time, embed_data, item)
		callback_url = self.cfg.callback_path
		create_payload = {
			"app_id": app_id,
			"app_trans_id": app_trans_id,
			"app_user": app_user,
			"app_time": app_time,
			"amount": srv_amount,
			"item": item,
			"embed_data": embed_data,
			"description": order_info,
			"callback_url": callback_url,
			"mac": mac,
		}
		resp = requests.post(self.cfg.create_url, json=create_payload, timeout=15)
		if resp.status_code >= 400:
			raise BusinessLogicError(f"ZaloPay create failed: {resp.text}", code="PAYMENT_CREATE_FAILED", status_code=502)
		data = resp.json()
		order_url = data.get("order_url") or data.get("orderurl")

		# Persist session + transaction
		session = self._create_or_get_session(
			user_id=user_id,
			auction_id=str(auction_id),
			bid_id=str(bid.id),
			app_trans_id=app_trans_id,
			amount=srv_amount,
			selected_nights=selected_nights,
			idempotency_key=idempotency_key,
			order_url=order_url,
		)
		ptx = PaymentTransaction(
			session_id=session.id,
			app_trans_id=app_trans_id,
			amount=srv_amount,
			status="PENDING",
			raw=None,
		)
		self.db.add(ptx)
		self.db.commit()
		
		# Notify payment initiated
		self._notify_payment_status(user_id, str(session.id), "INITIATED")
		
		return {"orderUrl": order_url, "appTransId": app_trans_id, "amount": srv_amount}

	async def get_zalopay_status(self, user_id: int, app_trans_id: str) -> Dict[str, Any]:
		session = self.db.execute(select(PaymentSession).where(PaymentSession.app_trans_id == app_trans_id)).scalar_one_or_none()
		if not session:
			raise NotFoundError("PaymentSession", app_trans_id)
		if session.user_id != user_id:
			raise AuthorizationError("Forbidden")
		payload = {
			"app_id": self.cfg.app_id,
			"app_trans_id": app_trans_id,
			"mac": self._sign_query(self.cfg.app_id, app_trans_id),
		}
		resp = requests.post(self.cfg.query_url, data=payload, timeout=15)
		if resp.status_code >= 400:
			raise BusinessLogicError("ZaloPay query failed", code="PAYMENT_QUERY_FAILED", status_code=502)
		data = resp.json()
		zstatus = data.get("return_code")
		status_map = {1: "PAID", 2: "PENDING", 3: "FAILED"}
		status = status_map.get(zstatus, "PENDING")
		session.status = status
		ptx = self.db.execute(select(PaymentTransaction).where(PaymentTransaction.app_trans_id == app_trans_id)).scalar_one_or_none()
		if ptx:
			ptx.status = status
			ptx.zp_trans_id = data.get("zp_trans_id")
			ptx.paid_at = datetime.utcfromtimestamp(data.get("server_time")/1000) if data.get("server_time") else None
			ptx.raw = data
		self.db.commit()
		
		# Notify status change if completed or failed
		if status in ["PAID", "FAILED"]:
			ws_status = "COMPLETED" if status == "PAID" else "FAILED"
			self._notify_payment_status(user_id, str(session.id), ws_status, ptx.zp_trans_id if ptx else None)
			
		return {"status": status, "transactionId": data.get("zp_trans_id"), "amount": data.get("amount"), "paidAt": data.get("server_time")}

	async def handle_zalopay_callback(self, payload: Dict[str, Any]) -> Dict[str, Any]:
		data_str = payload.get("data", "")
		mac = payload.get("mac", "")
		if not self._verify_key2(data_str, mac):
			return {"return_code": -1, "return_message": "mac not equal"}
		data = json.loads(data_str)
		app_trans_id = data.get("app_trans_id")
		ret = int(data.get("return_code", 0))
		status = "PAID" if ret == 1 else "FAILED"
		session = self.db.execute(select(PaymentSession).where(PaymentSession.app_trans_id == app_trans_id)).scalar_one_or_none()
		if session:
			session.status = status
			ptx = self.db.execute(select(PaymentTransaction).where(PaymentTransaction.app_trans_id == app_trans_id)).scalar_one_or_none()
			if ptx:
				ptx.status = status
				ptx.zp_trans_id = data.get("zp_trans_id")
				ptx.paid_at = datetime.utcfromtimestamp(data.get("server_time")/1000) if data.get("server_time") else None
				ptx.raw = data
			self.db.commit()
			
			# Notify payment status via WebSocket
			ws_status = "COMPLETED" if status == "PAID" else "FAILED"
			self._notify_payment_status(session.user_id, str(session.id), ws_status, data.get("zp_trans_id"))
			
		return {"return_code": 1, "return_message": "success"}

	async def get_payment_session(self, user_id: int, session_id: str) -> Dict[str, Any]:
		session = self.db.get(PaymentSession, session_id) or self.db.execute(select(PaymentSession).where(PaymentSession.app_trans_id == session_id)).scalar_one_or_none()
		if not session:
			raise NotFoundError("PaymentSession", session_id)
		if session.user_id != user_id:
			raise AuthorizationError("Forbidden")
		return {
			"id": str(session.id),
			"auctionId": str(session.auction_id),
			"userId": session.user_id,
			"amount": session.amount,
			"currency": "VND",
			"status": session.status,
			"appTransId": session.app_trans_id,
			"orderUrl": session.order_url,
			"createdAt": session.created_at.isoformat() if hasattr(session, "created_at") and session.created_at else None,
			"expiresAt": session.expires_at.isoformat() if session.expires_at else None,
		}

	async def get_payment_transaction(self, user_id: int, transaction_id: str) -> Dict[str, Any]:
		ptx = self.db.execute(select(PaymentTransaction).where(PaymentTransaction.app_trans_id == transaction_id)).scalar_one_or_none() or self.db.get(PaymentTransaction, transaction_id)
		if not ptx:
			raise NotFoundError("PaymentTransaction", transaction_id)
		session = self.db.get(PaymentSession, ptx.session_id)
		if session.user_id != user_id:
			raise AuthorizationError("Forbidden")
		return {
			"id": str(ptx.id),
			"sessionId": str(ptx.session_id),
			"appTransId": ptx.app_trans_id,
			"transactionId": ptx.zp_trans_id,
			"amount": ptx.amount,
			"status": ptx.status,
			"paidAt": ptx.paid_at.isoformat() if ptx.paid_at else None,
		} 