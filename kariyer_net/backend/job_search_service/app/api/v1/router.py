from fastapi import APIRouter
from .endpoints import search, filters

api_router = APIRouter()

# Include all endpoint modules
api_router.include_router(search.router, tags=["search"])
api_router.include_router(filters.router, prefix="/filters", tags=["filters"]) 