from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class AlertBase(BaseModel):
    query: Optional[str] = None
    location: Optional[str] = None
    work_mode: Optional[List[str]] = None
    job_type: Optional[List[str]] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    frequency: Optional[str] = None  # daily, weekly, etc.

class AlertCreate(AlertBase):
    user_id: int
    # 'query' should be mapped from the first keyword in the payload

class AlertResponse(AlertBase):
    id: int
    user_id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    keywords: List[str]

    @property
    def keywords(self) -> List[str]:
        return [self.query] if self.query else []

    class Config:
        from_attributes = True 