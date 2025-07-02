from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Service URLs
    #JOB_POSTING_SERVICE_URL: str = "http://job_posting:8000"
    JOB_POSTING_SERVICE_URL: str = "http://job_posting_service:8000"
    #JOB_SEARCH_SERVICE_URL: str = "http://job_search:8001"
    JOB_SEARCH_SERVICE_URL: str = "http://job_search_service:8001"
    #NOTIFICATION_SERVICE_URL: str = "http://notification:8002"
    NOTIFICATION_SERVICE_URL: str = "http://notification_service:8002"
    #AI_AGENT_SERVICE_URL: str = "http://ai_agent:8003"
    AI_AGENT_SERVICE_URL: str = "http://ai_agent:8003"
    
    # Database
    DATABASE_URL: str = "postgresql://user:pass@db:5432/api_gateway"

    # Security
    SECRET_KEY: str = "your_secret_key"

settings = Settings() 