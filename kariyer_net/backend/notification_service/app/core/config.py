from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    # Database
    #DATABASE_URL: str = "mongodb://nosql:27017/notifications"
    DATABASE_URL: str = "postgresql://ardah:password@db:5432/notifications"
    
    # RabbitMQ
    #RABBITMQ_URL: str = os.getenv("RABBITMQ_URL", "amqp://guest:guest@queue:5672/")
    RABBITMQ_URL: str = os.getenv("RABBITMQ_URL", "amqp://guest:guest@queue:5672/")

    
    # Email settings
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    
    class Config:
        env_file = ".env"

settings = Settings() 