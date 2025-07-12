from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.user.service import UserService
from app.user.model import User
from .schemas import RoleUpdate


class RoleService:
    
    @staticmethod
    def update_user_role(db: Session, user_id: int, role_data: RoleUpdate) -> User:
        """Update user role (admin only)"""
        # Validate role
        if role_data.role not in ["user", "admin"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid role. Must be 'user' or 'admin'"
            )
        
        # Get user
        user = UserService.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Update role
        user.role = role_data.role
        db.commit()
        db.refresh(user)
        
        return user
