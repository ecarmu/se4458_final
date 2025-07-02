from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.v1.router import api_router
from .core.database import connect_to_mongo, close_mongo_connection

app = FastAPI(
    title="Job Search Service",
    description="Service for job search functionality",
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

# Include the main router
app.include_router(api_router, prefix="/api/v1")

@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()

@app.get("/")
async def root():
    return {"message": "Job Search Service"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
