from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from ....core.database import get_database
from ....services.search_service import SearchService

router = APIRouter()

@router.get("/filters/cities")
async def get_cities(
    db = Depends(get_database),
    search_service: SearchService = Depends()
):
    """Get available cities for filtering"""
    return {"message": "Get cities endpoint - to be implemented"}

@router.get("/filters/companies")
async def get_companies(
    db = Depends(get_database),
    search_service: SearchService = Depends()
):
    """Get available companies for filtering"""
    return {"message": "Get companies endpoint - to be implemented"} 