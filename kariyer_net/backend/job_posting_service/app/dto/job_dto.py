from pydantic import BaseModel
from typing import Optional

class JobDTO(BaseModel):
    title: str
    description: str
    company: str
    location: str
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    work_mode: str
    job_type: str
    created_by: Optional[int] = None

    @classmethod
    def from_schema(cls, schema):
        """Create DTO from Pydantic schema"""
        return cls(**schema.dict())

    def to_dict(self):
        """Convert to dictionary"""
        return self.dict() 