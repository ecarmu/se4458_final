from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.v1.router import api_router

app = FastAPI(
    title="Job Posting Service",
    description="Service for managing job postings",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    #allow_origins=["*"],
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Job Posting Service is running"}

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "job_posting_service"}

# Include the main router
app.include_router(api_router, prefix="/api/v1")
