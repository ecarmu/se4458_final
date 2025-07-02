from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database (for companies and users)
    # DATABASE_URL: str = "postgresql://ardah@localhost:5432/job_posting"
    DATABASE_URL: str = "postgresql://ardah:password@db:5432/job_posting"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Redis (for job postings)
    # REDIS_URL: str = "redis://localhost:6379"
    REDIS_URL: str = "redis://redis:6379"
    
    # RabbitMQ
    # RABBITMQ_URL: str = "amqp://guest:guest@localhost:5672/"
    RABBITMQ_URL: str = "amqp://guest:guest@queue:5672/"
    
    class Config:
        env_file = ".env"

settings = Settings() 