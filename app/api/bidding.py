from fastapi import APIRouter, Depends
from app.schemas.BidDTO import BidsDTO
from app.core.container import Container
from dependency_injector.wiring import inject, Provide
from app.services.bid_service import BidService
from app.services.auction_service import AuctionService
from rstream import (
    AMQPMessage,
    MessageContext
)
import json
from app.services.rabbitMQ_service import RabbitMQService
# Use APIRouter instead of FastAPI app
bidding = APIRouter(
    tags=["bidings"],
    responses={404: {"description": "Not found"}}
)
@inject
async def call_back(msg:AMQPMessage,
                    message_context:MessageContext,
                    bid_service: BidService = Depends(Provide[Container.bid_service]),
                    auction_service: AuctionService = Depends(Provide[Container.auction_service]),
                    redis_service=Depends(Provide[Container.redis_service])
                    ):
    try:
        data_str = msg.body.decode("utf-8")
        try:
            # Load JSON from dict
            bid_data = json.loads(data_str)
        except Exception as e:
            print (f"Error decoding json: {e}")
            return None

        #update Db bid
        saved_bid = bid_service.place_bids(bid_data)
        #update auction the current highest bid
        if saved_bid:
            auction_service.update_highest_bid(bid_data.get("auction_id"),
                                               bid_data.get("bid_amount"))

            # Update the highest bid in redis
            redis_service.publication_lock(
                bid_data.get("auction_id"),
                doSomeThing= lambda: redis_service.update_highest_bid(
                    channel="bid_updates",
                    auction_id=bid_data.get("auction_id"),
                    current_bid=bid_data.get("bid_amount")
                )
            )
    except Exception as e:
        print(f"Error in updating db: {e}")
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

