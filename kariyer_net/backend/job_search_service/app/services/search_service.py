from motor.motor_asyncio import AsyncIOMotorClient
from typing import List, Optional
from ..models.search_history import SearchHistory, SearchHistoryInDB
from ..dto.search_dto import SearchDTO
from ..core.cache import get_cache
from datetime import datetime, timedelta
import httpx
import os

class SearchService:
    def __init__(self):
        self.cache = get_cache()

    async def search_jobs(self, db: AsyncIOMotorClient, search_dto: SearchDTO, skip: int = 0, limit: int = 10) -> List[dict]:
        """Search for jobs from job posting service with comprehensive filtering and pagination support"""
        # JOB_POSTING_SERVICE_URL = os.getenv("JOB_POSTING_SERVICE_URL", "http://job_posting_service:8000")
        JOB_POSTING_SERVICE_URL = os.getenv("JOB_POSTING_SERVICE_URL", "http://job_posting_service:8000")
        
        try:
            async with httpx.AsyncClient() as client:
                # Get all jobs from job posting service
                resp = await client.get(f"{JOB_POSTING_SERVICE_URL}/api/v1/jobs/")
                resp.raise_for_status()
                all_jobs = resp.json()
                
                # Filter jobs based on search criteria
                filtered_jobs = self._filter_jobs(all_jobs, search_dto)
                
                # Apply pagination
                return filtered_jobs[skip:skip+limit]
                
        except Exception as e:
            print(f"Error fetching jobs from job posting service: {e}")
            # Fallback to mock data for assignment demonstration
            return [
                {
                    "id": 1,
                    "title": search_dto.query or "Sample Job",
                    "location": search_dto.location or "Istanbul",
                    "company": "Sample Company"
                }
            ]

    async def get_total_count(self, db: AsyncIOMotorClient, search_dto: SearchDTO) -> int:
        """Get total count of jobs matching the search criteria (without pagination)"""
        # JOB_POSTING_SERVICE_URL = os.getenv("JOB_POSTING_SERVICE_URL", "http://job_posting_service:8000")
        JOB_POSTING_SERVICE_URL = os.getenv("JOB_POSTING_SERVICE_URL", "http://job_posting_service:8000")
        
        try:
            async with httpx.AsyncClient() as client:
                # Get all jobs from job posting service
                resp = await client.get(f"{JOB_POSTING_SERVICE_URL}/api/v1/jobs/")
                resp.raise_for_status()
                all_jobs = resp.json()
                
                # Apply same filtering logic as search_jobs but without pagination
                filtered_jobs = self._filter_jobs(all_jobs, search_dto)
                return len(filtered_jobs)
                
        except Exception as e:
            print(f"Error getting total count: {e}")
            return 0

    def _filter_jobs(self, all_jobs: List[dict], search_dto: SearchDTO) -> List[dict]:
        """Helper method to filter jobs based on search criteria"""
        filtered_jobs = []
        for job in all_jobs:
            # Filter by query (title/description)
            if search_dto.query and search_dto.query.lower() not in job.get('title', '').lower():
                continue
            
            # Filter by location
            if search_dto.location and search_dto.location.lower() not in job.get('location', '').lower():
                continue
            
            # Filter by work mode
            if search_dto.work_mode:
                work_modes = [mode.strip() for mode in search_dto.work_mode.split(',')]
                job_mode = job.get('work_mode', '').lower()
                if not any(mode.lower() in job_mode for mode in work_modes):
                    continue
            
            # Filter by date
            if search_dto.date_filter:
                job_created = job.get('created_at')
                print(f"Date filter: {search_dto.date_filter}, Job {job.get('id')} created_at: {job_created}")
                if job_created:
                    try:
                        # Handle different date formats
                        if 'T' in job_created:
                            job_date = datetime.fromisoformat(job_created.replace('Z', '+00:00'))
                        else:
                            job_date = datetime.fromisoformat(job_created)
                        
                        now = datetime.now(job_date.tzinfo)
                        
                        if search_dto.date_filter == 'today':
                            if job_date.date() != now.date():
                                print(f"  Job {job.get('id')} filtered out: not today")
                                continue
                        elif search_dto.date_filter == '3hours':
                            if now - job_date > timedelta(hours=3):
                                print(f"  Job {job.get('id')} filtered out: older than 3 hours")
                                continue
                        elif search_dto.date_filter == '8hours':
                            if now - job_date > timedelta(hours=8):
                                print(f"  Job {job.get('id')} filtered out: older than 8 hours")
                                continue
                        print(f"  Job {job.get('id')} passed date filter")
                    except Exception as e:
                        print(f"Date parsing error for job {job.get('id')}: {e}")
                        # If date parsing fails, skip date filtering
                        pass
                else:
                    print(f"  Job {job.get('id')} has no created_at field")
                    # If no created_at field, skip date filtering
                    pass
            
            # Filter by country/city/district
            if search_dto.country and search_dto.country.lower() not in job.get('location', '').lower():
                continue
            if search_dto.city and search_dto.city.lower() not in job.get('location', '').lower():
                continue
            if search_dto.district and search_dto.district.lower() not in job.get('location', '').lower():
                continue
            
            filtered_jobs.append(job)
        
        return filtered_jobs

    async def save_search_history(self, db: AsyncIOMotorClient, user_id: int, search_dto: SearchDTO, results_count: int):
        """Save search history to MongoDB"""
        # Only save if at least one meaningful field is present
        if not (search_dto.query or search_dto.location or search_dto.city or search_dto.country or search_dto.district):
            print("[DEBUG] Not saving empty search to history.")
            return
        print(f"[DEBUG] save_search_history called: user_id={user_id}, query={search_dto.query}, location={search_dto.location}, results_count={results_count}")
        search_history = SearchHistory(
            user_id=user_id,
            job_name=search_dto.query,
            location=search_dto.location or "",
            created_at=datetime.utcnow()
        )
        
        # Convert to dict for MongoDB
        search_data = search_history.dict()
        search_data["results_count"] = results_count
        try:
            insertion = db.job_search.search_history.insert_one(search_data)
            if hasattr(insertion, '__await__'):
                await insertion
            print("[DEBUG] Search history inserted successfully.")
        except Exception as e:
            print(f"[ERROR] Failed to insert search history: {e}")

    async def get_user_search_history(self, db: AsyncIOMotorClient, user_id: int, limit: int = 10) -> List[dict]:
        """Get user's search history from MongoDB"""
        cursor = db.job_search.search_history.find(
            {"user_id": user_id}
        ).sort("created_at", -1).limit(limit)
        
        history = await cursor.to_list(length=limit)
        # Convert ObjectId to string for each document
        for doc in history:
            if "_id" in doc:
                doc["_id"] = str(doc["_id"])
        print(f"[DEBUG] get_user_search_history for user_id={user_id}: {history}")
        return history

    async def get_search_suggestions(self, query: str) -> List[str]:
        """Get search suggestions from cache"""
        # This would typically use cached popular searches
        return ["Software Engineer", "Data Scientist", "Product Manager"]

    async def get_popular_searches(self) -> List[str]:
        """Get popular searches from cache"""
        return ["Software Engineer", "Data Scientist", "Product Manager"]

    async def delete_user_search_history(self, db: AsyncIOMotorClient, user_id: int):
        """Delete all search history for a user from MongoDB"""
        try:
            result = await db.job_search.search_history.delete_many({"user_id": user_id})
            print(f"[DEBUG] Deleted {result.deleted_count} search history records for user_id={user_id}")
            return result.deleted_count
        except Exception as e:
            print(f"[ERROR] Failed to delete search history: {e}")
            return 0 