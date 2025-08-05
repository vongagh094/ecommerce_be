from pydantic import BaseModel

class PusherConfigResponse(BaseModel):
    app_key: str
    cluster: str