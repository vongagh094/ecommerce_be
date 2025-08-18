# Payment API Documentation

This document describes the payment API endpoints implemented to support ZaloPay integration, session management, and booking creation.

## Base URL

All endpoints are prefixed with `/api/v1`.

## Authentication

All endpoints require Bearer JWT authentication unless explicitly noted.

## Payment Flow

1. User creates a ZaloPay order via `/payment/zalopay/create`
2. User is redirected to ZaloPay to complete payment
3. ZaloPay calls back to `/payment/zalopay/callback` (server-to-server)
4. User is redirected back to the frontend session page
5. Frontend checks status via WebSocket or `/payment/zalopay/status/{appTransId}`
6. On successful payment, frontend creates booking via `/payment/{paymentId}/booking`

## WebSocket Integration

The backend emits the following WebSocket events:

- `PAYMENT_STATUS`: Sent when payment status changes (INITIATED, PROCESSING, COMPLETED, FAILED)
- `BOOKING_CONFIRMED`: Sent when a booking is confirmed after payment

## Endpoints

### ZaloPay Integration

#### Create ZaloPay Order

- **URL**: `/payment/zalopay/create`
- **Method**: `POST`
- **Auth**: Required
- **Headers**:
  - `Idempotency-Key`: Optional string for idempotent requests
- **Request Body**:
  ```json
  {
    "auctionId": "uuid-string",
    "selectedNights": ["YYYY-MM-DD", "YYYY-MM-DD", ...],
    "amount": 1000000,
    "orderInfo": "Booking for Property Name (2023-10-15 - 2023-10-20)"
  }
  ```
- **Response**: 200 OK
  ```json
  {
    "orderUrl": "https://sbgateway.zalopay.vn/openinapp?...",
    "appTransId": "string",
    "amount": 1000000
  }
  ```
- **Errors**:
  - 400: Validation error (invalid auction, nights, amount mismatch)
  - 401: Authentication required
  - 404: Auction or bid not found
  - 409: Amount mismatch
  - 502: ZaloPay API error

#### Verify Payment Status

- **URL**: `/payment/zalopay/status/{appTransId}`
- **Method**: `GET`
- **Auth**: Required
- **Response**: 200 OK
  ```json
  {
    "status": "PENDING|PAID|FAILED",
    "transactionId": "string",
    "amount": 1000000,
    "paidAt": "2023-10-15T12:34:56Z"
  }
  ```
- **Errors**:
  - 401: Authentication required
  - 403: Forbidden (not owner)
  - 404: Payment session not found
  - 502: ZaloPay API error

#### ZaloPay Callback

- **URL**: `/payment/zalopay/callback`
- **Method**: `POST`
- **Auth**: None (server-to-server)
- **Request Body**: ZaloPay callback payload
- **Response**: 200 OK
  ```json
  {
    "return_code": 1,
    "return_message": "success"
  }
  ```

### Session & Transaction Management

#### Get Payment Session

- **URL**: `/payment/sessions/{sessionId}`
- **Method**: `GET`
- **Auth**: Required
- **Response**: 200 OK
  ```json
  {
    "id": "uuid-string",
    "auctionId": "uuid-string",
    "userId": 123,
    "amount": 1000000,
    "currency": "VND",
    "status": "PENDING|PAID|FAILED",
    "appTransId": "string",
    "orderUrl": "https://sbgateway.zalopay.vn/openinapp?...",
    "createdAt": "2023-10-15T12:34:56Z",
    "expiresAt": "2023-10-15T12:49:56Z"
  }
  ```
- **Errors**:
  - 401: Authentication required
  - 403: Forbidden (not owner)
  - 404: Session not found

#### Get Payment Transaction

