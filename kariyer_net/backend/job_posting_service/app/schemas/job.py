from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class JobBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=10)
    company_id: int = Field(..., gt=0)
    location: str = Field(..., min_length=1, max_length=255)
    salary_min: Optional[int] = Field(None, ge=0)
    salary_max: Optional[int] = Field(None, ge=0)
    work_mode: str = Field(..., pattern="^(remote|on-site|hybrid)$")
    job_type: str = Field(..., pattern="^(full-time|part-time|contract)$")

class JobCreate(JobBase):
    pass

class JobUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, min_length=10)
    company_id: Optional[int] = Field(None, gt=0)
    location: Optional[str] = Field(None, min_length=1, max_length=255)
    salary_min: Optional[int] = Field(None, ge=0)
    salary_max: Optional[int] = Field(None, ge=0)
    work_mode: Optional[str] = Field(None, pattern="^(remote|on-site|hybrid)$")
    job_type: Optional[str] = Field(None, pattern="^(full-time|part-time|contract)$")

class JobResponse(BaseModel):
    id: int
    title: str
    description: str
    company_id: int
    company_name: str
    location: str
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    work_mode: str
    job_type: str
    is_active: bool
    created_by: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    last_updated: Optional[datetime] = None
    application_count: Optional[int] = 0

    class Config:
        from_attributes = True 