from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # OpenAI
    OPENAI_API_KEY: str = ""  # Set this in your .env file as OPENAI_API_KEY=sk-...
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    
    # Service URLs
    # For Docker Compose deployment, use service names:
    #   JOB_SEARCH_SERVICE_URL=http://job_search:8001
    #   JOB_POSTING_SERVICE_URL=http://job_posting:8000
    # For local development, use localhost and correct ports:
    #   JOB_SEARCH_SERVICE_URL=http://job_search_service:8001
    #   JOB_POSTING_SERVICE_URL=http://job_posting_service:8000
    JOB_SEARCH_SERVICE_URL: str = "http://job_search_service:8001"
    JOB_POSTING_SERVICE_URL: str = "http://job_posting_service:8000"

    # JOB_SEARCH_SERVICE_URL="http://job_search_service:8001"
    # JOB_POSTING_SERVICE_URL="http://job_posting_service:8000"
    
    class Config:
        env_file = ".env"

settings = Settings() 