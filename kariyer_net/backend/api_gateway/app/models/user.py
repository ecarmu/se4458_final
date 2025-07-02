from sqlalchemy import Column, Integer, String, JSON
from ..core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)  # Not hashed as requested
    search_history = Column(JSON)  # Store recent searches
    notifications = Column(JSON)  # Store user notifications 
    is_company = Column(Integer, default=0)  # 0 = not company, 1 = company
    is_admin = Column(Integer, default=0)  # 0 = not admin, 1 = admin 