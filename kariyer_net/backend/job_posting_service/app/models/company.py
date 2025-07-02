from sqlalchemy import Column, Integer, String, Text
from ..core.database import Base

class Company(Base):
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    logo_url = Column(String)
    location = Column(String)
    jobs = Column(Text)  # Store job IDs as JSON string 