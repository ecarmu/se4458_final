from fastapi import APIRouter, HTTPException, status, Request
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
import httpx, os

router = APIRouter()

# Pydantic models for request/response
class JobAlertCreate(BaseModel):
    user_id: int
    keywords: List[str]
    location: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    frequency: str = "daily"  # daily, weekly, monthly

class NotificationCreate(BaseModel):
    user_id: int
    title: str
    message: str
    type: str = "info"  # info, success, warning, error
    priority: str = "normal"  # low, normal, high, urgent

class EmailNotification(BaseModel):
    to_email: EmailStr
    subject: str
    body: str
    template: Optional[str] = None

class NotificationResponse(BaseModel):
    id: int
    user_id: int
    title: str
    message: str
    type: str
    priority: str
    is_read: bool = False
    created_at: datetime

class JobAlertResponse(BaseModel):
    id: int
    user_id: int
    query: str
    keywords: List[str]
    location: Optional[str]
    salary_min: Optional[int]
    salary_max: Optional[int]
    frequency: str
    is_active: bool = True
    created_at: datetime

# Job Alerts endpoints
@router.post("/alerts", response_model=JobAlertResponse)
async def create_job_alert(alert_data: JobAlertCreate):
    NOTIFICATION_SERVICE_URL = os.getenv("NOTIFICATION_SERVICE_URL", "http://notification_service:8002")
    
    # Convert to dict and ensure safe access
    data = alert_data.dict()

    
    # Safely get 'query' from keywords
    keywords = data.get("keywords") or []
    data["query"] = keywords[0] if keywords else "GENERIC"

    keywords = data.get("keywords") or []
    query = keywords[0] if keywords else "GENERIC"

    # Now include query in the request payload
    filtered_data = {
        "user_id":    data["user_id"],
        "query":      query,  # Now safe
        "location":   data.get("location"),
        "salary_min": data.get("salary_min"),
        "salary_max": data.get("salary_max"),
        "frequency":  data.get("frequency"),
    }

    print("Sending to notification service:", filtered_data)

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{NOTIFICATION_SERVICE_URL}/api/v1/alerts/",
            json=filtered_data,
            headers={"Content-Type": "application/json"}
        )
        resp.raise_for_status()
        return resp.json()


@router.get("/alerts", response_model=List[JobAlertResponse])
async def get_user_alerts(user_id: int):
    NOTIFICATION_SERVICE_URL = os.getenv("NOTIFICATION_SERVICE_URL", "http://notification_service:8002")
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{NOTIFICATION_SERVICE_URL}/api/v1/alerts", params={"user_id": user_id})
            resp.raise_for_status()
            data = resp.json()
            print("DEBUG downstream data:", data)
            return data
        except httpx.HTTPStatusError as e:
            print("HTTP error from downstream:", e.response.status_code, e.response.text)
            raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
        except Exception as e:
            import traceback
            print("Unexpected error:", traceback.format_exc())
            raise HTTPException(status_code=500, detail=str(e))


@router.put("/alerts/{alert_id}", response_model=JobAlertResponse)
async def update_job_alert(alert_id: int, alert_data: JobAlertCreate):
    """Update an existing job alert"""
    return {
        "id": alert_id,
        "user_id": alert_data.user_id,
        "keywords": alert_data.keywords,
        "location": alert_data.location,
        "salary_min": alert_data.salary_min,
        "salary_max": alert_data.salary_max,
        "frequency": alert_data.frequency,
        "is_active": True,
        "created_at": datetime.now()
    }

@router.delete("/alerts/{alert_id}")
async def delete_job_alert(alert_id: int):
    """Delete a job alert"""
    return {"message": f"Job alert {alert_id} deleted successfully"}

# Notifications endpoints
@router.post("/notifications", response_model=NotificationResponse)
async def create_notification(notification_data: NotificationCreate):
    """Create a new notification for a user"""
    return {
        "id": 1,
        "user_id": notification_data.user_id,
        "title": notification_data.title,
        "message": notification_data.message,
        "type": notification_data.type,
        "priority": notification_data.priority,
        "is_read": False,
        "created_at": datetime.now()
    }

@router.get("/")
async def get_notifications(request: Request):
    #NOTIFICATION_SERVICE_URL = os.getenv("NOTIFICATION_SERVICE_URL", "http://notification_service:8003")
    NOTIFICATION_SERVICE_URL = os.getenv("NOTIFICATION_SERVICE_URL", "http://notification_service:8002")
    params = dict(request.query_params)
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{NOTIFICATION_SERVICE_URL}/api/v1/notifications/", params=params)
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@router.put("/notifications/{notification_id}/read")
async def mark_notification_read(notification_id: int):
    """Mark a notification as read"""
    return {"message": f"Notification {notification_id} marked as read"}

@router.delete("/notifications/{notification_id}")
async def delete_notification(notification_id: int):
    """Delete a notification"""
    return {"message": f"Notification {notification_id} deleted successfully"}

# Email/SMS endpoints
@router.post("/email")
async def send_email(email_data: EmailNotification):
    """Send an email notification"""
    return {
        "message": "Email sent successfully",
        "to": email_data.to_email,
        "subject": email_data.subject
    }

@router.post("/sms")
async def send_sms(phone: str, message: str):
    """Send an SMS notification"""
    return {
        "message": "SMS sent successfully",
        "to": phone,
        "message_length": len(message)
    }

# Bulk operations
@router.post("/notifications/bulk")
async def create_bulk_notifications(notifications: List[NotificationCreate]):
    """Create multiple notifications at once"""
    return {
        "message": f"Created {len(notifications)} notifications",
        "count": len(notifications)
    }

@router.put("/notifications/bulk/read")
async def mark_notifications_read(notification_ids: List[int]):
    """Mark multiple notifications as read"""
    return {
        "message": f"Marked {len(notification_ids)} notifications as read",
        "count": len(notification_ids)
    } 