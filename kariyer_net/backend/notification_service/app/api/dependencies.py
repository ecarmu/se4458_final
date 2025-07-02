from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def get_current_user():
    """Dependency to get current authenticated user"""
    # To be implemented
    pass 