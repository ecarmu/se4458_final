from fastapi import HTTPException, status
from ..models.user import User
from ..schemas.user import UserCreate
from sqlalchemy.orm import Session

class AuthService:
    @staticmethod
    def create_user(db: Session, user: UserCreate):
        """Create a new user"""
        # To be implemented
        pass

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str):
        """Authenticate user"""
        # To be implemented
        pass 