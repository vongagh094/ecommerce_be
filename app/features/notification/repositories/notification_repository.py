from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete, func
from app.db.models.notification import Notification
from app.db.models.subscription import Subscription
from app.features.notification.schemas.NotificationDTO import NotificationDTO, NotificationResponse
from app.features.notification.schemas.SubscriptionDTO import SubscriptionDTO
from typing import List, Tuple

class NotificationRepository:
    def __init__(self, db: Session):
        self.db = db

    async def create_notification(self, notification_dto: NotificationDTO) -> NotificationResponse:
        notification = Notification(
            user_id=notification_dto.user_id,
            title=notification_dto.title,
            message=notification_dto.message,
            link=notification_dto.link,
            is_pushed=notification_dto.is_pushed,
            type=notification_dto.type,
            is_read=False
        )
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        return NotificationResponse.from_orm(notification)

    async def get_notifications(self, user_id: int, page: int, limit: int) -> Tuple[List[NotificationResponse], dict]:
        offset = (page - 1) * limit
        # Count notifications for the specific user
        total_notifications = self.db.execute(
            select(func.count()).select_from(Notification).where(Notification.user_id == user_id)
        ).scalar_one()
        total_pages = (total_notifications + limit - 1) // limit
        # Fetch paginated notifications for the user
        notifications = self.db.execute(
            select(Notification)
            .where(Notification.user_id == user_id)
            .order_by(Notification.created_at.desc())
            .limit(limit)
            .offset(offset)
        ).scalars().all()
        notifications_response = [NotificationResponse.from_orm(n) for n in notifications]
        metadata = {
            "page": page,
            "limit": limit,
            "total_notifications": total_notifications,
            "total_pages": total_pages
        }
        return notifications_response, metadata

    async def mark_as_read(self, notification_id: int) -> NotificationResponse:
        notification = self.db.execute(
            select(Notification).where(Notification.id == notification_id)
        ).scalar_one_or_none()
        if not notification:
            raise ValueError("Notification not found")
        self.db.execute(
            update(Notification)
            .where(Notification.id == notification_id)
            .values(is_read=True)
        )
        self.db.commit()
        self.db.refresh(notification)
        return NotificationResponse.from_orm(notification)

    async def delete_notification(self, notification_id: int) -> bool:
        result = self.db.execute(
            delete(Notification).where(Notification.id == notification_id)
        )
        self.db.commit()
        return result.rowcount > 0

    async def create_subscription(self, subscription_dto: SubscriptionDTO) -> SubscriptionDTO:
        subscription = Subscription(
            user_id=subscription_dto.user_id,
            endpoint=subscription_dto.endpoint,
            p256dh=subscription_dto.p256dh,
            auth=subscription_dto.auth
        )
        self.db.add(subscription)
        self.db.commit()
        self.db.refresh(subscription)
        return SubscriptionDTO.from_orm(subscription)
    
    async def delete_subscription(self, subscription_id: int) -> bool:
        result = self.db.execute(
            delete(Subscription).where(Subscription.id == subscription_id)
        )
        self.db.commit()
        return result.rowcount > 0

    async def delete_subscription_by_endpoint(self, endpoint: str) -> bool:
        result = self.db.execute(
            delete(Subscription).where(Subscription.endpoint == endpoint)
        )
        self.db.commit()
        return result.rowcount > 0