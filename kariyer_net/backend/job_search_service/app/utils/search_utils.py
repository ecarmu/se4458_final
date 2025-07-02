from typing import List, Dict, Any
import re

def build_search_query(filters: Dict[str, Any]) -> str:
    """Build search query from filters"""
    query_parts = []
    
    if filters.get("query"):
        query_parts.append(filters["query"])
    
    if filters.get("location"):
        query_parts.append(f"location:{filters['location']}")
    
    if filters.get("company"):
        query_parts.append(f"company:{filters['company']}")
    
    return " ".join(query_parts)

def sanitize_search_term(term: str) -> str:
    """Sanitize search term"""
    return re.sub(r'[^\w\s]', '', term).strip()

def calculate_pagination_offset(page: int, limit: int) -> int:
    """Calculate pagination offset"""
    return (page - 1) * limit 