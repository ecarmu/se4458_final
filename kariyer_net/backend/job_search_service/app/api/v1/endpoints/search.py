from fastapi import APIRouter, Depends, Query
from motor.motor_asyncio import AsyncIOMotorClient
from ....services.search_service import SearchService
from ....dto.search_dto import SearchDTO
from typing import List, Optional

router = APIRouter()

# Dependency to get MongoDB client (to be implemented in your core/database.py)
def get_mongo_client():
    from ....core.database import db
    return db.client

@router.get("/search", response_model=dict)
async def search_jobs(
    query: str = Query(""),
    location: Optional[str] = None,
    work_mode: Optional[str] = None,
    date_filter: Optional[str] = None,
    country: Optional[str] = None,
    city: Optional[str] = None,
    district: Optional[str] = None,
    user_id: Optional[int] = None,
    page: int = 1,
    limit: int = 10,
    db: AsyncIOMotorClient = Depends(get_mongo_client),
    search_service: SearchService = Depends()
):
    """Search for jobs with comprehensive filtering and pagination support."""
    print(f"[DEBUG] /search called with: query={query}, location={location}, work_mode={work_mode}, date_filter={date_filter}, country={country}, city={city}, district={district}, user_id={user_id}, page={page}, limit={limit}")
    skip = (page - 1) * limit
    
    # Build search DTO with all filters
    search_dto = SearchDTO(
        query=query, 
        location=location,
        work_mode=work_mode,
        date_filter=date_filter,
        country=country,
        city=city,
        district=district
    )
    
    results = await search_service.search_jobs(db, search_dto, skip=skip, limit=limit)
    total_results = await search_service.get_total_count(db, search_dto)
    total_pages = (total_results + limit - 1) // limit
    
    if user_id is not None:
        print(f"[DEBUG] Calling save_search_history for user_id={user_id} with query={query}")
        await search_service.save_search_history(db, user_id, search_dto, results_count=len(results))
    
    return {
        "jobs": results,
        "total_results": total_results,
        "total_pages": total_pages,
        "current_page": page,
        "limit": limit
    }

@router.get("/search/suggestions", response_model=List[str])
async def autocomplete(
    query: str = Query(...),
    search_service: SearchService = Depends()
):
    """Get autocomplete suggestions for job search"""
    return await search_service.get_search_suggestions(query)

@router.get("/search/history", response_model=List[dict])
async def recent_searches(
    user_id: int = Query(...),
    limit: int = Query(10),
    db: AsyncIOMotorClient = Depends(get_mongo_client),
    search_service: SearchService = Depends()
):
    """Get recent search history for a user"""
    return await search_service.get_user_search_history(db, user_id, limit=limit)

@router.delete("/search/history", response_model=dict)
async def delete_search_history(
    user_id: int = Query(...),
    db: AsyncIOMotorClient = Depends(get_mongo_client),
    search_service: SearchService = Depends()
):
    """Delete all search history for a user"""
    deleted_count = await search_service.delete_user_search_history(db, user_id)
    return {"deleted_count": deleted_count} 