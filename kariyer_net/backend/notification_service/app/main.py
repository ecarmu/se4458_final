from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.v1.router import api_router
from .workers.job_alert_worker import JobAlertWorker
from .workers.related_job_worker import RelatedJobWorker
from .services.scheduler_service import SchedulerService
import asyncio

app = FastAPI(
    title="Notification Service",
    description="Service for handling notifications and alerts",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    #allow_origins=["*"],  # Or specify your frontend URL
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the main router
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Notification Service"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.on_event("startup")
async def startup_event():
    """Start background workers and scheduler"""
    # Start workers in background
    asyncio.create_task(JobAlertWorker().start())
    asyncio.create_task(RelatedJobWorker().start())
    asyncio.create_task(SchedulerService().start_scheduler())
