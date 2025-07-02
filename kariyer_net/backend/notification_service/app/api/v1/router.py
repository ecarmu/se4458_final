from fastapi import APIRouter
from .endpoints import alerts, notifications

api_router = APIRouter()

# Include all endpoint modules
api_router.include_router(alerts.router, prefix="/alerts", tags=["alerts"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["notifications"]) 