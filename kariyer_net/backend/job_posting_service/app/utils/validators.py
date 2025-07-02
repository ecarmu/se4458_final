import re
from typing import Optional

def validate_job_title(title: str) -> bool:
    """Validate job title"""
    if not title or len(title.strip()) < 1:
        return False
    return len(title) <= 255

def validate_company_name(company: str) -> bool:
    """Validate company name"""
    if not company or len(company.strip()) < 1:
        return False
    return len(company) <= 255

def validate_location(location: str) -> bool:
    """Validate location"""
    if not location or len(location.strip()) < 1:
        return False
    return len(location) <= 255

def validate_salary_range(min_salary: Optional[int], max_salary: Optional[int]) -> bool:
    """Validate salary range"""
    if min_salary is not None and min_salary < 0:
        return False
    if max_salary is not None and max_salary < 0:
        return False
    if min_salary is not None and max_salary is not None:
        return min_salary <= max_salary
    return True 