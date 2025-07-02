from fastapi import APIRouter, HTTPException, status, Depends, Request
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from ...dependencies import get_current_user
import httpx
import os

router = APIRouter()

# Pydantic models for request/response
class JobSearchRequest(BaseModel):
    query: Optional[str] = None
    location: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    job_type: Optional[str] = None  # full-time, part-time, contract, internship
    experience_level: Optional[str] = None  # entry, mid, senior, executive
    skills: Optional[List[str]] = None
    company: Optional[str] = None
    remote: Optional[bool] = None
    page: int = 1
    limit: int = 10
    sort_by: str = "relevance"  # relevance, date, salary, title

class JobResponse(BaseModel):
    id: int
    title: str
    company: str
    location: str
    salary_min: Optional[int]
    salary_max: Optional[int]
    job_type: str
    experience_level: str
    description: str
    requirements: List[str]
    benefits: List[str]
    posted_date: datetime
    is_active: bool

class SearchHistoryResponse(BaseModel):
    id: str  # Accept string IDs from MongoDB
    user_id: int
    query: str
    filters: dict
    results_count: int
    search_date: datetime

class SearchAnalyticsResponse(BaseModel):
    total_searches: int
    popular_keywords: List[str]
    popular_locations: List[str]
    average_results: float
    search_trends: dict

# Enhanced job search endpoints
@router.get("/", response_model=dict)
async def search_jobs(request: Request):
    """Proxy job search to job search microservice with pagination and filtering"""
    JOB_SEARCH_SERVICE_URL = os.getenv("JOB_SEARCH_SERVICE_URL", "http://job_search_service:8001")
    params = dict(request.query_params)
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{JOB_SEARCH_SERVICE_URL}/api/v1/search", params=params)
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@router.post("/search", response_model=List[JobResponse])
async def advanced_search(search_request: JobSearchRequest):
    """Advanced job search with structured request"""
    return [
        {
            "id": 1,
            "title": "Senior Python Developer",
            "company": "Tech Corp",
            "location": search_request.location or "Istanbul",
            "salary_min": search_request.salary_min or 50000,
            "salary_max": search_request.salary_max or 100000,
            "job_type": search_request.job_type or "full-time",
            "experience_level": search_request.experience_level or "senior",
            "description": "We are looking for a skilled Python developer...",
            "requirements": search_request.skills or ["Python", "Django"],
            "benefits": ["Health insurance", "Remote work"],
            "posted_date": datetime.now(),
            "is_active": True
        }
    ]

@router.get("/search/history", response_model=List[SearchHistoryResponse])
async def get_search_history(user_id: int, limit: int = 10):
    """Proxy user's search history to job_search_service and transform to match SearchHistoryResponse model."""
    JOB_SEARCH_SERVICE_URL = os.getenv("JOB_SEARCH_SERVICE_URL", "http://job_search_service:8001")
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{JOB_SEARCH_SERVICE_URL}/api/v1/search/history", params={"user_id": user_id, "limit": limit})
            resp.raise_for_status()
            data = resp.json()
            # Transform the data to match SearchHistoryResponse
            transformed = []
            for item in data:
                transformed.append({
                    "id": item.get("_id", ""),
                    "user_id": item.get("user_id"),
                    "query": item.get("job_name", ""),
                    "filters": {"location": item.get("location", "")},
                    "results_count": item.get("results_count", 0),
                    "search_date": item.get("created_at", item.get("search_date", "")),
                })
            return transformed
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@router.get("/search/analytics", response_model=SearchAnalyticsResponse)
async def get_search_analytics():
    """Get search analytics and trends"""
    return {
        "total_searches": 1250,
        "popular_keywords": ["python", "developer", "software engineer", "data scientist"],
        "popular_locations": ["Istanbul", "Ankara", "Izmir", "Bursa"],
        "average_results": 12.5,
        "search_trends": {
            "python": 150,
            "javascript": 120,
            "java": 80
        }
    }

