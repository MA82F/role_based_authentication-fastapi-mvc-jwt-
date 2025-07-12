from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.auth.dependencies import require_admin
from app.user.schemas import UserResponse
from app.user.model import User
from .service import RoleService
from .schemas import RoleUpdate

router = APIRouter()


@router.patch("/roles/{user_id}", response_model=UserResponse)
async def update_user_role(
    user_id: int,
    role_data: RoleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Update user role (Admin only)"""
    updated_user = RoleService.update_user_role(db, user_id, role_data)
    return updated_user
