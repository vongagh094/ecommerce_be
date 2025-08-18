# Auction Winners, Offers, Payment (ZaloPay), and Booking - Backend

Base path: `/api/v1`
Auth: All endpoints require Bearer JWT unless stated otherwise.

## Auctions

- GET `/auctions/winners/me`
- GET `/auctions/winners/{auctionId}`
- POST `/auctions/winners/{auctionId}/accept`
- POST `/auctions/winners/{auctionId}/decline`
- POST `/auctions/offers/{offerId}/accept`
- POST `/auctions/offers/{offerId}/decline`
- GET `/auctions/offers/second-chance/me`
- GET `/auctions/offers/second-chance/{offerId}`
- POST `/auctions/offers/second-chance/{offerId}/accept`
- POST `/auctions/offers/second-chance/{offerId}/decline`
- POST `/auctions/analytics/decline`

Note: Services are stubbed and ready to be wired to DB queries (`WinnerService`, `OfferService`).

## Payment (ZaloPay)

- POST `/payment/zalopay/create`
- GET `/payment/zalopay/status/{appTransId}`
- POST `/payment/zalopay/callback` (no auth)
- GET `/payment/zalopay/sessions/{sessionId}`
- GET `/payment/zalopay/transactions/{transactionId}`

Signing:
- Create: HMAC-SHA256 with key1 over `app_id|app_trans_id|app_user|amount|app_time|embed_data|item`.
- Query: HMAC-SHA256 with key1 over `app_id|app_trans_id|key1`.
- Callback verification: HMAC-SHA256 with key2 over `data` string; compare with `mac`.

Env config (add to `.env`):
- `ZALOPAY_APP_ID`
- `ZALOPAY_KEY1`
- `ZALOPAY_KEY2`
- Optional: `ZALOPAY_CREATE_URL`, `ZALOPAY_QUERY_URL`, `ZALOPAY_CALLBACK_PATH`

## Booking & Fulfillment

- POST `/payment/{paymentId}/booking`
- GET `/payment/{paymentId}/booking`
- POST `/bookings/{bookingId}/update-calendar`
- POST `/bookings/{bookingId}/conversation`
- POST `/bookings/{bookingId}/send-confirmation`

Notes:
- Booking flow is stubbed in `BookingService`; implement DB persistence, calendar writes, and messaging.
- Idempotency: header `Idempotency-Key` is accepted on create payment and booking creation; storage layer TODO.

## Error Model

App uses centralized error handler returning:
```
{ "error": { "code": "ERROR_CODE", "message": "...", "details": {} }, "status_code": 400 }
```

## Frontend Integration Notes

- Amount validation: backend will recompute amount for selected nights; current code returns request amount (TODO to enforce).
- Ownership checks: TODO across winners/offers/payment session resources.
- Sessions/transactions: endpoints exist; persistence layer pending.
- Callback URL: uses `settings.app.host + ZALOPAY_CALLBACK_PATH` if available. Ensure public callback URL matches deployment hostname.
- Rate limiting: not yet applied; consider FastAPI-limiter.
- WebSocket topics: to be integrated into services when states change. 