from fastapi import APIRouter, Depends
from app.core.container import Container
from dependency_injector.wiring import inject, Provide
from app.features.messages.services.pusher_service import PusherService
from app.features.messages.schemas.PusherDTO import PusherConfigResponse

router = APIRouter()

@router.get("/get", response_model=PusherConfigResponse, operation_id="getPusherConfig")
@inject
async def get_pusher_config(
    pusher_service: PusherService = Depends(Provide[Container.pusher_service])
):
    return pusher_service.get_pusher_config()