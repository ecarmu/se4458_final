from pydantic import BaseModel
from typing import Optional, List

class SearchDTO(BaseModel):
    query: Optional[str] = None
    location: Optional[str] = None
    work_mode: Optional[str] = None  # Comma-separated string from frontend
    date_filter: Optional[str] = None  # today, 3hours, 8hours
    country: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    job_type: Optional[List[str]] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    page: int = 1
    limit: int = 10

    def to_search_params(self) -> dict:
        """Convert to search parameters"""
        params = {}
        if self.query:
            params["query"] = self.query
        if self.location:
            params["location"] = self.location
        if self.work_mode:
            params["work_mode"] = self.work_mode
        if self.date_filter:
            params["date_filter"] = self.date_filter
        if self.country:
            params["country"] = self.country
        if self.city:
            params["city"] = self.city
        if self.district:
            params["district"] = self.district
        if self.job_type:
            params["job_type"] = self.job_type
        if self.salary_min:
            params["salary_min"] = self.salary_min
        if self.salary_max:
            params["salary_max"] = self.salary_max
        params["page"] = self.page
        params["limit"] = self.limit
        return params 