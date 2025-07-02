from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.v1.router import api_router

app = FastAPI(
    title="Job Search API Gateway",
    description="API Gateway for Job Search Application",
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
    return {"message": "Job Search API Gateway"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
