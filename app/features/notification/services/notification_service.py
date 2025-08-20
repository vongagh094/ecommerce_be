from fastapi import HTTPException
from sqlalchemy import select, delete
from app.features.notification.repositories.notification_repository import NotificationRepository
from app.features.notification.schemas.NotificationDTO import NotificationDTO, NotificationResponse
from app.features.notification.schemas.SubscriptionDTO import SubscriptionDTO
from app.db.models.subscription import Subscription
from typing import List, Tuple
from pywebpush import webpush, WebPushException
from app.features.notification.core.config import VAPID_PRIVATE_KEY
import json
import logging

logger = logging.getLogger(__name__)

class NotificationService:
    def __init__(self, repo: NotificationRepository):
        self.repo = repo

    async def save_notification(self, notification_dto: NotificationDTO) -> NotificationResponse:
        try:
            notification = await self.repo.create_notification(notification_dto)
            if notification_dto.is_pushed:
                await self.send_push_notification(notification)
            return notification
        except Exception as e:
            logger.error(f"Failed to save notification: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to save notification: {str(e)}")

    async def send_push_notification(self, notification: NotificationResponse):
        try:
            # Retrieve all subscriptions for the user
            subscriptions = self.repo.db.execute(
                select(Subscription).where(Subscription.user_id == notification.user_id)
            ).scalars().all()

            if not subscriptions:
                logger.warning(f"No subscriptions found for user_id: {notification.user_id}")
                return

            # Prepare the push notification payload
            payload = {
                "title": notification.title,
                "body": notification.message,
                "icon": "/images/logo.png",
                "url": notification.link or "/dashboard/notifications"
            }

            # Send push notification to each subscription
            for subscription in subscriptions:
                subscription_info = {
                    "endpoint": subscription.endpoint,
                    "keys": {
                        "p256dh": subscription.p256dh,
                        "auth": subscription.auth
                    }
                }
                try:
                    webpush(
                        subscription_info=subscription_info,
                        data=json.dumps(payload),
                        vapid_private_key=VAPID_PRIVATE_KEY,
                        vapid_claims={"sub": "mailto:support@example.com"}
                    )
                    logger.info(f"Push notification sent to endpoint: {subscription.endpoint}")
                except WebPushException as e:
                    logger.error(f"Failed to send push notification to {subscription.endpoint}: {str(e)}")
                    if e.response and e.response.status_code in [404, 410]:
                        # Subscription is no longer valid, delete it
                        await self.repo.db.execute(
                            delete(Subscription).where(Subscription.id == subscription.id)
                        )
                        self.repo.db.commit()
                        logger.info(f"Deleted invalid subscription: {subscription.id}")

        except Exception as e:
            logger.error(f"Error sending push notification: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to send push notification: {str(e)}")

    async def get_notifications(self, user_id: int, page: int, limit: int) -> Tuple[List[NotificationResponse], dict]:
        if page < 1 or limit < 1:
            raise HTTPException(status_code=400, detail="Invalid page or limit")
        if user_id < 1:
            raise HTTPException(status_code=400, detail="Invalid user_id")
        try:
            notifications, metadata = await self.repo.get_notifications(user_id, page, limit)
            return notifications, metadata
        except Exception as e:
            logger.error(f"Failed to fetch notifications: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to fetch notifications: {str(e)}")

    async def mark_as_read(self, notification_id: int) -> NotificationResponse:
        try:
            return await self.repo.mark_as_read(notification_id)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            logger.error(f"Failed to mark notification as read: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to mark as read: {str(e)}")

    async def delete_notification(self, notification_id: int) -> bool:
        try:
            return await self.repo.delete_notification(notification_id)
        except Exception as e:
            logger.error(f"Failed to delete notification: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to delete notification: {str(e)}")

    async def save_subscription(self, subscription_dto: SubscriptionDTO) -> SubscriptionDTO:
        try:
            return await self.repo.create_subscription(subscription_dto)
        except Exception as e:
            logger.error(f"Failed to save subscription: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to save subscription: {str(e)}")
        
    async def delete_subscription(self, subscription_id: int) -> bool:
        try:
            return await self.repo.delete_subscription(subscription_id)
        except Exception as e:
            logger.error(f"Failed to delete subscription: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to delete subscription: {str(e)}")
        
    async def delete_subscription_by_endpoint(self, endpoint: str) -> bool:
        try:
            return await self.repo.delete_subscription_by_endpoint(endpoint)
        except Exception as e:
            logger.error(f"Failed to delete subscription by endpoint: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to delete subscription by endpoint: {str(e)}")