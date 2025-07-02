from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer
import json

security = HTTPBearer()

async def get_current_user(request: Request):
    """Dependency to get current authenticated user from request headers"""
    # For now, we'll get user info from a custom header
    # In a real implementation, you'd validate JWT tokens
    user_header = request.headers.get('X-User-Info')
    if user_header:
        try:
            return json.loads(user_header)
        except:
            pass
    
    # Fallback: return a mock user for development
    return {
        "id": 1,
        "email": "admin@example.com",
        "first_name": "Admin",
        "last_name": "User",
        "is_admin": True,
        "is_company": False
    } 