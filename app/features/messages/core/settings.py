from functools import lru_cache
from decouple import config

@lru_cache
def get_settings():
    return {
        "PUSHER_APP_ID": config("PUSHER_APP_ID", default="2021288"),
        "PUSHER_KEY": config("PUSHER_KEY", default="9e079f4261072a6d7482"),
        "PUSHER_SECRET": config("PUSHER_SECRET", default="9b9447e78cac364ca220"),
        "PUSHER_CLUSTER": config("PUSHER_CLUSTER", default="ap1"),
        "NEXT_PUBLIC_PUSHER_KEY": config("NEXT_PUBLIC_PUSHER_KEY", default="9e079f4261072a6d7482"),
        "NEXT_PUBLIC_PUSHER_CLUSTER": config("NEXT_PUBLIC_PUSHER_CLUSTER", default="ap1")
    }

settings = get_settings()