from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import timedelta

from app.core.security import verify_password, create_access_token
from app.core.config import settings
from app.user.service import UserService
from app.user.schemas import UserCreate
from .schemas import LoginRequest, TokenResponse


class AuthService:
    
    @staticmethod
    def register_user(db: Session, user_data: UserCreate):
        """Register a new user"""
        # Check if user already exists
        if UserService.get_user_by_username(db, user_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        
        if UserService.get_user_by_email(db, user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create user
        user = UserService.create_user(db, user_data)
        return user
    
    @staticmethod
    def authenticate_user(db: Session, login_data: LoginRequest) -> TokenResponse:
        """Authenticate user and return JWT token"""
        # Get user by username
        user = UserService.get_user_by_username(db, login_data.username)
        
        if not user or not verify_password(login_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )
        
        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username, "user_id": user.id, "role": user.role},
            expires_delta=access_token_expires
        )
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer"
        )
