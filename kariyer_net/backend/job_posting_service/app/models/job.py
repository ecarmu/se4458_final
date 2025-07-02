from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from ..core.database import Base

class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    job_name = Column(String, nullable=False)  # e.g., "Yazılım Uzmanı"
    country = Column(String, nullable=False)
    city = Column(String, nullable=False)  # e.g., "Istanbul"
    town = Column(String, nullable=False)  # e.g., "Kadıköy"
    employment_type = Column(String, nullable=False)  # "part-time" or "full-time"
    workplace_type = Column(String, nullable=False)  # "on-site", "hybrid", "remote"
    company_id = Column(Integer, ForeignKey("companies.id"))
    job_description = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now()) 
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now()) 