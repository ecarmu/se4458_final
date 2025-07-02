from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from ....core.database import get_db
from ....schemas.job import JobResponse
from ....services.job_service import JobService

router = APIRouter()

@router.get("/jobs/pending", response_model=List[JobResponse])
async def get_pending_jobs(
    db: Session = Depends(get_db),
    job_service: JobService = Depends()
):
    """Get pending job approvals (admin only)"""
    return {"message": "Get pending jobs endpoint - to be implemented"} 