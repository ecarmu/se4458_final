from pydantic import BaseModel
from typing import List

class FilterDTO(BaseModel):
    cities: List[str] = []
    companies: List[str] = []
    work_modes: List[str] = []
    job_types: List[str] = []
    salary_ranges: List[str] = []

    def to_dict(self) -> dict:
        return self.dict() 