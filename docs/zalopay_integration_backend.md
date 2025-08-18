sequenceDiagram
    participant Frontend as Next.js Frontend
    participant Backend as FastAPI Backend
    participant ZaloPay as ZaloPay Gateway

    Frontend->Backend: Request to create order<br>(amount, internal order_id)
    activate Backend

    Backend->Backend: Generate app_trans_id (yymmdd_YOUR_ORDER_ID)<br>Generate app_time (Unix milliseconds)
    Backend->Backend: Construct ZaloPay Create Order payload<br>(app_id, app_trans_id, app_user, app_time, amount, item, embed_data, description, bank_code, callback_url)
    Backend->Backend: Generate HMAC-SHA256 signature (mac) using key1
    Backend->ZaloPay: POST /v2/create<br>(signed Create Order payload)
    activate ZaloPay

    ZaloPay->ZaloPay: Validate request and signature
    ZaloPay->Backend: Response (JSON with order_url)
    deactivate ZaloPay

    Backend->Frontend: order_url
    deactivate Backend

    Frontend->ZaloPay: Redirect user's browser to order_url
    activate ZaloPay

    ZaloPay->ZaloPay: User interacts with ZaloPay Gateway to complete payment

    ZaloPay->Backend: Asynchronous POST to callback_url<br>(data string, mac)
    activate Backend

    Backend->Backend: Parse data string and mac
    Backend->Backend: Verify HMAC-SHA256 signature of data string using key2 against received mac
    alt Signature Verification Fails
        Backend->ZaloPay: HTTP 400 (Cease processing)
    else Signature Verification Succeeds
        Backend->Backend: Parse data string, check return_code (1 for success)
        Backend->Backend: Find order using app_trans_id
        Backend->Backend: Update internal order status (e.g., PAID)
        Backend->Backend: Trigger order fulfillment
        Backend->ZaloPay: JSON response {"return_code": 1, "return_message": "success"} (Acknowledge receipt)
    end
    deactivate Backend

    ZaloPay->Frontend: Redirect user's browser to Redirect URL<br>(often with preliminary status query parameters)
    activate Frontend

    Frontend->Frontend: Parse redirect parameters (DO NOT TRUST FOR STATUS)
    Frontend->Backend: Request verified order status<br>(GET /api/zalopay/status/{app_trans_id})
    activate Backend

    Backend->Backend: Construct ZaloPay Query Order Status payload<br>(app_id, app_trans_id, app_time)
    Backend->Backend: Generate HMAC-SHA256 signature (mac) using key1 (app_id|app_trans_id|key1)
    Backend->ZaloPay: POST /v2/query<br>(signed Query Order Status payload)
    activate ZaloPay

    ZaloPay->Backend: Response (JSON with definitive status)
    deactivate ZaloPay

    Backend->Frontend: Verified order status
    deactivate Backend

    Frontend->Frontend: Display appropriate message to user based on verified status
    deactivate Frontend

    Backend->Backend: Background job (scheduled task) periodically queries status of PENDING orders using /v2/query (Failsafe)



    ZaloPay Integration: Backend Technical Documentation (FastAPI)
1. Overview
This document outlines the backend responsibilities and implementation details for integrating the ZaloPay Payment Gateway into our application using FastAPI. The backend's primary roles are to securely communicate with the ZaloPay API, manage the lifecycle of a transaction, handle sensitive credentials, and provide secure endpoints for the frontend.

Core Responsibilities:

Securely store and use ZaloPay API credentials (app_id, key1, key2).

Create payment orders with ZaloPay by sending signed requests.

Provide an endpoint for the frontend to initiate a payment and receive a ZaloPay order_url.

Receive and validate asynchronous callbacks (webhooks) from ZaloPay to get the authoritative transaction status.

Provide a secure endpoint for the frontend to query the status of a transaction.

Update the application's database with the final transaction status.

2. Setup and Configuration
2.1. Credentials
You will receive three credentials from ZaloPay after completing the business registration process. These must be stored securely as environment variables, not hardcoded in the application.

ZALOPAY_APP_ID: Your application's public identifier.

ZALOPAY_KEY1: Secret Key. Used for signing outgoing requests to ZaloPay (e.g., creating an order).

ZALOPAY_KEY2: Secret Key. Used for verifying the signature of incoming callbacks from ZaloPay.

2.2. API Endpoints
The application must be configured to use the correct ZaloPay endpoints for the target environment.

Operation

Environment

Endpoint URL

Create Order

