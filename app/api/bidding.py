from fastapi import APIRouter, Depends
from app.schemas.BidDTO import BidsDTO
from app.core.container import Container
from dependency_injector.wiring import inject, Provide
from app.services.bid_service import BidService
from app.services.calendar_service import CalendarService
from rstream import (
    AMQPMessage,
    MessageContext
)
import json
from app.services.rabbitMQ_service import RabbitMQService
from datetime import datetime as dt
# Use APIRouter instead of FastAPI app
bidding = APIRouter(
    tags=["bidings"],
    responses={404: {"description": "Not found"}}
)

@inject
async def call_back(msg: AMQPMessage,
                    message_context: MessageContext,
                    bid_service: BidService = Depends(Provide[Container.bid_service]),
                    calendar_service: CalendarService = Depends(Provide[Container.calendar_service])  # ADD THIS
                    ):
    """
    FIXED CALLBACK:
    1. Insert/Update bid in bids table
    2. Update calendar_availability table with highest bid
    3. FE polling will see updated data immediately
    """
    try:
        data_str = msg.body.decode("utf-8")
        try:
            bid_data = json.loads(data_str)
        except Exception as e:
            print(f"Error decoding json: {e}")
            return None

        # === STEP 1: CREATE BidsDTO ===
        try:
            current_time = dt.now().isoformat()

            bids_dto = BidsDTO(
                user_id=int(bid_data.get("user_id")),
                property_id=int(bid_data.get("property_id", 0)),
                auction_id=str(bid_data.get("auction_id")),
                bid_amount=int(bid_data.get("bid_amount")),
                bid_time=bid_data.get("bid_time", current_time),
                check_in=bid_data.get("check_in"),
                check_out=bid_data.get("check_out"),
                allow_partial=bool(bid_data.get("allow_partial", True)),
                partial_awarded=bool(bid_data.get("partial_awarded", False)),
                created_at=bid_data.get("created_at", current_time)
            )
        except Exception as e:
            print(f"Error creating BidsDTO: {e}")
            return None

        # === STEP 2: INSERT/UPDATE BID ===
        result = bid_service.place_bid(bids_dto)

        if result.get("success"):
            bid_id = result.get("bid_id")
            action = result.get("action")  # "created" or "updated"

            print(f"✅ Bid {action}: {bid_id}")
            print(f"   User: {bids_dto.user_id}")
            print(f"   Property: {bids_dto.property_id}")
            print(f"   Auction: {bids_dto.auction_id}")
            print(f"   Total Amount: {result.get('total_amount')}")
            print(f"   Price/Night: {result.get('price_per_night')}")

            # === STEP 3: UPDATE CALENDAR_AVAILABILITY ===
            try:
                # Create mock bid record object for calendar service
                from collections import namedtuple
                from datetime import datetime

                BidRecord = namedtuple('BidRecord', ['id', 'check_in', 'check_out', 'price_per_night'])

                bid_record = BidRecord(
                    id=bid_id,
                    check_in=datetime.fromisoformat(bids_dto.check_in).date(),
                    check_out=datetime.fromisoformat(bids_dto.check_out).date(),
                    price_per_night=result.get('price_per_night')
                )

                # Update calendar with new bid
                updated_dates = calendar_service.update_calendar_with_new_bid(
                    property_id=bids_dto.property_id,
                    bid_record=bid_record
                )

                if updated_dates:
                    print(f"📅 Calendar updated for dates: {updated_dates}")
                    print(f"   → FE polling will see new highest bids!")
                else:
                    print(f"📅 Calendar not updated (bid not highest)")

            except Exception as e:
                print(f"⚠️ Calendar update failed (non-critical): {e}")
                # Don't fail the whole process if calendar update fails

        else:
            print(f"❌ Bid failed: {result.get('message')}")

    except Exception as e:
        print(f"Error in callback: {e}")
    finally:
        await message_context.consumer.close()

    return "call back complete"
# producers to send a bid
@bidding.post("/sending_bid", tags=["bidings"])
@inject
async def sending_bid(
        bid: BidsDTO,
        rabbitMQ_service:RabbitMQService = Depends(Provide[Container.rabbitMQStream_service]) ,
    ):
     return await rabbitMQ_service.use_producer(bid)

# API travel the message from the stream 
@bidding.get("/receiving_bid", tags=["bidings"])
@inject
async def receiving_bid(
        rabbitmq_service: RabbitMQService = Depends(Provide[Container.rabbitMQStream_service]),
    ):
        return await rabbitmq_service.use_consumer(callback=call_back)

