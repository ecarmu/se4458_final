from pydantic_settings import BaseSettings
import asyncio

class Settings(BaseSettings):
    app_name: str = "Job Search Service"
    debug: bool = False
    # MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_URL: str = "mongodb://nosql:27017"
    # REDIS_URL: str = "redis://localhost:6379"
    REDIS_URL: str = "redis://redis:6379"
    
    # Job Posting Service
    JOB_POSTING_SERVICE_URL: str = "http://job_posting:8000"
    
    class Config:
        env_file = ".env"

class MockDB:
    def __init__(self):
        async def insert_one(*args, **kwargs):
            print(f"Saved search: {args if args else kwargs}")
        self.job_search = type('obj', (object,), {
            'search_history': type('obj', (object,), {
                'insert_one': insert_one,
                'find': lambda *args, **kwargs: type('obj', (object,), {
                    'sort': lambda *args, **kwargs: type('obj', (object,), {
                        'limit': lambda *args, **kwargs: type('obj', (object,), {
                            'to_list': lambda *args, **kwargs: asyncio.coroutine(lambda: [])
                        })()
                    })()
                })()
            })()
        })()

settings = Settings() 