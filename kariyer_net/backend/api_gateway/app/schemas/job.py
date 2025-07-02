from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class JobBase(BaseModel):
    title: str
    description: str
    company: str
    location: str
    work_mode: str
    job_type: str

class JobCreate(JobBase):
    pass

class Job(JobBase):
    id: int
    created_at: datetime
    applications_count: int = 0

    class Config:
        from_attributes = True 