from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List
from ....core.database import get_db
from ....services.job_service import JobService
from ....schemas.job import JobCreate, JobUpdate, JobResponse
from pydantic import BaseModel

router = APIRouter()

@router.get("/", response_model=List[JobResponse])
async def get_jobs(
    skip: int = 0, 
    limit: int = 10,
    db: Session = Depends(get_db),
    job_service: JobService = Depends()
):
    """Get all jobs with pagination from Redis"""
    try:
        jobs = await job_service.get_jobs(db, skip, limit)
        return jobs
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving jobs: {str(e)}"
        )

@router.post("/", response_model=JobResponse)
async def create_job(
    job_data: JobCreate,
    db: Session = Depends(get_db),
    job_service: JobService = Depends()
):
    """Create a new job posting in Redis"""
    try:
        # Mock user ID for now
        created_by = 1
        job = await job_service.create_job(db, job_data, created_by)
        return job
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating job: {str(e)}"
        )

@router.get("/home", response_model=List[JobResponse])
async def get_home_jobs(
    city: str,
    db: Session = Depends(get_db),
    job_service: JobService = Depends()
):
    """Get at least 5 jobs in the given city, fallback to other jobs if none found."""
    jobs = await job_service.get_jobs_by_location(db, city, limit=5)
    if not jobs or len(jobs) < 5:
        # Fallback: get more jobs (not filtered by city), but avoid duplicates
        needed = 5 - len(jobs)
        all_jobs = await job_service.get_jobs(db, 0, 20)
        # Exclude jobs already in the city list
        city_job_ids = {job['id'] for job in jobs}
        fallback_jobs = [job for job in all_jobs if job['id'] not in city_job_ids and job.get('is_active', True)]
        jobs += fallback_jobs[:needed]
    return jobs[:5]

@router.get("/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: int,
    db: Session = Depends(get_db),
    job_service: JobService = Depends()
):
    """Get a specific job by ID from Redis"""
    job = await job_service.get_job(db, job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    return job

@router.put("/{job_id}", response_model=JobResponse)
async def update_job(
    job_id: int,
    job_data: JobUpdate,
    db: Session = Depends(get_db),
    job_service: JobService = Depends()
):
    """Update an existing job in Redis"""
    job = await job_service.update_job(db, job_id, job_data)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    return job

@router.delete("/{job_id}")
async def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    job_service: JobService = Depends()
):
    """Delete a job from Redis (soft delete)"""
    success = await job_service.delete_job(db, job_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    return {"message": "Job deleted successfully"} 

@router.get("/{job_id}/related", response_model=List[JobResponse])
async def get_related_jobs(
    job_id: int,
    skip: int = 0,
    limit: int = 3,
    db: Session = Depends(get_db),
    job_service: JobService = Depends()
):
    """Get related jobs by title or location, with pagination."""
    related = await job_service.get_related_jobs(db, job_id, skip=skip, limit=limit)
    return related

class ApplyRequest(BaseModel):
    user_id: int

@router.post("/{job_id}/apply")
async def apply_to_job(
    job_id: int,
    apply_req: ApplyRequest,
    db: Session = Depends(get_db),
    job_service: JobService = Depends()
):
    """Apply to a job. Returns 200 if successful, 409 if already applied."""
    success = await job_service.apply_to_job(db, job_id, apply_req.user_id)
    if not success:
        raise HTTPException(status_code=409, detail="Already applied to this job.")
    return {"message": "Application successful"} 