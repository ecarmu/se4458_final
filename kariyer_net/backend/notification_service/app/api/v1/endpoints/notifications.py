from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from ....core.database import get_db
from ....schemas.notification import NotificationResponse
from ....services.notification_service import NotificationService
import json

router = APIRouter()

def get_notification_service(db: Session = Depends(get_db)) -> NotificationService:
    return NotificationService(db)

@router.get("/", response_model=List[NotificationResponse])
async def get_user_notifications(
    user_id: int,
    notification_service: NotificationService = Depends(get_notification_service)
):
    notifications = await notification_service.get_user_notifications(user_id)
    # Parse data field from JSON string to dict
    for n in notifications:
        if isinstance(n.data, str):
            try:
                n.data = json.loads(n.data)
            except Exception:
                n.data = {}
    return notifications

@router.post("/mark-read")
async def mark_notification_read(
    notification_id: int,
    notification_service: NotificationService = Depends(get_notification_service)
):
    return {"message": "Mark read endpoint - to be implemented"}