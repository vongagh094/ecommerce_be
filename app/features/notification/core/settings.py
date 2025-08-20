from fastapi import Depends
from sqlalchemy.orm import Session
from app.features.notification.repositories.notification_repository import NotificationRepository
from app.features.notification.services.notification_service import NotificationService
from app.db.sessions.session import get_db_session

def get_notification_repository(db: Session = Depends(get_db_session)) -> NotificationRepository:
    return NotificationRepository(db)

def get_notification_service(repo: NotificationRepository = Depends(get_notification_repository)) -> NotificationService:
    return NotificationService(repo)