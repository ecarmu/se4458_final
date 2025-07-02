from fastapi import APIRouter
from .endpoints import chat

api_router = APIRouter()

# Include all endpoint modules with /ai_agent prefix
api_router.include_router(chat.router, prefix="/ai_agent", tags=["ai_agent"]) 