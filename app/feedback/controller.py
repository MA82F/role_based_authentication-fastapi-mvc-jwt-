from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user, require_admin
from app.core.database import get_db
from app.user.model import User

from .schemas import FeedbackCreate, FeedbackResponse, FeedbackSummary, FeedbackWithUser
from .service import FeedbackService

router = APIRouter()


@router.post(
    "/feedback", response_model=FeedbackResponse, status_code=status.HTTP_201_CREATED
)
async def submit_feedback(
    feedback_data: FeedbackCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> FeedbackResponse:
    """Submit feedback (User access required)"""
    feedback = FeedbackService.create_feedback(db, feedback_data, current_user.id)
    return feedback


@router.get("/admin/feedback", response_model=List[FeedbackWithUser])
async def get_all_feedback(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> List[FeedbackWithUser]:
    """Get all feedback (Admin only)"""
    feedback_list = FeedbackService.get_all_feedback(db, skip=skip, limit=limit)
    return feedback_list


@router.get("/feedback/summary", response_model=FeedbackSummary)
async def get_feedback_summary(db: Session = Depends(get_db)) -> FeedbackSummary:
    """Get feedback summary (Public access)"""
    summary = FeedbackService.get_feedback_summary(db)
    return summary
