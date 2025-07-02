from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr
from typing import Optional
from sqlalchemy.orm import Session
from ....core.database import get_db
from ....models.user import User as UserModel

router = APIRouter()

# Pydantic models for request/response
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    is_company: bool = False
    is_admin: bool = False

class UserResponse(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    is_active: bool = True
    is_company: bool = False
    is_admin: bool = False

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

@router.post("/login", response_model=LoginResponse)
async def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    """User login endpoint"""
    user = db.query(UserModel).filter(UserModel.email == credentials.email).first()
    if not user or user.password != credentials.password:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return {
        "access_token": "mock_jwt_token_12345",
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "first_name": getattr(user, 'first_name', user.email.split('@')[0]),
            "last_name": getattr(user, 'last_name', ''),
            "phone": getattr(user, 'phone', None),
            "is_active": True,
            "is_company": bool(getattr(user, 'is_company', 0)),
            "is_admin": bool(getattr(user, 'is_admin', 0)),
        }
    }

@router.post("/register", response_model=UserResponse)
async def register(user_data: RegisterRequest, db: Session = Depends(get_db)):
    """User registration endpoint"""
    existing = db.query(UserModel).filter(UserModel.email == user_data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = UserModel(
        email=user_data.email,
        password=user_data.password,
        is_company=int(user_data.is_company),
        is_admin=int(user_data.is_admin),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {
        "id": user.id,
        "email": user.email,
        "first_name": user_data.first_name,
        "last_name": user_data.last_name,
        "phone": user_data.phone,
        "is_active": True,
        "is_company": user_data.is_company,
        "is_admin": user_data.is_admin,
    }

@router.post("/logout")
async def logout():
    """User logout endpoint"""
    # TODO: Implement token blacklisting
    return {"message": "Successfully logged out"}

@router.get("/profile", response_model=UserResponse)
async def get_profile():
    """Get current user profile"""
    # TODO: Implement actual user retrieval from token
    return {
        "id": 1,
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "phone": "+1234567890",
        "is_active": True
    }

@router.put("/profile", response_model=UserResponse)
async def update_profile(user_data: RegisterRequest):
    """Update current user profile"""
    # TODO: Implement actual profile update logic
    return {
        "id": 1,
        "email": user_data.email,
        "first_name": user_data.first_name,
        "last_name": user_data.last_name,
        "phone": user_data.phone,
        "is_active": True
    }

@router.post("/refresh")
async def refresh_token():
    """Refresh access token"""
    # TODO: Implement token refresh logic
    return {
        "access_token": "new_mock_jwt_token_67890",
        "token_type": "bearer"
    } 