Sandbox

https://sb-openapi.zalopay.vn/v2/create

Create Order

Production

https://openapi.zalopay.vn/v2/create

Query Order Status

Sandbox

https://sb-openapi.zalopay.vn/v2/query

Query Order Status

Production

https://openapi.zalopay.vn/v2/query

3. Backend-Exposed APIs
The backend will expose the following endpoints for frontend consumption and receive callbacks from ZaloPay.

3.1. POST /api/payment/create
This endpoint is called by the frontend to initiate a payment. It orchestrates the creation of an order with ZaloPay and returns the payment URL.

Purpose: To create a ZaloPay transaction and get a redirect URL for the user.

Request Body from Frontend:

{
    "amount": 50000,
    "order_info": "Payment for Order #12345"
}

Response Body to Frontend:

{
    "order_url": "https://sbgateway.zalopay.vn/openinapp?order=..."
}

Internal Logic:

Receive the amount and order_info from the frontend.

Generate a unique transaction ID for our system. This ID is critical and must follow ZaloPay's format: yymmdd_unique_string. For example: 250816_order12345.

Construct the request payload for ZaloPay's /v2/create API.

app_id: Your App ID.

app_trans_id: The unique ID you just generated (e.g., 250816_order12345).

app_user: The user's ID in our system.

app_time: Current Unix timestamp in milliseconds.

amount: The order amount.

item: A JSON string of the items. Can be "" if not applicable.

embed_data: A JSON string for merchant data. Use "{}" if empty.

description: The order_info received from the frontend.

Generate the mac Signature:

Create the hmac_input string by concatenating the following fields with |:
f"{app_id}|{app_trans_id}|{app_user}|{amount}|{app_time}|{embed_data}|{item}"

Sign this string using key1 with the HMAC-SHA256 algorithm.

Add the generated mac to the request payload.

Send a POST request to the ZaloPay "Create Order" endpoint.

If successful, ZaloPay returns a JSON response with an order_url.

Return this order_url to the frontend.

Store the new order in the database with a PENDING status.

3.2. POST /api/payment/callback
This is the webhook endpoint that ZaloPay will call to notify our server of the final transaction result. This endpoint is NOT called by our frontend.

Purpose: To receive the authoritative payment status from ZaloPay.

Request Body from ZaloPay:

{
    "data": "{\"app_id\":553,\"app_trans_id\":\"...\",\"status\":1,...}",
    "mac": "a1b2c3d4..."
}

Internal Logic:

Receive the raw POST request from ZaloPay.

Parse the JSON to get the data (string) and mac (string).

CRITICAL: Verify the Signature.

Calculate your own HMAC-SHA256 signature of the data string using key2.

Compare your calculated signature with the mac received from ZaloPay.

If they do not match, return an HTTP 400 error immediately and stop processing. This is a potential fraudulent request.

If the signature is valid, parse the data string into a JSON object.

Check the return_code within the data object. A value of 1 indicates success.

Use the app_trans_id from the data object to find the order in our database.

Update the order status (e.g., to PAID or FAILED).

Trigger any necessary post-payment business logic (e.g., order fulfillment).

Respond to ZaloPay: To acknowledge receipt, you must return the following JSON. Failure to do so may cause ZaloPay to retry the callback.

{
    "return_code": 1,
    "return_message": "success"
}

3.3. GET /api/payment/status/{app_trans_id}
This endpoint allows the frontend to securely poll for the transaction status. This is necessary because the user's browser redirect is not a secure confirmation of payment.

Purpose: To provide the frontend with the verified status of an order.

URL Parameter: app_trans_id (The transaction ID our system generated).

Response Body to Frontend:

{
    "status": "PAID" // or "PENDING", "FAILED"
}

Internal Logic:

Receive the app_trans_id from the request.

Look up the order in our database.

Return the current status of the order from our database.

(Optional Failsafe): If the status is still PENDING after a certain time, you can implement logic here to proactively call ZaloPay's "Query Order Status" API to get an update. The mac signature for the Query API has a different format: f"{app_id}|{app_trans_id}|{key1}", signed with key1.

4. Coordination and Data Contracts
Backend's Promise: The backend will provide the three endpoints detailed above (/create, /callback, /status).

Frontend's Responsibility: The frontend will call /create to start the payment and /status to verify the result.

Single Source of Truth: The final status of any order is determined only by the data received and verified through the /api/payment/callback endpoint or a proactive status query. The frontend must rely on the /api/payment/status endpoint for this information.