from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class SearchHistory(BaseModel):
    user_id: int
    job_name: str
    location: str
    employment_type: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class SearchHistoryInDB(SearchHistory):
    id: str = Field(default_factory=lambda: str(datetime.utcnow().timestamp())) 