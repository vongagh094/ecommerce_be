from rstream import (
    Producer,
    AMQPMessage,
    ConfirmationStatus,
    Consumer,
    MessageContext,
    amqp_decoder,
    ConsumerOffsetSpecification,
    OffsetType
)
from app.schemas.BidDTO import BidsDTO
import json

class RabbitMQService:
    def __init__(self, stream_property: dict):
        self.stream_property = stream_property

    async def on_publish_confirm(self,status: ConfirmationStatus):
        if status.is_confirmed:
            return print("publish confirm")
        return print("on confirm completed")

    async def use_producer(self, bid_data: BidsDTO, on_publish_confirm= None):
        """Create a RabbitMQ producer."""

        if on_publish_confirm is None:
            on_publish_confirm = self.on_publish_confirm
        try:
            async with Producer(
                self.stream_property["host"],
                username=self.stream_property["username"],
                password=self.stream_property["password"]
            ) as producer:
                await producer.create_stream(
                    self.stream_property["stream_name"],
                    exists_ok=True,
                    arguments={"max-length-bytes": self.stream_property["stream_retention"]}
                )
                amqp_message = AMQPMessage(
                    body=bid_data.model_dump_json().encode("utf-8")
                )
                await producer.send(
                    stream=self.stream_property["stream_name"],
                    message=amqp_message,
                    on_publish_confirm=lambda status: on_publish_confirm(status)
                )
        except Exception as e:
            # Handle exception (add your logic here)
            print(f"Error sending bid data: {e}")
            return {"error": "Failed to send bid data"}

    async def call_back(self,msg: AMQPMessage,message_context: MessageContext):
        try:
            data_str = msg.body.decode("utf-8")
            try:
                # Load JSON from dict
                bid_data = json.loads(data_str)
            except Exception as e:
                print(f"Error decoding json: {e}")
                return None
        except Exception as e:
            print(f"Error in updating db: {e}")
            await message_context.consumer.close()
            return None
        return print(f"receive the message {bid_data}")

    async def use_consumer(self, callback=None):
        """Create a RabbitMQ consumer."""
        if callback is None:
            callback = self.call_back
        consumer = Consumer(
            self.stream_property["host"],
            username=self.stream_property["username"],
            password=self.stream_property["password"]
        )
        await consumer.create_stream(
            self.stream_property["stream_name"],
            exists_ok=True,
            arguments={"max-length-bytes": self.stream_property["stream_retention"]}
        )

        try:
            await consumer.start()
            await consumer.subscribe(
                stream=self.stream_property["stream_name"],
                callback=callback,
                decoder=amqp_decoder,
                offset_specification=ConsumerOffsetSpecification(OffsetType.LAST)
            )
            await consumer.run()
        except Exception as e:
            try:
                await consumer.close()
            except Exception as close_error:
                print(f"Error closing consumer: {close_error}")
            print(f"Error in consumer: {e}")