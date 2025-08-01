import time
import uuid


class RedisRepository:
    def __init__(self, redis_client):
        (self.redis,
         self.max_retry,
         self.expire) = redis_client

    def set(self, key, value, ex=None, nx=True):
        """Set a value in Redis with an optional expiration time."""
        return self.redis.set(key, value, ex=ex, nx=nx)

    def get(self, key):
        """Get a value from Redis."""
        return self.redis.get(key)

    def delete(self, key):
        """Delete a key from Redis."""
        self.redis.delete(key)

    def exists(self, key):
        """Check if a key exists in Redis."""
        return self.redis.exists(key)
    def publish(self, channel, message):
        """Publish a message to a Redis channel."""
        self.redis.publish(channel, message)

