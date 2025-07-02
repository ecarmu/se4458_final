from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

#Base = declarative_base()
from ..core.database import Base
class JobAlert(Base):
    __tablename__ = "job_alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    job_name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    employment_type = Column(String)  # "part-time", "full-time"
    is_active = Column(Boolean, default=True)  # Allow users to pause/resume alerts
    last_triggered = Column(DateTime(timezone=True))  # Prevent spam notifications 
    frequency = Column(String, nullable=True)  # daily, weekly, etc.
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) 