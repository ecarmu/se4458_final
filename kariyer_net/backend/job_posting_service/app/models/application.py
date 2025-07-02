from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from ..core.database import Base

class JobApplication(Base):
    __tablename__ = "job_applications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    job_id = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now()) 