from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class SearchRequest(BaseModel):
    query: Optional[str] = None
    location: Optional[str] = None
    work_mode: Optional[List[str]] = None
    job_type: Optional[List[str]] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    page: int = 1
    limit: int = 10

class SearchResponse(BaseModel):
    id: int
    title: str
    company: str
    location: str
    work_mode: str
    job_type: str
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True

class Filters(BaseModel):
    cities: List[str] = []
    companies: List[str] = []
    work_modes: List[str] = []
    job_types: List[str] = []
    salary_ranges: List[str] = [] 