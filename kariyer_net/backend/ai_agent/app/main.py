from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.v1.router import api_router

app = FastAPI(
    title="AI Agent Service",
    description="Service for AI-powered job search assistance",
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

@app.get("/")
async def root():
    return {"message": "AI Agent Service"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
