from fastapi import APIRouter
from .endpoints import jobs, auth, notifications, ai_agent

api_router = APIRouter()

# Include all endpoint modules
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["notifications"])
api_router.include_router(ai_agent.router, prefix="/ai_agent", tags=["ai_agent"]) 