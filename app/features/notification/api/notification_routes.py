from fastapi import APIRouter, Depends, HTTPException
from app.features.notification.services.notification_service import NotificationService
from app.features.notification.schemas.NotificationDTO import NotificationDTO, NotificationResponse
from app.features.notification.schemas.SubscriptionDTO import SubscriptionDTO
from app.features.notification.core.settings import get_notification_service
from typing import List, Dict

router = APIRouter(tags=["Notifications"])

@router.post("/create", response_model=NotificationResponse)
async def create_notification(
    notification_dto: NotificationDTO,
    service: NotificationService = Depends(get_notification_service)
):
    return await service.save_notification(notification_dto)

@router.get("/list", response_model=Dict[str, List[NotificationResponse] | Dict])
async def get_notifications(
    user_id: int,
    page: int = 1,
    limit: int = 5,
    service: NotificationService = Depends(get_notification_service)
):
    notifications, metadata = await service.get_notifications(user_id, page, limit)
    return {"notifications": notifications, "metadata": metadata}

@router.put("/read")
async def mark_as_read(
    notification_id: int,
    service: NotificationService = Depends(get_notification_service)
):
    return await service.mark_as_read(notification_id)

@router.delete("/delete")
async def delete_notification(
    notification_id: int,
    service: NotificationService = Depends(get_notification_service)
):
    success = await service.delete_notification(notification_id)
    if not success:
        raise HTTPException(status_code=404, detail="Notification not found")
    return {"message": "Notification deleted"}

@router.post("/subscribe", response_model=SubscriptionDTO)
async def create_subscription(
    subscription_dto: SubscriptionDTO,
    service: NotificationService = Depends(get_notification_service)
):
    return await service.save_subscription(subscription_dto)

@router.delete("/unsubscribe")
async def delete_subscription(
    endpoint: str,
    service: NotificationService = Depends(get_notification_service)
):
    success = await service.delete_subscription_by_endpoint(endpoint)
    if not success:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return {"message": "Subscription deleted"}