@router.get("/search/suggestions")
async def get_search_suggestions(query: str, limit: int = 5):
    """Get search suggestions based on partial query"""
    suggestions = [
        f"{query} developer",
        f"{query} engineer",
        f"senior {query}",
        f"{query} specialist",
        f"{query} manager"
    ]
    return {"suggestions": suggestions[:limit]}

# Job CRUD operations (existing functionality)
@router.post("/")
async def create_job(job_data: dict, current_user=Depends(get_current_user)):
    """Proxy job creation to job posting microservice"""
    if not (current_user.get('is_admin', False) or current_user.get('is_company', False)):
        raise HTTPException(status_code=403, detail="Not authorized to create jobs.")
    JOB_POSTING_SERVICE_URL = os.getenv("JOB_POSTING_SERVICE_URL", "http://job_posting_service:8000")
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(f"{JOB_POSTING_SERVICE_URL}/api/v1/jobs/", json=job_data)
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@router.get("/{job_id}")
async def get_job(job_id: int):
    """Route job retrieval requests to job-posting-service"""
    JOB_POSTING_SERVICE_URL = os.getenv("JOB_POSTING_SERVICE_URL", "http://job_posting_service:8000")
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{JOB_POSTING_SERVICE_URL}/api/v1/jobs/{job_id}")
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@router.put("/{job_id}")
async def update_job(job_id: int, job_data: dict, current_user=Depends(get_current_user)):
    """Route job update requests to job-posting-service"""
    if not (current_user.get('is_admin', False) or current_user.get('is_company', False)):
        raise HTTPException(status_code=403, detail="Not authorized to update jobs.")
    JOB_POSTING_SERVICE_URL = os.getenv("JOB_POSTING_SERVICE_URL", "http://job_posting_service:8000")
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.put(f"{JOB_POSTING_SERVICE_URL}/api/v1/jobs/{job_id}", json=job_data)
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{job_id}")
async def delete_job(job_id: int, current_user=Depends(get_current_user)):
    """Route job deletion requests to job-posting-service"""
    if not (current_user.get('is_admin', False) or current_user.get('is_company', False)):
        raise HTTPException(status_code=403, detail="Not authorized to delete jobs.")
    return {"message": f"Delete job {job_id} endpoint - to be implemented"}

# Additional search features
@router.get("/search/filters")
async def get_available_filters():
    """Get available search filters and options"""
    return {
        "job_types": ["full-time", "part-time", "contract", "internship"],
        "experience_levels": ["entry", "mid", "senior", "executive"],
        "locations": ["Istanbul", "Ankara", "Izmir", "Bursa", "Antalya"],
        "salary_ranges": [
            {"min": 0, "max": 25000, "label": "0-25K"},
            {"min": 25000, "max": 50000, "label": "25K-50K"},
            {"min": 50000, "max": 100000, "label": "50K-100K"},
            {"min": 100000, "max": None, "label": "100K+"}
        ]
    }

@router.post("/search/save")
async def save_search(user_id: int, search_request: JobSearchRequest):
    """Save a search for later use"""
    return {
        "message": "Search saved successfully",
        "search_id": 1,
        "user_id": user_id
    }

@router.post("/{job_id}/apply")
async def apply_to_job(job_id: int, apply_data: dict):
    """Proxy job application to job posting microservice"""
    #JOB_POSTING_SERVICE_URL = os.getenv("JOB_POSTING_SERVICE_URL", "http://job_posting:8000")
    JOB_POSTING_SERVICE_URL = os.getenv("JOB_POSTING_SERVICE_URL", "http://job_posting_service:8000")
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(f"{JOB_POSTING_SERVICE_URL}/api/v1/jobs/{job_id}/apply", json=apply_data)
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@router.get("/{job_id}/related")
async def get_related_jobs(job_id: int, skip: int = 0, limit: int = 3):
    """Proxy related jobs to job posting microservice with pagination support."""
    JOB_POSTING_SERVICE_URL = os.getenv("JOB_POSTING_SERVICE_URL", "http://job_posting_service:8000")
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{JOB_POSTING_SERVICE_URL}/api/v1/jobs/{job_id}/related", params={"skip": skip, "limit": limit})
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) 