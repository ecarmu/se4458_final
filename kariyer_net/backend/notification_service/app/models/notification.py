from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, DateTime
from sqlalchemy.sql import func
from ..core.database import Base

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    type = Column(String, nullable=False, default="info")
    title = Column(String, nullable=False, default="Bildirim")
    message = Column(Text, nullable=False)
    data = Column(Text)  # Store as JSON string if needed
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    read_at = Column(DateTime(timezone=True), nullable=True)
    job_id = Column(Integer)
    alert_id = Column(Integer, ForeignKey("job_alerts.id")) 