from functools import lru_cache
import os
from dotenv import load_dotenv

load_dotenv()

@lru_cache
def get_settings():
    return {
        "PUSHER_APP_ID": os.getenv("PUSHER_APP_ID"),
        "PUSHER_KEY": os.getenv("PUSHER_KEY"),
        "PUSHER_SECRET": os.getenv("PUSHER_SECRET"),
        "PUSHER_CLUSTER": os.getenv("PUSHER_CLUSTER"),
        "NEXT_PUBLIC_PUSHER_KEY": os.getenv("NEXT_PUBLIC_PUSHER_KEY"),
        "NEXT_PUBLIC_PUSHER_CLUSTER": os.getenv("NEXT_PUBLIC_PUSHER_CLUSTER")
    }

settings = get_settings()