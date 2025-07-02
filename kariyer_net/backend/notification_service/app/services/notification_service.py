from typing import List, Optional
from sqlalchemy.orm import Session
from ..models.notification import Notification
from ..schemas.notification import NotificationCreate
from ..core.database import get_db
import json

class NotificationService:
    def __init__(self, db: Session):
        self.db = db

    async def create_notification(self, notification: NotificationCreate) -> Notification:
        """Create a new notification"""
        db_notification = Notification(
            user_id=notification.user_id,
            type=getattr(notification, 'type', 'info'),
            title=getattr(notification, 'title', 'Bildirim'),
            message=notification.message,
            data=json.dumps(notification.data) if notification.data else None,
            is_read=False,
            job_id=notification.data.get('job_id') if notification.data else None,
            alert_id=notification.data.get('alert_id') if notification.data else None
        )
        self.db.add(db_notification)
        self.db.commit()
        self.db.refresh(db_notification)
        return db_notification

    async def get_user_notifications(self, user_id: int) -> List[Notification]:
        """Get user's notifications"""
        return self.db.query(Notification).filter(Notification.user_id == user_id).all()

    async def mark_as_read(self, notification_id: int) -> bool:
        """Mark notification as read"""
        # To be implemented
        pass

    async def send_email_notification(self, user_email: str, subject: str, message: str):
        """Send email notification"""
        # To be implemented
        pass 