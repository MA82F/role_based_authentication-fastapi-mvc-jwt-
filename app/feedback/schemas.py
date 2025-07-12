from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class FeedbackBase(BaseModel):
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5")
    comment: Optional[str] = None


class FeedbackCreate(FeedbackBase):
    pass


class FeedbackResponse(FeedbackBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class FeedbackWithUser(FeedbackResponse):
    username: str


class FeedbackSummary(BaseModel):
    total_feedback: int
    average_rating: float
