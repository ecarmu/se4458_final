import httpx
from ..core.config import settings

class JobService:
    @staticmethod
    async def get_jobs_from_search_service(query: str = None, city: str = None, page: int = 1, limit: int = 10):
        """Get jobs from search service"""
        # To be implemented
        pass

    @staticmethod
    async def create_job_in_posting_service(job_data: dict):
        """Create job in posting service"""
        # To be implemented
        pass 