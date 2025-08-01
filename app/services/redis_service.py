import json

from app.db.repositories.redis_repository import RedisRepository
import uuid
import time

class RedisService:
    def __init__(self, redis_repository: RedisRepository):
        """Initialize the RedisService with a Redis repository."""
        self.redis_repository = redis_repository
        self.max_retry = redis_repository.max_retry
        self.expire = redis_repository.expire

    def publish_message(self, channel: str, message: str) -> bool:
        """Publish a message to a Redis channel."""
        try:
            self.redis_repository.publish(channel, message)
            print(f"Message published to {channel}: {message}")
            return True
        except Exception as e:
            print(f"Error publishing message: {e}")
            return False
    def get_highest_bid(self, auction_id: str) -> float:
        """Get the highest bid for an auction from Redis."""
        try:
            highest_bid = self.redis_repository.get(auction_id)
            if highest_bid is not None:
                return float(highest_bid)
            return 0.0
        except Exception as e:
            print(f"Error getting highest bid: {e}")
            return 0.0
    def set_highest_bid(self, auction_id: str, highest_bid: float) -> None:
        """Set the highest bid for an auction in Redis."""
        try:
            self.redis_repository.set(auction_id, highest_bid)
            print(f"Highest bid for {auction_id} set to {highest_bid}")
        except Exception as e:
            print(f"Error setting highest bid: {e}")
    def publication_lock(self, key: str, value=None, expire=None, doSomeThing=None) -> bool:
        """Acquire a lock in Redis for publication."""

        if self.expire is None:
            expire = self.expire
        if value is None:
            value = gen_lock_value()
        if doSomeThing is None:
            raise Exception("Missing doSomeThing callback")
        lock_key = f"lock:{key}"
        retry_count = 0
        while retry_count < self.max_retry:
            got_lock = self.redis_repository.set(lock_key, value, ex=expire, nx=True)
            if got_lock:
                try:
                    if doSomeThing:
                        doSomeThing()
                    return True
                finally:
                    if self.redis_repository.get(lock_key) == value.encode():
                        self.redis_repository.delete(lock_key)
                return True
                break
            else:
                retry_count += 1
                print(f"Lock busy, retrying {retry_count}/{self.max_retry}...")
                time.sleep(0.2)  # Wait before retry
        return False
    def update_highest_bid(self, channel:str ,auction_id: str, current_bid: int) -> bool:
        try:
            highest_bid = float(self.redis_repository.get(auction_id).decode("utf-8"))
            if current_bid > highest_bid:
                self.redis_repository.publish(channel,
                                              json.dumps({"auction_id":auction_id,
                                                        "current_bid":current_bid}))
                print (self.redis_repository.set(auction_id, current_bid))
            else:
                print(f"Bid {current_bid} is not higher than current highest {highest_bid}")
                return False
        except Exception as e:
            print(f"Error updating highest bid redis service: {e}")
            return False
        return True
def gen_lock_value() -> str:
    """Generate a unique lock value."""
    return str(uuid.uuid4())
def doSomeThing():
    """A placeholder function to demonstrate functionality."""
    return print("Doing something in RedisRepository.")
        # You can add more logic here as needed.
