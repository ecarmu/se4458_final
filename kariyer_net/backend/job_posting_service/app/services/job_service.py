from sqlalchemy.orm import Session
from typing import List, Optional
import json
import redis
from ..models.job import Job
from ..models.company import Company
from ..schemas.job import JobCreate, JobUpdate
from ..core.config import settings
from ..models.application import JobApplication
from sqlalchemy import func
from datetime import datetime, timezone
import aio_pika
import asyncio

class JobService:
    def __init__(self):
        self.redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)
    
    async def get_jobs(self, db: Session, skip: int = 0, limit: int = 10) -> List[dict]:
        """Get all jobs from Redis with pagination"""
        # Get all job keys from Redis
        job_keys = self.redis_client.keys("job:*")
        job_keys = job_keys[skip:skip + limit]
        
        jobs = []
        for key in job_keys:
            job_data = self.redis_client.get(key)
            if job_data:
                jobs.append(json.loads(job_data))
        
        return jobs

    async def get_job(self, db: Session, job_id: int) -> Optional[dict]:
        """Get a specific job by ID from Redis and add application_count and last_updated"""
        job_data = self.redis_client.get(f"job:{job_id}")
        if job_data:
            job = json.loads(job_data)
            # Get application count from DB
            application_count = db.query(func.count(JobApplication.id)).filter(JobApplication.job_id == job_id).scalar()
            job["application_count"] = application_count or 0
            # Use updated_at if available, else fetch from SQL, else created_at
            updated_at = job.get("updated_at")
            if not updated_at:
                sql_job = db.query(Job).filter(Job.id == job_id).first()
                if sql_job and sql_job.updated_at:
                    updated_at = sql_job.updated_at.replace(tzinfo=timezone.utc).isoformat().replace('+00:00', 'Z')
            else:
                # Patch: ensure Z for UTC
                if updated_at and not updated_at.endswith('Z'):
                    updated_at = updated_at + 'Z'
            created_at = job.get("created_at")
            if created_at and not created_at.endswith('Z'):
                created_at = created_at + 'Z'
            job["last_updated"] = updated_at or created_at or datetime.utcnow().replace(tzinfo=timezone.utc).isoformat().replace('+00:00', 'Z')
            job["updated_at"] = updated_at
            job["created_at"] = created_at
            return job
        return None

    async def create_job(self, db: Session, job_data: JobCreate, created_by: int) -> dict:
        """Create a new job in Redis and also in SQL for FK integrity, and publish to RabbitMQ."""
        # Get company info from SQL database
        company = db.query(Company).filter(Company.id == job_data.company_id).first()
        if not company:
            raise ValueError("Company not found")
        
        # Generate job ID
        job_id = self.redis_client.incr("job_counter")
        
        # Create timestamp
        now = datetime.utcnow().replace(tzinfo=timezone.utc)
        iso_now = now.isoformat().replace('+00:00', 'Z')
        
        job_dict = {
            "id": job_id,
            "title": job_data.title,
            "description": job_data.description,
            "company_id": job_data.company_id,
            "company_name": company.name,
            "location": job_data.location,
            "salary_min": job_data.salary_min,
            "salary_max": job_data.salary_max,
            "work_mode": job_data.work_mode,
            "job_type": job_data.job_type,
            "created_by": created_by,
            "is_active": True,
            "created_at": iso_now,
            "updated_at": iso_now
        }
        
        # Store in Redis
        self.redis_client.setex(
            f"job:{job_id}", 
            3600 * 24 * 30,  # 30 days TTL
            json.dumps(job_dict)
        )
        
        # Also insert into SQL jobs table for FK integrity
        sql_job = Job(
            id=job_id,
            job_name=job_data.title,
            country="Turkey",  # Default or parse from location
            city=job_data.location.split(",")[0] if "," in job_data.location else job_data.location,
            town="",  # Not available, set empty
            employment_type=job_data.job_type,
            workplace_type=job_data.work_mode,
            company_id=job_data.company_id,
            job_description=job_data.description
        )
        db.add(sql_job)
        db.commit()
        db.refresh(sql_job)
        
        # Publish to RabbitMQ (safe, non-blocking)
        try:
            connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
            async with connection:
                channel = await connection.channel()
                queue = await channel.declare_queue("new_jobs", durable=True)
                message_body = json.dumps(job_dict).encode()
                await channel.default_exchange.publish(
                    aio_pika.Message(body=message_body),
                    routing_key=queue.name
                )
                print("[RabbitMQ] Published new job event")
        except Exception as e:
            print(f"[RabbitMQ] Failed to publish new job event: {e}")
        return job_dict

    async def update_job(self, db: Session, job_id: int, job_data: JobUpdate) -> Optional[dict]:
        """Update an existing job in Redis and SQL"""
        job = await self.get_job(db, job_id)
        if not job:
            return None
        
        # Update fields in Redis job dict
        update_data = job_data.dict(exclude_unset=True)
        job.update(update_data)
        # Set updated_at to now
        now = datetime.utcnow().replace(tzinfo=timezone.utc)
        iso_now = now.isoformat().replace('+00:00', 'Z')
        job['updated_at'] = iso_now
        
        # Store updated job back to Redis
        self.redis_client.setex(
            f"job:{job_id}",
            3600 * 24 * 30,  # 30 days TTL
            json.dumps(job)
        )
        
        # --- Update SQL record ---
        sql_job = db.query(Job).filter(Job.id == job_id).first()
        if sql_job:
            for field, value in update_data.items():
                # Map field names if needed
                if hasattr(sql_job, field):
                    setattr(sql_job, field, value)
                elif field == "title":
                    sql_job.job_name = value
                elif field == "description":
                    sql_job.job_description = value
                elif field == "work_mode":
                    sql_job.workplace_type = value
                elif field == "job_type":
                    sql_job.employment_type = value
                elif field == "location":
                    sql_job.city = value.split(",")[0] if "," in value else value
            sql_job.updated_at = now
            db.commit()
            db.refresh(sql_job)
        
        return job

    async def delete_job(self, db: Session, job_id: int) -> bool:
        """Delete a job from Redis"""
        job = await self.get_job(db, job_id)
        if not job:
            return False
        
        # Soft delete by setting is_active to False
        job["is_active"] = False
        self.redis_client.setex(
            f"job:{job_id}",
            3600 * 24 * 30,  # 30 days TTL
            json.dumps(job)
        )
        
        return True

    async def get_jobs_by_location(self, db: Session, location: str, limit: int = 5) -> List[dict]:
        """Get jobs by location from Redis"""
        # This is a simplified implementation
        # In production, you might want to use Redis search or maintain separate indexes
        all_jobs = await self.get_jobs(db, 0, 100)  # Get more jobs to filter
        filtered_jobs = [
            job for job in all_jobs 
            if location.lower() in job.get("location", "").lower() and job.get("is_active", True)
        ]
        return filtered_jobs[:limit]

    async def get_company(self, db: Session, company_id: int) -> Optional[Company]:
        """Get company from SQL database"""
        return db.query(Company).filter(Company.id == company_id).first()

    async def create_company(self, db: Session, company_data: dict) -> Company:
        """Create a new company in SQL database"""
        company = Company(**company_data)
        db.add(company)
        db.commit()
        db.refresh(company)
        return company 

    async def get_related_jobs(self, db: Session, job_id: int, skip: int = 0, limit: int = 3) -> list:
        """Find related jobs by similar title or location, excluding the current job, with pagination."""
        job = await self.get_job(db, job_id)
        if not job:
            return []
        all_jobs = await self.get_jobs(db, 0, 100)
        related = [
            j for j in all_jobs
            if j["id"] != job_id and (
                job["title"].split()[0].lower() in j["title"].lower() or
                job["location"].lower() == j["location"].lower()
            ) and j.get("is_active", True)
        ]
        return related[skip:skip+limit]

    async def apply_to_job(self, db: Session, job_id: int, user_id: int) -> bool:
        """Create a job application if not already applied."""
        exists = db.query(JobApplication).filter(JobApplication.job_id == job_id, JobApplication.user_id == user_id).first()
        if exists:
            return False  # Already applied
        application = JobApplication(job_id=job_id, user_id=user_id)
        db.add(application)
        db.commit()
        db.refresh(application)
        
        # Update application count in Redis
        job_data = self.redis_client.get(f"job:{job_id}")
        if job_data:
            job = json.loads(job_data)
            # Get current application count from DB
            application_count = db.query(func.count(JobApplication.id)).filter(JobApplication.job_id == job_id).scalar()
            job["application_count"] = application_count
            # Update the job in Redis
            self.redis_client.setex(
                f"job:{job_id}",
                3600 * 24 * 30,  # 30 days TTL
                json.dumps(job)
            )
        
        return True 