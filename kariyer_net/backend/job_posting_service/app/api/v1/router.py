from fastapi import APIRouter
from .endpoints import jobs, admin

api_router = APIRouter()

# Include all endpoint modules
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"]) 