- **URL**: `/payment/transactions/{transactionId}`
- **Method**: `GET`
- **Auth**: Required
- **Response**: 200 OK
  ```json
  {
    "id": "uuid-string",
    "sessionId": "uuid-string",
    "appTransId": "string",
    "transactionId": "string",
    "amount": 1000000,
    "status": "PENDING|PAID|FAILED",
    "paidAt": "2023-10-15T12:34:56Z"
  }
  ```
- **Errors**:
  - 401: Authentication required
  - 403: Forbidden (not owner)
  - 404: Transaction not found

### Booking & Fulfillment

#### Create Booking from Payment

- **URL**: `/payment/{paymentId}/booking`
- **Method**: `POST`
- **Auth**: Required
- **Request Body**:
  ```json
  {
    "idempotencyKey": "optional-string"
  }
  ```
- **Response**: 200 OK
  ```json
  {
    "id": "uuid-string",
    "referenceNumber": "BK202310151234-123",
    "propertyId": "123",
    "propertyName": "Beach Villa",
    "hostId": "456",
    "checkIn": "2023-10-15",
    "checkOut": "2023-10-20",
    "guestCount": 1,
    "totalAmount": 1000000,
    "status": "CONFIRMED",
    "createdAt": "2023-10-15T12:34:56Z"
  }
  ```
- **Errors**:
  - 401: Authentication required
  - 403: Forbidden (not owner)
  - 404: Payment not found
  - 409: Payment not completed or dates not available

#### Get Booking for Payment

- **URL**: `/payment/{paymentId}/booking`
- **Method**: `GET`
- **Auth**: Required
- **Response**: 200 OK (same as Create Booking)
- **Errors**:
  - 401: Authentication required
  - 404: Booking not found

#### Update Calendar Availability

- **URL**: `/bookings/{bookingId}/update-calendar`
- **Method**: `POST`
- **Auth**: Required
- **Response**: 200 OK
  ```json
  {}
  ```
- **Errors**:
  - 401: Authentication required
  - 404: Booking not found

#### Create Conversation Thread

- **URL**: `/bookings/{bookingId}/conversation`
- **Method**: `POST`
- **Auth**: Required
- **Response**: 200 OK
  ```json
  {
    "threadId": "uuid-string"
  }
  ```
- **Errors**:
  - 401: Authentication required
  - 404: Booking not found

#### Send Booking Confirmation

- **URL**: `/bookings/{bookingId}/send-confirmation`
- **Method**: `POST`
- **Auth**: Required
- **Response**: 200 OK
  ```json
  {}
  ```
- **Errors**:
  - 401: Authentication required
  - 404: Booking not found

## Database Schema

Two new tables were added to support payment processing:

### payment_sessions

| Column | Type | Description |
|--------|------|-------------|
| id | uuid | Primary key |
| user_id | bigint | User ID (FK to users) |
| auction_id | uuid | Auction ID (FK to auctions) |
| bid_id | uuid | Bid ID (FK to bids) |
| app_trans_id | varchar(64) | ZaloPay app transaction ID |
| amount | integer | Payment amount in VND |
| selected_nights | jsonb | Array of selected night dates |
| status | varchar(50) | PENDING, PAID, FAILED |
| idempotency_key | varchar(128) | Optional idempotency key |
| expires_at | timestamp | Session expiration time |
| order_url | text | ZaloPay order URL |
| created_at | timestamp | Creation timestamp |
| updated_at | timestamp | Last update timestamp |

### payment_transactions

| Column | Type | Description |
|--------|------|-------------|
| id | uuid | Primary key |
| session_id | uuid | FK to payment_sessions |
| app_trans_id | varchar(64) | ZaloPay app transaction ID |
| zp_trans_id | varchar(64) | ZaloPay transaction ID |
| amount | integer | Payment amount in VND |
| status | varchar(50) | PENDING, PAID, FAILED |
| paid_at | timestamp | Payment completion time |
| raw | jsonb | Raw ZaloPay response |
| created_at | timestamp | Creation timestamp |
| updated_at | timestamp | Last update timestamp | 