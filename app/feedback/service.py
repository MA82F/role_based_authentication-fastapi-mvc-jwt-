from typing import List

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.user.model import User

from .model import Feedback
from .schemas import FeedbackCreate, FeedbackSummary, FeedbackWithUser


class FeedbackService:

    @staticmethod
    def create_feedback(
        db: Session, feedback_data: FeedbackCreate, user_id: int
    ) -> Feedback:
        """Create new feedback"""
        db_feedback = Feedback(
            rating=feedback_data.rating, comment=feedback_data.comment, user_id=user_id
        )
        db.add(db_feedback)
        db.commit()
        db.refresh(db_feedback)
        return db_feedback

    @staticmethod
    def get_all_feedback(
        db: Session, skip: int = 0, limit: int = 100
    ) -> List[FeedbackWithUser]:
        """Get all feedback with user information"""
        feedback_list = (
            db.query(Feedback, User.username)
            .join(User, Feedback.user_id == User.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

        return [
            FeedbackWithUser(
                id=feedback.id,
                rating=feedback.rating,
                comment=feedback.comment,
                user_id=feedback.user_id,
                created_at=feedback.created_at,
                username=username,
            )
            for feedback, username in feedback_list
        ]

    @staticmethod
    def get_feedback_summary(db: Session) -> FeedbackSummary:
        """Get feedback summary statistics"""
        result = db.query(
            func.count(Feedback.id).label("total"),
            func.avg(Feedback.rating).label("average"),
        ).first()

        total_feedback = result.total or 0
        average_rating = float(result.average) if result.average else 0.0

        return FeedbackSummary(
            total_feedback=total_feedback, average_rating=round(average_rating, 2)
        )
